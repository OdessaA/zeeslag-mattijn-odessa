"""
ships.py definieert de Ship-klasse voor het spel. 
"""

class Ship:
    """
    Een schip in het zeeslag spel. Bestaat uit een aantal vakjes (lentgh) 
    en lijst met coördinaten (rij, kolom). 
    
    Attributen:
        length (int): hoeveel vakjes het schip inneemt. 
        coordinates (list): lijst met (rij, kolom)-paren waar het schip ligt. 
    """
    def __init__(self, length, coordinates=None):
        """
        Initialiseert een nieuw schip. 

        Arguments: 
            length(int): hoeveel vakjes het schip innneemt.
            coordinates (list of None): een optinele lijst van coördinaten als (rij, kolom)-paren.
                                        Als None, word het schip gemaakt zonder meteen coördinaten mee te geven. 
        """
        self.length = int(length)
        self.coordinates = coordinates if coordinates is not None else [] # Zorgt dat coordinates altijd een lijst is 

    def occupies(self, row, col):
        """
        Controleert of het schip het vakje (row, col) bezet. 

        Arguments: 
            row (int): Het rijnummer (0-index).
            col(int): Het kolomnummer (0-index). 

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

        if not self.coordinates or len(self.coordinates) != self.length: 
            return False
        for coord in self.coordinates:
            if coord not in hits: 
                return False
        return True
    
    def set_coordinates(self, coords):
        """
        Stel de coördinaten van het schip in.

        Argumenten: 
            coords (list): Lijst van alle (row, col)-paren met de exacte posities. 
        
        Raises: 
            ValueError: Als het aantal coördinaten niet overeenkomt met de lengte.
        """

        if len(coords) != self.length:
            raise ValueError("Aantal coördinaten komt niet overeen met de lengte van het schip.")
        self.coordinates = coords[:]

    def __repr__(self):
        """
        Geeft een tekstrepresentatie van het schip terug.

        Returns:
            str: een string met de lengte en de coördinaten. 
        """
    
        return f"Schip lengte = {self.length}\nSchip coördinaten = {self.coordinates}"