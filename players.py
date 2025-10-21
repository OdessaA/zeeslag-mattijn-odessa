""" 
players.py bevat de Player class.
Deze class verwerkt aanvallen en checkt of alle schepen al gezonken zijn. 

Elke speler heeft: 
    - Een naam.
    - Een lijst met schepen.
    - Een verzameling coördinaten van hits en misses.
    
    Gemaakt door: Odessa Al-Dib

    Kleine aanpassing: Mattijn Thijert

    Deze class hoort bij het Zeeslag-spel en wordt gebruikt in spelboard.py.
"""

class Player:
    """Parent klasse voor een speler in het spel."""
    def __init__(self, name, ships=None):
        """Initialiseer een speler: naam van de speler, lijst met schepen en een verzameling coördinaten van hits en misses."""
        self.name = name
        self.schepen = list(ships or []) # Lijst van schepen, bijvoorbeeld [Slagschip(), Onderzeeër(), ...]
        self.hits = set()    # Coördinaten waar deze speler geraakt is door de tegenstander. (set want dat voorkomt dubbele waardes)
        self.misses = set()  # Coördinaten waar de tegenstander miste bij deze speler.
        self.tried = set()   # Alle coördinaten waar de speler al op geschoten heeft

    def set_ships(self, ships):
        """Stel de schepen van de speler in."""
        self.schepen = list(ships or []) 

    def ontvang_aanval(self, coord): 
        """
        Verwerkt een aanval op deze speler op de gegeven coördinaat.
        Returns:
            - 'Raak!' als een schip geraakt wordt.
            - 'Gezonken! [scheepsnaam]' als het schip volledig geraakt is.
            - 'Mis!' als er geen schip op dat vakje ligt.
        """
        row, col = coord
        for schip in self.schepen:
            if schip.occupies(row, col):
                self.hits.add(coord)
                if schip.is_sunk(self.hits):
                    return f"Gezonken! {schip.name}" 
                return "Raak!" 
        self.misses.add(coord)
        return "Mis!" 

    def alle_schepen_gezonken(self): 
        """Controleer of alle schepen van de speler gezonken zijn."""
        return all(s.is_sunk(self.hits) for s in self.schepen) 