"""
Startpunt voor het Zeeslag-spel.

Gemaakt door: Odessa Al-Dib & Mattijn Thijert
"""

import tkinter as tk
from place_ships import PlaatsingsUI
from tkinter import simpledialog # Voor het invoeren van namen -odessa

def main():
    """ Start de GUI voor het plaatsen van schepen en het spelen van het spel. """
    root = tk.Tk()
    root.withdraw()  # verberg tijdelijk het hoofdvenster

    # Zet standaard namen voor spelers op None zodat while loop gebruikt kan worden -odessa
    speler1_naam = None
    speler2_naam = None
    
    # Vraag namen op met een simpele dialoog -odessa
    while not speler1_naam:
        speler1_naam = simpledialog.askstring("Naam speler 1", "Voer de naam in van speler 1 (mag niet leeg zijn):")
    while not speler2_naam:
        speler2_naam = simpledialog.askstring("Naam speler 2", "Voer de naam in van speler 2 (mag niet leeg zijn):")

    root.deiconify()  # toon het hoofdvenster weer
    app = PlaatsingsUI(root, speler1_naam, speler2_naam)

    root.mainloop()

if __name__ == "__main__":
    main()