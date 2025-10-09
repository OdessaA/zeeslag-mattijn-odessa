#Spelboard.py
'''
In dit bestand word het spelbord van de zeeslag bijgehouden, en de graphical GUI bijgehouden

Gemaakt door:   Mattijn Thijert
                ...
'''
#---------------------------------------------------------------------------------
"""CODE WERKT NOG NIET EN KAN DUS OOK NOG NIET RUNNEN"""
#---------------------------------------------------------------------------------
import tkinter as tk
from tkinter import messagebox
import os

#Bepaal de grote van je bord, 
#default value = 10
BORD_GROOTTE = 10


# Pad naar de PNG-bestanden
IMG_PAD = os.path.join(os.path.dirname(__file__), 'img')
class ZeeslagGUI:
    def init(self, root):
        self.root = root
        self.root.title("Zeeslag")

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
                    text=" ",
                    width=4,
                    height=2,
                    command=lambda x=rij, y=kolom: self.schiet_en_update(x, y)
                )
                knop.grid(row=rij, column=kolom)
                rij_knoppen.append(knop)
            self.knoppen.append(rij_knoppen)

    def schiet_en_update(self, x, y):
        resultaat = schiet_op(x, y)  # voor als je hit miss wilt doen

        knop = self.knoppen[x][y]

        if resultaat == "raak":
            knop.config(image=self.images["raak"], width=32, height=32)
            knop.image = self.images["raak"]
        else:
            knop.config(image=self.images["mis"], width=32, height=32)
            knop.image = self.images["mis"]

        #Deactiveer de knop
        knop.config(state="disabled")

    #nog niet totaal klaar maar moest er iets bijdoen anders kreeg ik een error
    def toon_help(self):
        messagebox.showinfo("Help", "Klik op een vakje om te schieten.")