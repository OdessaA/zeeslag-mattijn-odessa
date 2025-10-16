#Spelboard.py
'''
In dit bestand word het spelbord van de zeeslag, en de graphical GUI bijgehouden

Gemaakt door:   Mattijn Thijert
                Odessa Al-Dib
'''
#---------------------------------------------------------------------------------
"""Pauze bij beurtwissel en wisselscherm"""
#---------------------------------------------------------------------------------
import tkinter as tk
from tkinter import messagebox
import os
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
        self.current = 2 if self.current == 1 else 1
        self._refresh_view()
        self._set_board_enabled(True)

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
            messagebox.showinfo("Einde spel", f"{shooter.name} heeft gewonnen!")
            for rr in range(BORD_GROOTTE):
                for cc in range(BORD_GROOTTE):
                    self.buttons[rr][cc].config(state="disabled")
            return
       
        # --- 5s pauze vóór wisselen ---
        self._set_board_enabled(False)  # voorkom dubbel klikken tijdens de pauze
        self.turn_label.config(
            text=f"{shooter.name} schoot: {'Raak!' if is_hit else 'Mis!'} — wisselt over 5s"
        )
        # Plan de wissel over 5000 ms, zonder GUI vast te laten lopen
        self.root.after(5000, self._switch_turn) # time.sleep zou de GUI vast laten lopen en dan mogelijk niet meer kunnen laten doorstarten

        # beurt wisselen
        self.current = 2 if self.current == 1 else 1
        self._refresh_view()


    # -------- Info --------
    def toon_help(self):
        messagebox.showinfo("Help", "Klik op een vakje om te schieten.")

    def toon_regels(self):
        messagebox.showinfo("Regels", "leeg")

# -- testfunctie om te kijken naar aanpassingen
if __name__ == "__main__":
    root = tk.Tk()
    app = ZeeslagGUI(root, player1=Player("P1", []), player2=Player("P2", []))
    root.mainloop()
