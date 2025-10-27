#Place_Ships
'''
Zorgt ervoor dat er een boot geplaatst kan worden op een makkelijke manier

Gemaakt door:   Mattijn Thijert
                Odessa Al-Dib
'''
#---------------------------------------------------------------------------------
"""Tkinter uitleg toevoegen"""
#---------------------------------------------------------------------------------
import tkinter as tk
from tkinter import messagebox
from ships import Patrouilleschip, Onderzeeër, Torpedobootjager, Slagschip, Vliegdekschip
from players import Player 
import os
from spelboard import ZeeslagGUI 
from string import ascii_uppercase # Dit is een module die de standaard waarde van alfabet heeft, en is soms wel handig als je niet het hele ding wilt uit typen
#--------------------------------------------------------------------------------------------------

BORD_GROOTTE = 10
CEL_GROOTTE = 64
BORD_PIXELS = BORD_GROOTTE * CEL_GROOTTE

SCHEEPS_SPEC = [
    ("Vliegdekschip",   Vliegdekschip,    5, "#4c1d95"),
    ("Slagschip",       Slagschip,        4, "#B91C1C"),
    ("Onderzeeër",      Onderzeeër,       3, "#374151"),
    ("Torpedobootjager",    Torpedobootjager, 3, "#c14a09"), # 'Torpedojager' aangepast naar 'Torpedobootjager' -odessa 
    ("Patrouilleschip", Patrouilleschip,  2, "#59a14f"),
]

# Maakt de route duidelijk tot de map met de pixelarts
IMG_PAD = os.path.join(os.path.dirname(__file__), 'img')


