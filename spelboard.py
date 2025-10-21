#Spelboard.py
'''
spelboard.py bevat de GUI en spelbesturing voor Zeeslag.
Regelt beurtwisseling, schoten en de eindmelding.

Gemaakt door:   Mattijn Thijert
                Odessa Al-Dib
'''

import tkinter as tk
from tkinter import messagebox
import os
import sys # sys toegevoegd voor herstart van het spel - odessa
from ships import Ship, Patrouilleschip, Slagschip, Onderzeeër, Torpedobootjager, Vliegdekschip
from players import Player

# Grootte van het bord
BORD_GROOTTE = 10

# Pad naar de PNG-bestanden
IMG_PAD = os.path.join(os.path.dirname(__file__), 'img')


class ZeeslagGUI:
    def __init__(self, root, *, player1, player2):
        self.root = root
        self.root.title("Zeeslag (2 spelers)")

        # Spelers (Player objecten)
        self.p1 = player1
        self.p2 = player2

        # Namen komen uit de Player
        self.name_p1 = self.p1.name
        self.name_p2 = self.p2.name

        # Afbeeldingen
        self.images = {
            "hit": tk.PhotoImage(file=os.path.join(IMG_PAD, "Battleship_hit64.png")),
            "miss": tk.PhotoImage(file=os.path.join(IMG_PAD, "Battleship_miss64.png")),
            "unknown": tk.PhotoImage(file=os.path.join(IMG_PAD, "Battleship_unknown64.png")),
        }

        # UI: header + bord (ongewijzigd)
        header = tk.Frame(self.root); header.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 0))
        self.turn_label = tk.Label(header, text="", font=("TkDefaultFont", 12, "bold"))
        self.turn_label.pack(side="left")

        rules_btn = tk.Button(header, text="Regels", command=self.toon_regels)
        rules_btn.pack(side="right", padx=(6, 0))
        help_btn = tk.Button(header, text="Help", command=self.toon_help)
        help_btn.pack(side="right")

        self.board_frame = tk.Frame(self.root)
        self.board_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        for i in range(BORD_GROOTTE):
            self.board_frame.grid_rowconfigure(i, weight=1)
            self.board_frame.grid_columnconfigure(i, weight=1)

        self.buttons = []
        for r in range(BORD_GROOTTE):
            row_btns = []
            for c in range(BORD_GROOTTE):
                b = tk.Button(self.board_frame, image=self.images["unknown"],
                              command=lambda x=r, y=c: self.klik(x, y))
                b.grid(row=r, column=c, sticky="nsew")
                row_btns.append(b)
            self.buttons.append(row_btns)

        # Start met speler 1
        self.current = 1
        self._refresh_view()


    # ---- helpers ----
    def _current_player(self):
        return self.p1 if self.current == 1 else self.p2

    def _opponent_player(self):
        return self.p2 if self.current == 1 else self.p1

    def _current_name(self):
        return self._current_player().name

    def _opponent_name(self):
        return self._opponent_player().name

    def _refresh_view(self):
        self.root.title(f"{self._current_name()}: Schiet een schot")
        self.turn_label.config(text=f"Beurt: {self._current_name()} — schiet op {self._opponent_name()}")

        shooter = self._current_player()
        tried = shooter.tried
        # ‘Hit’ voor de schutter = schoten die raak waren; die info kun je afleiden:
        hits = shooter.tried & self._opponent_player().hits  # doorsnede: wat ik probeerde en wat echt raak was

        for r in range(BORD_GROOTTE):
            for c in range(BORD_GROOTTE):
                btn = self.buttons[r][c]
                if (r, c) not in tried:
                    btn.config(image=self.images["unknown"], state="normal")
                else:
                    state = "hit" if (r, c) in hits else "miss"
                    btn.config(image=self.images[state], state="disabled")

    def _set_board_enabled(self, enabled: bool):
        state = "normal" if enabled else "disabled"
        for r in range(BORD_GROOTTE):
            for c in range(BORD_GROOTTE):
                # laat reeds geschoten vakjes disabled blijven
                if self.buttons[r][c]["state"] == "disabled" and enabled:
                    continue
                self.buttons[r][c].config(state=state)

    def _switch_turn(self):
        """Wissel de huidige speler en toon een wisselvenster."""
        # Wissel speler (1 > 2 of 2 > 1) - odessa
        self.current = 2 if self.current == 1 else 1
        self._set_board_enabled(False) # bord tijdelijk uitschakelen tijdens beurtwissel - odessa

        # Maak een wisselvenster -odessa
        wissel_win = tk.Toplevel(self.root) # apart popup-venster boven het hoofdvenster - odessa
        wissel_win.withdraw() # bug fix: verberg het venster tijdelijk totdat we het gecentreerd hebben - odessa
        wissel_win.title("Beurtwissel")
        wissel_win.geometry("300x150") # vaste grootte voor consistentie - odessa
        wissel_win.transient(self.root) # blijft boven het hoofdvenster - odessa

        # Bericht in het venster van de beurtwissel -odessa
        msg = tk.Label(
            wissel_win,
            text=f"Beurtwissel!\n\nDraai nu het scherm naar {self._current_name()}",
            font=("TkDefaultFont", 12),
            justify="center"
        )
        msg.pack(expand=True, pady=20) # centreer bericht in venster - odess


        def doorgaan(): # funtie aangemaakt binnen de switch turn functie, die wordt aangeroepen wanneer iemand op de doorgaan knop drukt -odessa
            """Sluit het wisselvenster en ververst het bord voor de nieuwe speler."""
            wissel_win.destroy() # sluit het popup-venster -odessa
            self._refresh_view()   # update het bord voor de nieuwe speler -odessa    
            self._set_board_enabled(True)   # maakt het bord weer klikbaar voor de nieuwe speler -odessa

        # Knop om door te gaan naar de volgende speler -odessa
        tk.Button(wissel_win, text="Doorgaan", command=doorgaan).pack(pady=5) 
        # Centreer het venster
        wissel_win.update_idletasks()  # bereken venstergrootte voordat we centreren - odessa
        
        # Bereken x en y voor het in het midden plaatsen van het venster -odessa
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - 150 # Positie van het hoofdvenster. 300px breed, dus helft is 150, zodat de popup in het midden komt -odessa
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - 75 # huidige breedte en hoogte van het hoofdvenster. 150px hoog, dus helft is 75, zodat de popup in het midden komt -odessa
        
        # Plaats de popup op de berekende posities op het scherm -odessa
        wissel_win.geometry(f"+{x}+{y}") # +x+y betekent: 'zet linkerbovenhoek van het venster op (x,y) coördinaat' -odessa
        
        wissel_win.deiconify()  # maak het zichtbaar zodra het goed gepositioneerd is -odessa
        wissel_win.grab_set() # blokkeer invoer naar hoofdvenster totdat dit venster gesloten is -odessa

    # ---- interactie ----
    def klik(self, r, c):
        shooter = self._current_player()
        target  = self._opponent_player()

        if (r, c) in shooter.tried:
            return

        shooter.tried.add((r, c))              # schutter heeft hier geschoten
        resultaat = target.ontvang_aanval((r, c))  # doelwit verwerkt de kogel: zet hits/misses bij target

        # Update tegel direct:
        is_hit = (resultaat != "Mis!")
        btn = self.buttons[r][c]
        btn.config(image=self.images["hit" if is_hit else "miss"], state="disabled")

        # Meldingen bij ‘Gezonken!’
        if resultaat.startswith("Gezonken!"):
            messagebox.showinfo("Gezonken!", f"{resultaat} van {self._opponent_name()}")

        # Wincheck bij target:
        if target.alle_schepen_gezonken():
            # Bereken score van beide spelers -odessa
            # 'tried' bevat alle coördinaten waarop de speler geschoten heeft -odessa
            # 'hits' bevat alle coördinaten die echt raak waren -odessa
            treffers_sp1 = len(self.p1.tried & self.p2.hits) # schoten van speler 1 die raak waren -odessa
            missers_sp1 = len(self.p1.tried) - treffers_sp1 # overige schoten waren mis -odessa
            treffers_sp2 = len(self.p2.tried & self.p1.hits) # schoten van speler 2 die raak waren -odessa
            missers_sp2 = len(self.p2.tried) - treffers_sp2 # overige schoten waren mis -odessa


            # Toon eindscherm met scores
            eind_venster = tk.Toplevel(self.root)
            eind_venster.title("Einde spel")
            eind_venster.geometry("320x240")
            eind_venster.transient(self.root)

            # Toon winnaar -odessa
            winnaar = shooter.name
            tk.Label(
                    eind_venster,
                    text=f"{winnaar} heeft gewonnen!",
                    font=("TkDefaultFont", 14, "bold"),
                    pady=10
                ).pack()

            # Toon scores van beide spelers -odessa
            tk.Label(
                eind_venster,
                text=(
                    f"--- Scores ---\n\n"
                    f"{self.p1.name}  →  {treffers_sp1} raak, {missers_sp1} mis\n"
                    f"{self.p2.name}  →  {treffers_sp2} raak, {missers_sp2} mis"
                ),
                justify="center"
            ).pack(pady=10)

            # Knoppen: Opnieuw spelen of afsluiten -odessa
            def opnieuw_spelen():
                """Herstart het hele programma volledig, inclusief alle afbeeldingen."""
                python = sys.executable      # pad naar de huidige Python-interpreter -odessa
                os.execl(python, python, *sys.argv)  # start het script opnieuw op (verse sessie) -odessa

            def afsluiten():
                """Sluit het hele programma."""
                self.root.destroy() # sluit huidige GUI volledig af -odessa

            # Maak een frame om de knoppen netjes naast elkaar te zetten -odessa
            knop_frame = tk.Frame(eind_venster)
            knop_frame.pack(pady=10)

            # Knoppen voor opnieuw spelen en afsluiten -odessa
            tk.Button(knop_frame, text="Opnieuw spelen", command=opnieuw_spelen).grid(row=0, column=0, padx=8)
            tk.Button(knop_frame, text="Spel afsluiten", command=afsluiten).grid(row=0, column=1, padx=8)

            # Zet bord uit
            for rr in range(BORD_GROOTTE):
                for cc in range(BORD_GROOTTE):
                    self.buttons[rr][cc].config(state="disabled")
            return
       
        # Wissel beurt -odessa
        self._set_board_enabled(False) # maak bord tijdelijk niet klikbaar, zodat spelers niet meerdere keren snel achter elkaar kunnen klikken. -odessa
        self.turn_label.config(
            text=f"{shooter.name} schoot: {'Raak!' if is_hit else 'Mis!'}"
        ) # toon direct resultaat op de turn label of het schot raak of mis was -odessa

        self.root.update()   # update GUI zodat resultaat zichtbaar is voordat het wisselscherm opent -odessa
        self._switch_turn()  # start de beurtwissel -odessa

    # -------- Info --------
    def toon_help(self):
        """Toont korte uitleg over de bediening tijdens het spel."""
        messagebox.showinfo(
            "Help",
            "Klik op een vakje om te schieten op het bord van je tegenstander.\n\n"
            "Je ziet meteen of je schot raak of mis was.\n\n"
            "Bij een voltreffer verschijnt 'Gezonken!'.\n\n"
            "Na elk schot krijgt de andere speler de beurt.\n\n"
            "Draai dan het scherm of geef de muis door."
        )  # Helpvenster geschreven -odessa

    def toon_regels(self):
        """Toont korte uitleg van de spelregels."""
        messagebox.showinfo(
            "Spelregels – Zeeslag",
            "1. Plaats je vijf schepen op het bord (ze mogen niet overlappen).\n\n"
            "2. Spelers schieten om de beurt op elkaars bord.\n"
            "'Raak!' = deel van een schip. 'Gezonken!' = hele schip geraakt.\n\n"
            "3. Na elke beurt wisselen de spelers.\n"
            "Draai het scherm of geef de muis door.\n\n"
            "4. Wie als eerste alle schepen van de tegenstander laat zinken, wint!"
        )  # Regelsvenster geschreven -odessa

# Test functie die gelijk naar het eindvenster gaat voor debuggen
if __name__ == "__main__":
    root = tk.Tk()
    app = ZeeslagGUI(root, player1=Player("P1", []), player2=Player("P2", []))
    root.mainloop()