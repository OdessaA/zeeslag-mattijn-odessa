""" 
players.py bevat de Player class.
Deze class verwerkt aanvallen en checkt of alle schepen al gezonken zijn. 

Elke speler heeft: 
    - Een naam.
    - Een lijst met schepen.
    - Een verzameling coördinaten van hits en misses.
"""

from ships import TweeSchip, DrieSchip, VierSchip, VijfSchip

class Player: 
    def __init__(self, name):
        """ Initialiseren nieuwe speler. """
        self.name = name
        self.schepen = []
        self.hits = set() # Coordinaten waar de speler geraakt is. (set want dat voorkomt dubbele waardes)
        self.misses = set() # Coordinaten waar de speler miste 

    def ontvang_aanval(self, coord):
        """ Verwerkt een aanval op deze speler. """
        row, col = coord 

        for schip in self.schepen: 
            if schip.occupies(row, col):
                self.hits.add(coord)
                if schip.is_sunk(self.hits):
                    return f"Gezonken! {schip.name}" # "Gezonken!" als het schip volledig gezonken is. 
                return "Raak!" # "raak" als er een schip geraakt is maar nog niet gezonken is. 
        
        self.misses.add(coord)
        return "Mis!" # "Mis" als er geen schip op de plek ligt waar er aangevallen is. 

    def alle_schepen_gezonken(self):
        """ Checkt of alle schepen van de speler gezonken zijn. """
        for schip in self.schepen:
            if not schip.is_sunk(self.hits):
                return False # False als er minimaal één schip nog niet gezonken is.
            
        return True # True als alle schepen gezonken zijn. 
    
    def __repr__(self):
        """ Geeft een string met de naam en aantal schepen van de speler. """
        return f"Speler: {self.name}, Schepen: {len(self.schepen)}"
    
