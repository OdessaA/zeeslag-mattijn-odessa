""" 
ships.py bevat een parentklasse (Ship) en subklassen voor elke schipsoort.

Elk Ship bevat: 
    - De naam van het schip. (bijv. "Tweeboot").
    - De lengte van het schip: het aantal vakjes dat het schip in beslag neemt. 
    - Een lijst van coördinaten die aangeven waar een schip precies ligt. (bijv. [(1,2), (1,3), (1,4)]).

    Gemaakt door:   Odessa Al-Dib
"""

class Ship: # Parent-klasse voor alle schepen. 
    """ Parentklasse voor schepen met naam, lengte en coördinaten. """

    def __init__(self, length, name="Onbekend"):
        """ Maakt een schip met opgegeven lengte en naam. """
        self.name = name
        self.length = length 
        self.coordinates = []

    def set_coordinates(self, coords):
        """ Stelt de coördinaten van het schip in. """
        if len(coords) != self.length: 
            raise ValueError("Aantal coördinaten komt niet overeen met de lengte van het schip.")
        self.coordinates = coords 

    def occupies(self, row, col):
        """ Checkt of een schip een bepaald vakje op het speelbord bezet. """
        for coord in self.coordinates: # Loop door alle coördinaten van het schip. 
            if coord == (row, col): # Als het opgegeven coördinaat in de functie gelijk is aan de coördinaat van het schip krijg je True terug. 
                return True
        return False
    
    def is_sunk(self, hits):
        """ Geeft True als alle vakjes van het schip geraakt zijn. """
        for coord in self.coordinates:
            if coord not in hits: # Als één vakje nog niet geraakt is, is het schip nog niet gezonken 
                return False
        return True           
    
    def __repr__(self):
        """ Tekstweergave van het schip. """
        return f"Schip lengte = {self.length}\nSchip coördinaten = {self.coordinates}"

class TweeSchip(Ship): 
    """ Schip van twee vakjes. """
    def __init__(self): 
        super().__init__(2, name="Tweeboot") 

class DrieSchip(Ship): 
    """Schip van drie vakjes. """
    def __init__(self):
        super().__init__(3, name="Drieboot")

class VierSchip(Ship): 
    """ Schip van vier vakjes. """
    def __init__(self):
        super().__init__(4, name="Vierboot")

class VijfSchip(Ship): 
    """ Schip van vijf vakjes. """
    def __init__(self):
        super().__init__(5, name="Vijfboot")