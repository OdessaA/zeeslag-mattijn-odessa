#Spelboard.py
'''
In dit bestand word het spelbord van de zeeslag, en de graphical GUI bijgehouden

Gemaakt door:   Mattijn Thijert
                Odessa Al-Dib
'''
#---------------------------------------------------------------------------------
"""De functies `schiet_op` en `toon_help` hebben nog aanpassing nodig"""
#---------------------------------------------------------------------------------
import tkinter as tk
from tkinter import messagebox
import os
from ships import Ship, Patrouilleschip, Slagschip, Onderzeeër, Torpedobootjager, Vliegdekschip

# Grootte van het bord
BORD_GROOTTE = 10

# Pad naar de PNG-bestanden
IMG_PAD = os.path.join(os.path.dirname(__file__), 'img')


class ZeeslagGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Zeeslag")
     
        # Laad afbeeldingen
        self.images = {
            "hit": tk.PhotoImage(file=os.path.join(IMG_PAD, "Battleship_hit.png")),
            "miss": tk.PhotoImage(file=os.path.join(IMG_PAD, "Battleship_miss.png")),
            "unknown": tk.PhotoImage(file=os.path.join(IMG_PAD, "Battleship_unknown.png"))
        }

        self.knoppen = []
        self.hits = set()   # houdt bij welke coördinaten zijn geraakt
        self.schepen = []

         # Rechter kolom: bediening
        controls = tk.Frame(self.root)
        controls.grid(row=0, column=1, sticky="n", padx=10, pady=10)

        # Helpknop
        help_knop = tk.Button(controls, text="Help", width=10, command=self.toon_help)
        help_knop.grid(row=0, column=0, padx=10, pady=(0, 10), sticky="e")

        # Rules
        rules_knop = tk.Button(controls, text="Regels", width=10, command=self.toon_regels)
        rules_knop.grid(row=1, column=0, padx=10, pady=10, sticky="e")

        # Linker kolom: spelbord
        self.bord_frame = tk.Frame(self.root)
        self.bord_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.plaats_schepen()
        self.maak_spelbord()

    def schiet_op(self, x, y):
        """Controleer of (x, y) een schip raakt."""
        # Optioneel: voorkomen dat je twee keer op hetzelfde vakje 'schiet'
        if (x, y) in self.hits:
            return "miss"  # of raise/geen actie — ik kies hier 'mis' zodat GUI ermee om kan gaan

        self.hits.add((x, y))
        for schip in self.schepen:
            if schip.occupies(x, y):
                if schip.is_sunk(self.hits):
                    # Optioneel: geef een melding wanneer een schip gezonken is
                    messagebox.showinfo("Gezonken!", f"{schip.name} is gezonken!")
                return "hit"
        return "miss"

    def maak_spelbord(self):
        # Zorg dat het bord mee kan schalen
        for i in range(BORD_GROOTTE):
            self.bord_frame.grid_rowconfigure(i, weight=1)
            self.bord_frame.grid_columnconfigure(i, weight=1)

        # (Her)bouw knoppen
        self.knoppen.clear()
        for rij in range(BORD_GROOTTE):
            rij_knoppen = []
            for kolom in range(BORD_GROOTTE):
                knop = tk.Button(
                    self.bord_frame,
                    image=self.images["unknown"],
                    command=lambda x=rij, y=kolom: self.schiet_en_update(x, y)
                )
                # Plaats elke knop in het grid en laat ‘m vullen
                knop.grid(row=rij, column=kolom, sticky="nsew")
                rij_knoppen.append(knop)
            self.knoppen.append(rij_knoppen)

    def schiet_en_update(self, x, y):
        resultaat = self.schiet_op(x, y)
        knop = self.knoppen[x][y]
        
        #Deactiveer de knop
        knop.config(image=self.images[resultaat], state="disabled")

    
    def plaats_schepen(self):
        """Plaats de schepen op het bord (voorlopig vast)."""
        
        schip1 = Patrouilleschip()
        schip1.set_coordinates([(0, 0), (0, 1)])

        schip2 = Onderzeeër()
        schip2.set_coordinates([(2, 3), (3, 3), (4, 3)])

        schip3 = Slagschip()
        schip3.set_coordinates([(6, 6), (6, 7), (6, 8), (6, 9)])

        self.schepen = [schip1, schip2, schip3]

    def toon_help(self):
        messagebox.showinfo("Help", "Klik op een vakje om te schieten.")

    def toon_regels(self):
        messagebox.showinfo("Regels", "leeg")

# -- testfunctie om te kijken naar aanpassingen
if __name__ == "__main__":
    root = tk.Tk()
    app = ZeeslagGUI(root)
    root.mainloop()