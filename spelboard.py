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
import random

# Grootte van het bord
BORD_GROOTTE = 10

# Pad naar de PNG-bestanden
IMG_PAD = os.path.join(os.path.dirname(__file__), 'img')


def schiet_op(x, y):
    """Tijdelijke testfunctie: geeft willekeurig 'raak' of 'mis' terug."""
    return random.choice(["raak", "mis"])


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
        self.maak_spelbord()

        # Helpknop
        help_knop = tk.Button(root, text="Help", command=self.toon_help)
        help_knop.pack(side=tk.RIGHT, padx=10, pady=10)

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
        resultaat = schiet_op(x, y)
        knop = self.knoppen[x][y]

        #Deactiveer de knop
        knop.config(image=self.images[resultaat], state="disabled")

    def toon_help(self):
        messagebox.showinfo("Help", "Klik op een vakje om te schieten.")


# -- testfunctie om te kijken naar aanpassingen
#if __name__ == "__main__":
#    root = tk.Tk()
#    app = ZeeslagGUI(root)
#    root.mainloop()