# Zeeslag 
Welkom bij het spel **Zeeslag**! 
Dit is een digitale versie van het strategische Zeeslag bordspel.

De code is geschreven in **Python 3** met de python library **Tkinter** voor de Graphical User Interface. 

## Spelbeschrijving 

Onze versie van zeeslag speel je met twee spelers die het tegen elkaar opnemen. 

Eerst plaatst iedere speler zijn vloot, met 5 schepen van verschillende lengtes, op hun eigen **10 x 10** spelbord. 

Wanneer de vloten zijn geplaatst begint het zeeslag spel, waarbij de spelers **om de beurt** schieten op het bord van de tegenstander. 

Je wint het spel wanneer je **alle vakjes van de vijandelijke schepen** hebt geraakt voordat jouw eigen vloot gezonken is.

## De schepen 

| Schip              | Lengte | Kleur   |
|--------------------|--------|----------|
| Vliegdekschip      | 5 vakjes | Paars |
| Slagschip          | 4 vakjes | Rood |
| Onderzeeër         | 3 vakjes | Grijs |
| Torpedobootjager   | 3 vakjes | Oranje |
| Patrouilleschip    | 2 vakjes | Groen |

Er zijn 5 soorten schepen. 
Standaard heeft elke speler 5 schepen, dit kan aangepast worden (zie custom mode). 
Ieder schip heeft zijn eigen naam, lengte en kleur. 
Iedere speler zet elk schip één keer op zijn bord. 

Hoe groter het schip, hoe makkelijker het te raken is - dus verstop ze goed! 

## Besturing 

**Plaatsen van schepen** 
- Klik met de **linkermuisknop** op een schip uit de lijst links om een schip te selecteren. 
- Klik vervolgens met de **linkermuisknop** op het bord om het schip te plaatsen.  
- Klik met de **rechtermuisknop** om een schip te verwijderen.  
- Druk op de **R-toets** op je toetsenbord om de oriëntatie te draaien (horizontaal of verticaal).  
- Zodra alle schepen geplaatst zijn, wordt de knop **“Start spel”** actief. 

**Tijdens het spel**
- Klik op een vakje om te schieten.  
- Je ziet meteen of je schot raak of mis was boven in het scherm. 
- Na elke beurt verschijnt een **wisselscherm** zodat spelers eerlijk kunnen afwisselen.

**Custom mode**
Tijdens het plaatsen van de schepen is er een knop **Instellingen** waarmee je twee instellingen kunt aanpassen:
- `Aantal schepen` - Pas aan hoeveel schepen elke speler krijgt. 
- `Aantal shoten` - Pas het aantal schoten aan dat je per beurt hebt voordat de beurten wisselen. 

Een aantal andere aanpassingen die je kunt doen met uitleg over hoe je het aanpast:
- Afbeelding aanpassen, vervang de image in `/img` de huidige png's met andere png's met afmetingen 64x64 (of groter), zorg wel dat alle afbeeldingen dezelfde grootte hebben.
    LET OP! Is je afbeelding groter dan 64x64. Pas dan ook de variabele **BORD_GROOTE** (hoe groot het speelscherm is) aan naar de grootte van de afbeelding.
- De kleuren van het schepen plaatsen, pas in `place_ships.py` de HEX-codes van de de variabelen in **SCHEEPS_SPES** aan.
- 

## Modules 
  - `main.py` – start het spel  
  - `place_ships.py` – plaatsen van schepen  
  - `players.py` – spelerlogica  
  - `ships.py` – definities van schepen  
  - `spelboard.py` – spelbord en beurtwisseling  

Afbeeldingen voor de tegels en schepen staan in de map **`/img`**.

## Samenvatting project 
In ons project maken we gebruik van **object oriented programming (OOP)**, **Graphical User Interface (GUI)** en verschillende modules. 

## Makers 
**Gemaakt door:**  
Odessa Al-Dib & Mattijn Thijert  
Vak: *Inleiding programmeren – Eindopdracht*
