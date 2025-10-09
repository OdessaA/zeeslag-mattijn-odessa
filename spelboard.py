#Spelboard.py
'''
In dit bestand word het spelbord van de zeeslag, en de graphical GUI bijgehouden

Gemaakt door:   Mattijn Thijert
                ...
'''
#---------------------------------------------------------------------------------
"""De functies `schiet_op` en `toon_help` hebben nog aanpassing nodig"""
#---------------------------------------------------------------------------------
import tkinter as tk
from tkinter import messagebox
import os
from ships import Ship, TweeSchip, DrieSchip, VierSchip, VijfSchip


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
            "raak": tk.PhotoImage(file=os.path.join(IMG_PAD, "Battleship_hit.png")),
            "mis": tk.PhotoImage(file=os.path.join(IMG_PAD, "Battleship_miss.png")),
            "unknown": tk.PhotoImage(file=os.path.join(IMG_PAD, "Battleship_unknown.png"))
        }

        self.knoppen = []
        self.hits = set()   # houdt bij welke coördinaten zijn geraakt
        self.schepen = []

        self.plaats_schepen()
        self.maak_spelbord()

        # Helpknop
        help_knop = tk.Button(root, text="Help", command=self.toon_help)
        help_knop.pack(side=tk.RIGHT, padx=10, pady=10)

    def schiet_op(self, x, y):
        """Controleer of (x, y) een schip raakt."""
        # Optioneel: voorkomen dat je twee keer op hetzelfde vakje 'schiet'
        if (x, y) in self.hits:
            return "mis"  # of raise/geen actie — ik kies hier 'mis' zodat GUI ermee om kan gaan

        self.hits.add((x, y))
        for schip in self.schepen:
            if schip.occupies(x, y):
                if schip.is_sunk(self.hits):
                    # Optioneel: geef een melding wanneer een schip gezonken is
                    messagebox.showinfo("Gezonken!", f"{schip.name} is gezonken!")
                return "raak"
        return "mis"

    def maak_spelbord(self):
        bord_frame = tk.Frame(self.root)
        bord_frame.pack(side=tk.LEFT, padx=10, pady=10)

        for rij in range(BORD_GROOTTE):
            rij_knoppen = []
            for kolom in range(BORD_GROOTTE):
                knop = tk.Button(
                    bord_frame,
                    image=self.images["unknown"],
                    command=lambda x=rij, y=kolom: self.schiet_en_update(x, y)
                )
                knop.grid(row=rij, column=kolom)
                rij_knoppen.append(knop)
            self.knoppen.append(rij_knoppen)

    def schiet_en_update(self, x, y):
        resultaat = self.schiet_op(x, y)
        knop = self.knoppen[x][y]
        
        #Deactiveer de knop
        knop.config(image=self.images[resultaat], state="disabled")

    
    def plaats_schepen(self):
        """Plaats de schepen op het bord (voorlopig vast)."""
        
        schip1 = TweeSchip()
        schip1.set_coordinates([(0, 0), (0, 1)])

        schip2 = DrieSchip()
        schip2.set_coordinates([(2, 3), (3, 3), (4, 3)])

        schip3 = VierSchip()
        schip3.set_coordinates([(6, 6), (6, 7), (6, 8), (6, 9)])

        self.schepen = [schip1, schip2, schip3]

    def toon_help(self):
        messagebox.showinfo("Help", "Klik op een vakje om te schieten.")


# -- testfunctie om te kijken naar aanpassingen
#if __name__ == "__main__":
#    root = tk.Tk()
#    app = ZeeslagGUI(root)
#    root.mainloop()