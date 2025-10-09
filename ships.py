"""
ships.py definieert de Ship klassen voor het spel. 

De module bevat: 
    - Een parent-klasse met gemeenschappelijke functies. 
    - Subklassen 

    Deze opzet gebruikt overerving zodat elk type schip automatisch 
    de juiste lengte en naam krijgt. 
"""

class Ship: # Parent-klasse voor alle schepen. 
    """
    Parent klasse voor alle schepen in het spel. 

    Elk schip bestaat uit een bepaalde lengte (aantal vakjes dat het inneemt) en 
    een lijst met coördinaten die aangeven waar het schip zich op het spelbord bevindt. 
    
    Attributen:
        name (str): de naam van het schip (bijv. 'Tweeboot', 'Drieboot').
        length (int): hoeveel vakjes het schip inneemt. 
        coordinates (list): lijst met (rij, kolom)-paren die de positie van het schip aangeven. 
    """

    def __init__(self, length, name="Onbekend"):
        """
        Initialiseert een nieuw schip. 

        Arguments: 
            length(int): hoeveel vakjes het schip innneemt.
            name (str): 
        """
        self.name = name
        self.length = length 
        self.coordinates = []
    def set_coordinates(self, coords):
        """
        Plaatst het schip op het bord door coördinaten in te vullen 

        Argumenten: 
            coords (list): een lijst met de vakjes waar het schip ligt. 
            Elk vakje als (rij, kolom). 
        
        Raises: 
            ValueError: Als het aantal coördinaten niet overeenkomt met de lengte.
        """
        if len(coords) != self.length: # controleert of het aantal opgegeven vakjes overeenkomt met de lente van het schip. 
            raise ValueError("Aantal coördinaten komt niet overeen met de lengte van het schip.")
        self.coordinates = coords 

    def occupies(self, row, col):
        """
        Controleert of het schip het vakje (row, col) bezet. 

        Arguments: 
            row (int): Rij index op het bord
            col(int): Kolom index op het bord 
        Returns: 
            bool: True als het vakje deel uitmaakt van het schip, anders False.
        """
        return (row, col) in self.coordinates
    
    def is_sunk(self, hits):
        """
        Controleer of het schip volledig gezonken is. 
        
        Arguments: 
            hits (set): een set met (row, col)-paren die geraakt zijn door de tegenstander. 
        
        Returns:
            bool: True als alle coördinaten van het schip in hits voorkomen, anders False.
        """
        return all(coord in hits for coord in self.coordinates)
    
    def __repr__(self):
        """
        Geeft een tekstrepresentatie van het schip terug.

        Returns:
            str: een string met de lengte en de coördinaten. 
        """
    
        return f"Schip lengte = {self.length}\nSchip coördinaten = {self.coordinates}"

class TweeSchip(Ship): 
    def __init__(self): 
        super().__init__(2, name="Tweeboot")

class DrieSchip(Ship): 
    def __init__(self):
        super().__init__(3, name="Drieboot")

class VierSchip(Ship): 
    def __init__(self):
        super().__init__(4, name="Vierboot")

class VijfSchip(Ship): 
    def __init__(self):
        super().__init__(5, name="Vijfboot")