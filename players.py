""" 
players.py bevat de Player class.
Deze class verwerkt aanvallen en checkt of alle schepen al gezonken zijn. 

Elke speler heeft: 
    - Een naam.
    - Een lijst met schepen.
    - Een verzameling coördinaten van hits en misses.
    
    Gemaakt door:   Odessa Al-Dib

    kleine aanpassing: Mattijn Thijert
"""
#---------------------------------------------------------------------------------
"""n.v.t"""
#---------------------------------------------------------------------------------

class Player:
    def __init__(self, name, ships=None):
        self.name = name
        self.schepen = list(ships or [])
        self.hits = set()    # Coordinaten waar de speler geraakt is. (set want dat voorkomt dubbele waardes)
        self.misses = set()  # Coordinaten waar de speler miste 
        self.tried = set()   # <- voeg toe: alle geschoten coördinaten (voor UI)

    def set_ships(self, ships):
        self.schepen = list(ships or [])

    def ontvang_aanval(self, coord): # Het is precies dezelfde aanval functie, alleen dwe niet meer op ships.py maar op spelboard.py
        """Verwerk aanval op deze speler (coördinaat is (r,c)).
           Return: "Raak!", of "Gezonken! <naam>", of "Mis!"
        """
        row, col = coord
        for schip in self.schepen:
            if schip.occupies(row, col):
                self.hits.add(coord)
                if schip.is_sunk(self.hits):
                    return f"Gezonken! {schip.name}" # "Gezonken!" als het schip volledig gezonken is. 
                return "Raak!" # "raak" als er een schip geraakt is maar nog niet gezonken is. 
        self.misses.add(coord)
        return "Mis!" # "Mis" als er geen schip op de plek ligt waar er aangevallen is.

    def alle_schepen_gezonken(self): # De functie is wat ingekort om de check een stukje makkelijk te maken
        return all(s.is_sunk(self.hits) for s in self.schepen) # check kort en snel of er nog een schip uit de lijst overeindstaat
