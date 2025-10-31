# Zeeslag 
Welkom bij het spel **Zeeslag**! 
Dit is een digitale versie van het strategische Zeeslag bordspel.

De code is geschreven in **Python 3** met de python library **Tkinter** voor de Graphical User Interface. 

Om het spel te kunnen spelen run je het bestand `main.py`. 

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

## Custom mode
Tijdens het plaatsen van de shepen is er een knop **Instellingen** waar je twee instellingen kunt aanpassen:
- `Aantal schepen` - Pas aan hoeveel schepen iedere speler krijgt. 
- `Aantal shoten` - Pas het het aantal schoten aan dat elke speler per beurt krijgt voordat de beurt wisselt. 

Druk na het aanpassen op 'toepassen', dan start het spel met de nieuwe instellingen.
_Je kunt niet meer dan vijf schepen per speler hebben in de huidige code._

### Overige aanpassingen 
Overige aanpassingen die je kunt doen met uitleg over hoe je het aanpast:
- **Afbeelding aanpassen:** vervang de huidige png's in `/img` met andere png's met de afmetingen 64x64 (of groter), zorg er wel voor dat alle afbeeldingen dezelfde grootte hebben.
    __LET OP!__ Is je afbeelding groter dan 64x64, pas dan ook de variabele **CEL_GROOTE** aan naar de grootte van de afbeelding!

- **De kleuren van het schepen plaatsen:** pas in `place_ships.py` de HEX-codes van de de variabelen van **SCHEEPS_SPEC** aan.

- **Grootte van een schip aanpassen:** ga naar `ships.py` en pas het nummer dat voorin de haakjes staat aan, pas dit getal ook aan in `place_ships.py` bij **SCHEEPS_SPEC**.

- **Bord grootte aanpassen** ga naar `place_ships.py` & `spelboard.py` en pas daar de waarde van **BORD_GROOTTE** aan.
    __LET OP!__ Zorg er wel voor dat de 2 waardes gelijk zijn. Anders kun je schepen in de nieuwe vakjes niet raken!

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
