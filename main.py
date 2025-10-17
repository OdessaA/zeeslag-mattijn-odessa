"""
Startpunt voor het Zeeslag-spel.

Gemaakt door: Odessa Al-Dib & Mattijn Thijert
"""

import tkinter as tk
from place_ships import PlaatsingsUI

def main():
    """Start de GUI voor het plaatsen van schepen en daarna het spel."""
    root = tk.Tk()
    app = PlaatsingsUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