class PlaatsingsUI(tk.Frame):
    def __init__(self, master, speler1_naam="Speler 1", speler2_naam="Speler 2"):
        super().__init__(master); self.grid(sticky="nsew")  # geef alle toestemmingen aan self.grid
        self.speler1_naam = speler1_naam # Zet de naam van speler 1 in een variabele -odessa
        self.speler2_naam = speler2_naam # Zet de naam van speler 2 in een variabele -odessa
        master.title(f"Zeeslag – {self.speler1_naam}: Plaats je vloot") # Zet een titel bovenaan de window, word ietsjes later over writen

        # ----- Instellingen (defaults) -----
        # ships_per_player: hoeveel schepen mag/zal elke speler hebben (1..len(SCHEEPS_SPEC))
        # shots_per_turn:   hoeveel schoten per beurt (1..5)
        self.settings = getattr(master, "_game_settings", {"ships_per_player": len(SCHEEPS_SPEC), "shots_per_turn": 1})

        # Basic Values instellen voor het plaatsen van schepen
        self.orientatie = tk.StringVar(value="H")     # "H" (horizontaal) of "V" (verticaal)
        self.geselecteerde_sleutel = None             # key van gekozen schip (unieke waarde)
        self.bezet = [[None]*BORD_GROOTTE for _ in range(BORD_GROOTTE)]  # raster met keys of None

        
        # Activeer alleen de eerste N schepen volgens instelling
        actieve_spec = SCHEEPS_SPEC[: self.settings["ships_per_player"]]
        # schepen: sleutel -> dict
        self.schepen = {
            naam: {"naam": naam, "klasse": cls, "lengte": lengte, "kleur": kleur,
                   "coordinaten": [], "geplaatst": False, "knop": None}
            for naam, cls, lengte, kleur in actieve_spec
        }


        # Foto voor achtergrond kiezen
        self.img_unknown = tk.PhotoImage(file=os.path.join(IMG_PAD, "Battleship_miss64.png"))
        self._tile_images = []  # zet de foto in een list om hem altijd op de juiste manier aan te kunnen roepen en als nodig te kunnen up of downscalen, kan ook zonder een list maar met meer dan 1 foto is een list altijd makkelijker
        self._tile_images.append(self.img_unknown) # met append blijven de afbeeldingen in de list staan als we meerdere afbeeldingen willen toevoegen -odessa

        # layout van het bord zonder knoppen of functies 
        paneel_links  = tk.Frame(self); paneel_links.grid(row=0, column=0, padx=8, pady=8, sticky="ns")
        paneel_rechts = tk.Frame(self); paneel_rechts.grid(row=0, column=1, padx=8, pady=8, sticky="nsew")

        # voeg de knoppen toe om een schip te kiezen dat je op het bord wilt zetten op basis van zijn unieke waarde
        palet = tk.LabelFrame(paneel_links, text="Kies een schip en klik op het bord")
        palet.pack(fill="x")
        for sleutel, schip in self.schepen.items():
            schip["knop"] = tk.Button(
                palet, text=f"{schip['naam']} ({schip['lengte']})",
                bg=schip["kleur"], fg="white", activebackground={ "activebackground": schip["kleur"] }.get("activebackground", schip["kleur"]), # zet een kleur voor de achtergrond van de knop
                command=lambda s=sleutel: self._selecteer_schip(s)
            )
            schip["knop"].pack(fill="x", pady=3)

        # Maakt het keuzemenu om te kiezen welke oriëntatie het schip heeft
        orbox = tk.LabelFrame(paneel_links, text="Oriëntatie"); orbox.pack(fill="x", pady=(6,0))
        tk.Radiobutton(orbox, text="Horizontaal", variable=self.orientatie, value="H").grid(row=0, column=0, padx=6, pady=4, sticky="w")
        tk.Radiobutton(orbox, text="Verticaal",   variable=self.orientatie, value="V").grid(row=0, column=1, padx=6, pady=4, sticky="w")
        tk.Label(orbox, text="Tip: druk 'r' om te roteren", fg="#666").grid(row=1, column=0, columnspan=2, padx=6, sticky="w")

        # Zorg ervoor dat de knoppen Help, Start en Reset naast elkaar kunnen
        actiebalk = tk.Frame(paneel_links); actiebalk.pack(fill="x", pady=(8, 0))
        links = tk.Frame(actiebalk); links.pack(side="left") # Om het makkelijk te houden is alles voor Links onder "links" gezet
        
        # Knoppen
        # Maakt een knop die alle schepen van het bord kan halen met behulp van de functie: "_reset_alle_schepen"
        tk.Button(links, text="Alles wissen", command=self._reset_alle_schepen).pack(anchor="w")
        # Maakt een hulp knop en zet deze onder de knop van reset
        tk.Button(links, text="Help", width=9, command=self.toon_help).pack(anchor="w", pady=(4, 0)) # Deze heeft wel een width statement, want help is te kort om een standaart lengte van 9 te halen
        # Instellingen-knop 
        tk.Button(links, text="⚙ Instellingen", command=self._open_instellingen).pack(anchor="w", pady=(6, 0))

        # Maakt een start knop om de boten door te sturen naar het spelbord
        tk.Frame(actiebalk).pack(side="left", expand=True, fill="x")
        self.start_knop = tk.Button(actiebalk, text="Start spel", state="disabled", command=self._start_spel) # De disabeld komt omdat uit nature hij uit staat tot de waarde in "_update_start_knop" is uitgevoerd, waarna het de waarde enabled(default) krijgt
        self.start_knop.pack(side="right") # Deze heeft er ook de waarde right bij waardoor hij dus rechts van de linker knoppen komt

        # --- WRAPPER om labels + canvas te kunnen combineren ---
        board_wrapper = tk.Frame(paneel_rechts)
        board_wrapper.pack()  # buitenste container mag 'pack' houden

        # Geef het grid (denk aan een excel tabel maar dan voor knoppen) regels om zich aan te houden om niet oneindig groot te worden
        board_wrapper.grid_rowconfigure(0, weight=0)    # Dingen met een weight van 0 zullen dus niet meetellen
        board_wrapper.grid_columnconfigure(0, weight=0)
        for r in range(1, BORD_GROOTTE + 1):
            board_wrapper.grid_rowconfigure(r, weight=1, minsize=CEL_GROOTTE)   # Dingen met een weight van 1 daartegen wel, en de minsize is de minimale groote van de cel wat dus gelijk staat aan de celgroote van de PNG
        for c in range(1, BORD_GROOTTE + 1):
            board_wrapper.grid_columnconfigure(c, weight=1, minsize=CEL_GROOTTE)

        # Maakt een opvul kolom om te zorgen dat de de tekst niet overlapt met de al bestaande grit en de hoeken van het scherm
        tk.Label(board_wrapper, text="").grid(row=0, column=0, padx=0, pady=0)

        # Maakt in de bovenste kolomlabels A - J
        for c in range(BORD_GROOTTE):
            tk.Label(
                board_wrapper, text=ascii_uppercase[c], # Dit is dus simpel gezeht neem de eerste 10 stappen uit het alfabet in het lettertype TKDefaultFont en Maakt het bolt
                font=("TkDefaultFont", 10, "bold")
            ).grid(row=0, column=c+1, padx=2, pady=(0, 4), sticky="n") # Door sticky te gebruiken staan ze vast aan de knop (klikvakje) wat eronde zit, de rest is om de groote en locatie te bepalen van de cordinaten waar in de grit het beland

        # Maakt in de linker rijlabels 1 - 10
        for r in range(BORD_GROOTTE):
            tk.Label(
                board_wrapper, text=str(r+1), # Hier doe je precies hetzelfde maar dan met een getal wat je elke keer +1 doet tot er geen rijen meer zijn in het speelveld
                font=("TkDefaultFont", 10, "bold")
            ).grid(row=r+1, column=0, padx=(0, 6), pady=2, sticky="e")

        # Maakt een canvas (je kunt het zien als een vierkante shape in excel) over je klikknoppen heen om ze als "1" vak te kunnen behanden in opmaak
        self.canvas = tk.Canvas(
            board_wrapper,
            width=BORD_PIXELS, height=BORD_PIXELS,
            highlightthickness=0
        )
        self.canvas.grid(       # geef het canvas een grit om nieuwe knoppen op te zetten 
            row=1, column=1,
            rowspan=BORD_GROOTTE, columnspan=BORD_GROOTTE,
            sticky="nsew"   # Als je sticky op nsew zet kan de grote van de cel meeschalen aan de grote van jou gritruimte waardoor hij altijg zo groot mogelijk probeerd te zijn binnen zijn toegestaande regels
        )

        # Leg per cel een tegel neer + dun grid erbovenop
        self.cell_items = {}  # Maakt een list om uiteindelijk makkelijk de klikknoppen in te kunnen zetten, en te kunnen wijzigen
        for r in range(BORD_GROOTTE):
            for c in range(BORD_GROOTTE):
                x0 = c * CEL_GROOTTE
                y0 = r * CEL_GROOTTE

                # Voeg de PNG toe als opvulling van de klikknop
                img_id = self.canvas.create_image(
                    x0, y0, # Cordinaten om bij te houden waar de knop/tegel zit
                    image=self.img_unknown,
                    anchor="nw",    # Met nw (noord-west) lijn je een knop of wat dan ook uit aan de linker bovenkant van een cell
                    tags=("cell", f"r{r}c{c}", "tile"),
                )
                self.cell_items[(r, c)] = img_id # Voeg de knoppen toe aan de lijst

                # Maakt een klein dun lijntje tussen alle Cellen die op het canvas worden gezet, is niet nodig, maar staat wel mooier
                self.canvas.create_rectangle(
                    x0, y0, x0 + CEL_GROOTTE, y0 + CEL_GROOTTE, # cordinaten en lengte
                    outline="#cccccc", width=1, tags=("grid",) # Kies een kleur en de breete voor het decorative lijntje
                )

        # Zorgt ervoor dat de knop netjes op het grid ligt
        self.canvas.tag_lower("tile", "grid")

        # Evenementen (gebeurtenissen)
        self.canvas.bind("<Motion>", self._muis_beweging) # Elke muisbeweging word bijgehouden om een perfecte preview te kunnen geven
        self.canvas.bind("<Leave>", lambda e: self.canvas.delete("preview")) # Als je het canvas verlaat (kliktegels) verlaat word de previeuw ook weg gehaald
        self.canvas.bind("<Button-1>", self._linker_klik) # Houd bij of je op je linker muisknop drukt om een ship te plaatsen

        # Rechtsklik functie op alle platformen: Windows/Linux en MacOS -odessa
        self.canvas.bind("<Button-3>", self._rechter_klik)          # Windows/Linux -odessa 
        self.canvas.bind("<Button-2>", self._rechter_klik)          # macOS -odessa
        self.canvas.bind("<Control-Button-1>", self._rechter_klik)  # macOS alternatief voor rechtsklik -odessa

        master.bind("r", lambda e: self.orientatie.set("V" if self.orientatie.get()=="H" else "H")) # Houd  bij of er op "r" word gedrukt om de oriëntatie slider te wisselen van horizontaal naar verticaal of andersom

        self.speler_index = 1   # Houd bij welke speler schepen mag plaatsen
        self.vloot_speler1 = None

    # ---------- helpers ----------                                                                                                                                                                                                                                                             help mij ook, moet dit niet doen om half 2
    """Dit zijn functies die zorgen dat __init__ kan werken"""
    # Deze functie zorgt dat je maar 1 schip van elk soort kunt plaatsen
    def _selecteer_schip(self, sleutel):
        if self.schepen[sleutel]["geplaatst"]:
            return
        self.geselecteerde_sleutel = sleutel
        for k, schip in self.schepen.items():
            schip["knop"].config(relief=("sunken" if k == sleutel else "raised"))

    # Checked of alle spots van het schip binnen het veld vallen
    def _binnen_bord(self, rij, kol): 
        return 0 <= rij < BORD_GROOTTE and 0 <= kol < BORD_GROOTTE

    
    def _voetafdruk(self, rij, kol, lengte, orient):
        return ([(rij, kol+i) for i in range(lengte)] if orient == "H"
                else [(rij+i, kol) for i in range(lengte)])

    # Checked of alle spots nog vrij zijn en niet of er al een ander schip ligt
    def _plek_vrij(self, coords):
        return all(self._binnen_bord(r, c) and self.bezet[r][c] is None for r, c in coords)

    # Maakt de cellen aan waar schepen geplaatst kunnen worden
    def _teken_cel(self, rij, kol, **kwargs):
        x0, y0 = kol*CEL_GROOTTE+1, rij*CEL_GROOTTE+1
        x1, y1 = x0+CEL_GROOTTE-2, y0+CEL_GROOTTE-2
        return self.canvas.create_rectangle(x0, y0, x1, y1, **kwargs)

    # Geeft tekst aan de helpfunctie knop
    def toon_help(self):
        """Toont een helpbericht met instructies voor het plaatsen van schepen."""
        messagebox.showinfo("Help", "Selecteer een schip links en klik op het bord om het te plaatsen.\n"
                            "Klik met rechts om een schip te verwijderen.\n\n"
                            "Druk op 'r' om de oriëntatie (horizontaal/verticaal) te wisselen.") # Helpfunctie tekst geschreven -odessa

    # ---------- interactie ----------
    """Dit zijn functies die bijhouden wat er gebreurd met de muis of toetsenbord"""
    # Houd bij waar je muis is tijdens het runnen van de code en maakt de juiste keuzes op wat jij doet
    def _muis_beweging(self, e):
        self.canvas.delete("preview")
        if not self.geselecteerde_sleutel:
            return
        rij, kol = e.y // CEL_GROOTTE, e.x // CEL_GROOTTE
        schip = self.schepen[self.geselecteerde_sleutel]
        coords = self._voetafdruk(rij, kol, schip["lengte"], self.orientatie.get())
        toegestaan = self._plek_vrij(coords)
        for r, c in coords:
            if self._binnen_bord(r, c):
                self._teken_cel(r, c, outline=("#2a2" if toegestaan else "#a22"),
                                width=2, fill="", tags="preview")

    # Kijkt wanneer er op de linker muisknop word gedrukt om een schip te plaatsen, en of die spot wel vrij is, anders doet het niets
    def _linker_klik(self, e):
        if not self.geselecteerde_sleutel:
            messagebox.showinfo("Kies schip", "Selecteer eerst een schip links in de balk."); return
        rij, kol = e.y // CEL_GROOTTE, e.x // CEL_GROOTTE
        schip = self.schepen[self.geselecteerde_sleutel]
        coords = self._voetafdruk(rij, kol, schip["lengte"], self.orientatie.get())
        if not self._plek_vrij(coords):
            self.master.bell(); return

        tag = f"schip_{self.geselecteerde_sleutel}"
        for r, c in coords:
            self.bezet[r][c] = self.geselecteerde_sleutel
            self._teken_cel(r, c, fill=schip["kleur"], width=0, tags=("ship", tag))
        schip["coordinaten"], schip["geplaatst"] = coords, True
        schip["knop"].config(state="disabled", relief="raised")
        self.geselecteerde_sleutel = None
        self.canvas.delete("preview") # Haal de preview weg als je een ship geplaatst hebt
        self._update_start_knop()

    # Kijkt wanneer er op de rechter muisknop word gerukt en of er een schip is en haalt die dan weg
    def _rechter_klik(self, e):
        rij, kol = e.y // CEL_GROOTTE, e.x // CEL_GROOTTE
        if not self._binnen_bord(rij, kol): 
            return
        sleutel = self.bezet[rij][kol]
        if sleutel is None: # Er word hier gewerkt met sleutel om te kunnen kijken welk schip het is
            return
        schip = self.schepen[sleutel]
        for r, c in schip["coordinaten"]:
            self.bezet[r][c] = None
        self.canvas.delete(f"schip_{sleutel}")
        schip["coordinaten"], schip["geplaatst"] = [], False
        schip["knop"].config(state="normal")    # Reset de nu lege tegel om er een mogelijk nieuw schip op te kunnen zetten
        self._update_start_knop()

    # Haalt alle schepen in 1x van het bord af om makkelijk opnieuw te kunnen beginnen
    def _reset_alle_schepen(self):
        for schip in self.schepen.values():
            schip["coordinaten"] = []
            schip["geplaatst"] = False
            schip["knop"].config(state="normal", relief="raised")
        for r in range(BORD_GROOTTE):
            for c in range(BORD_GROOTTE):
                self.bezet[r][c] = None
        self.geselecteerde_sleutel = None
        self.canvas.delete("ship"); self.canvas.delete("preview")
        self._update_start_knop() # Reset ook weer de startknop, anders zou je het spel kunenn starten zonder shepen
        self.update_idletasks() 


    # Houd bij welke schepen al geplaatst zijn
    def _alle_geplaatst(self):
        return all(s["geplaatst"] for s in self.schepen.values())


    # houd bij wanneer alle schepen geplaatst zijn en toestemming mag geven om de spelstart knop toegangkelijk te maken
    def _update_start_knop(self):
        """Update de status van de startknop op basis van of alle schepen zijn geplaatst."""
        ready = self._alle_geplaatst()
        if ready:
            # Kies tekst afhankelijk van welke speler bezig is - odessa
            tekst = "Vloot geplaatst" if self.speler_index == 1 else "Start Zeeslag!"

            # Enabled-look
            self.start_knop.config(
                state="normal",      # In andere woorden "enabled"
                bg="#40c470",        # Zet een kleur voor de achtergrond van de knop
                fg="white",          # Zet een kleur voor de voorgrond van de knop
                activebackground="#2c8f50",
                activeforeground="white",
                cursor="hand2"       # Op het moment dat je de knop aan kunt drukken word het zo leuk klik handje
            )
            self.start_knop.config(text=tekst)

        else:
            # Disabled-look
            self.start_knop.config(
                state="disabled",    # Zorgt dat de knop niet ingedrukt kan worden
                bg="#f3f4f6",          
                fg="#f3f4f6",
                activebackground="#f3f4f6",
                activeforeground="#f3f4f6",
                disabledforeground="#f3f4f6",
                cursor="arrow"       # Hetzelfde pijltje als de rest van het programma
            )


    def _herstart_met_settings(self, ships_per_player, shots_per_turn):
        """Sla de aangepaste settings aan, en start een nieuw spel op met die settings"""
        from tkinter import messagebox
        # Waarschuwing als er al plaatsingen zijn
        if any(s["geplaatst"] for s in self.schepen.values()):
            if not messagebox.askyesno("Let op", "Instellingen wijzigen reset je huidige plaatsing. Doorgaan?"):
                return

        # Sla settings op aan het master-venster zodat ze behouden blijven
        setattr(self.master, "_game_settings", {
            "ships_per_player": int(ships_per_player),
            "shots_per_turn": int(shots_per_turn),
        })

        # Rebuild UI met dezelfde spelersnamen
        master = self.master
        speler1, speler2 = self.speler1_naam, self.speler2_naam
        for w in master.winfo_children():
            w.destroy()
        PlaatsingsUI(master, speler1, speler2)


    def _open_instellingen(self):
        """Dialoog: aantal schepen per speler en schoten per beurt."""
        win = tk.Toplevel(self.master)
        win.title("Instellingen")
        win.transient(self.master)
        win.resizable(False, False)

        # Huidige waarden
        ships_var = tk.IntVar(value=self.settings["ships_per_player"])
        shots_var = tk.IntVar(value=self.settings["shots_per_turn"])

        frm = tk.Frame(win, padx=12, pady=12); frm.pack(fill="both", expand=True)

        # Aantal schepen per speler
        tk.Label(frm, text=f"Aantal schepen per speler (1–{len(SCHEEPS_SPEC)}):").grid(row=0, column=0, sticky="w")
        tk.Spinbox(frm, from_=1, to=len(SCHEEPS_SPEC), textvariable=ships_var, width=5)\
            .grid(row=0, column=1, sticky="w", padx=(8,0))

        # Schoten per beurt
        tk.Label(frm, text="Schoten per beurt (1–5):").grid(row=1, column=0, sticky="w", pady=(6,0))
        tk.Spinbox(frm, from_=1, to=5, textvariable=shots_var, width=5)\
            .grid(row=1, column=1, sticky="w", padx=(8,0), pady=(6,0))

        tk.Label(frm, text="Wijzigen reset het plaats-scherm.", fg="#a00")\
            .grid(row=2, column=0, columnspan=2, sticky="w", pady=(10,0))

        # Buttons
        btns = tk.Frame(frm); btns.grid(row=3, column=0, columnspan=2, sticky="e", pady=(10,0))
        tk.Button(btns, text="Annuleren", command=win.destroy).pack(side="left", padx=(0,6))
        def toepassen():
            win.destroy()
            self._herstart_met_settings(ships_var.get(), shots_var.get())
        tk.Button(btns, text="Toepassen", command=toepassen).pack(side="left")

        # Positioneer linksonder van hoofdvenster
        self.master.update_idletasks()
        x = self.master.winfo_x() + 16
        y = self.master.winfo_y() + self.master.winfo_height() - 260
        win.geometry(f"+{x}+{y}")
        win.grab_set()


    # ---------- Start spel ----------
   
    def _start_spel(self):
        """Checkt of alle variabelen goed zijn om door te gaan naar spelboard en of bijde spelers hun vloot hebben ingevuld"""
    # Check: zijn alle schepen geplaatst?
        if not self._alle_geplaatst():
            messagebox.showinfo("Nog niet klaar", "Plaats eerst alle schepen.")
            return  # Zou als het goed is nooit mogen uitgevoerd worden, maar je weet het nooit

        # Vloot bouwen uit huidige GUI (grid)
        vloot = []
        for schip in self.schepen.values():
            inst = schip["klasse"]()
            inst.set_coordinates(schip["coordinaten"])
            vloot.append(inst)

        if self.speler_index == 1:
            # Bewaar vloot speler 1 en reset voor speler 2
            self.vloot_speler1 = vloot
            self._reset_alle_schepen()

            # Laat speler 2 schepen plaatsen
            self.speler_index = 2
            self.master.deiconify()
            self.master.title(f"Zeeslag – {self.speler2_naam}: Plaats je vloot")

            messagebox.showinfo(
                f"{self.speler1_naam} klaar",                               # Aanpassing in de tekst zodat de namen van de spelers worden gebruikt -odessa
                f"{self.speler1_naam} heeft zijn/haar vloot geplaatst.\n\n"
                f"Geef nu de muis of laptop aan {self.speler2_naam},\n"
                f"zodat {self.speler2_naam} zijn/haar vloot kan plaatsen."
            )
            return

        # Speler 2 klaar → start het spel
        vloot_speler2 = vloot
        top = tk.Toplevel(self.master) # Zet het venster bovenop al je andere vensters
        top.title("Zeeslag (2 spelers)")

        p1 = Player(self.speler1_naam, self.vloot_speler1)# Maak de spelers aan met hun naam (niet meer hardcoded als "speler 1" of "speler 2") -odessa
        p2 = Player(self.speler2_naam, vloot_speler2)
        spt = getattr(self.master, "_game_settings", {}).get("shots_per_turn", 1) # shots_per_turn doorgeven aan het spelbord
        self.game = ZeeslagGUI(top, player1=p1, player2=p2, shots_per_turn=int(spt))

        self.master.withdraw() # Sluit het place_ships tkinter interactive pannel (GUI)



# Voer een test uit op alleen de code in dit bestand
if __name__ == "__main__":
    root = tk.Tk()
    PlaatsingsUI(root)
    root.mainloop()
