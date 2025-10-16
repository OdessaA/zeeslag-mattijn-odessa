#Place_Ships
'''
Zorgt ervoor dat er een boot geplaatst kan worden op een makkelijke manier

Gemaakt door:   Mattijn Thijert
                Odessa Al-Dib
'''
#---------------------------------------------------------------------------------
"""n.v.t"""
#---------------------------------------------------------------------------------
import tkinter as tk
from tkinter import messagebox
from ships import Patrouilleschip, Onderzeeër, Torpedobootjager, Slagschip, Vliegdekschip
import os, importlib.util, inspect, traceback
from spelboard import ZeeslagGUI

#--------------------------------------------------------------------------------------------------

BORD_GROOTTE = 10
CEL_GROOTTE = 64
BORD_PIXELS = BORD_GROOTTE * CEL_GROOTTE

SCHEEPS_SPEC = [
    ("Vliegdekschip",   Vliegdekschip,    5, "#4c1d95"),
    ("Slagschip",       Slagschip,        4, "#c14a09"),
    ("Onderzeeër",      Onderzeeër,       3, "#374151"),
    ("Torpedojager",    Torpedobootjager, 3, "#B91C1C"),
    ("Patrouilleschip", Patrouilleschip,  2, "#59a14f"),
]

# maak een toegang tot de map met de pixelarts
IMG_PAD = os.path.join(os.path.dirname(__file__), 'img')


class PlaatsingsUI(tk.Frame):
    def __init__(self, master):
        super().__init__(master); self.grid(sticky="nsew")
        master.title("Zeeslag – Plaats je vloot")

        # status
        self.orientatie = tk.StringVar(value="H")     # "H" of "V"
        self.geselecteerde_sleutel = None             # key van gekozen schip
        self.bezet = [[None]*BORD_GROOTTE for _ in range(BORD_GROOTTE)]  # raster met keys of None

        # schepen: sleutel -> dict
        self.schepen = {
            naam: {"naam": naam, "klasse": cls, "lengte": lengte, "kleur": kleur,
                "coordinaten": [], "geplaatst": False, "knop": None}
            for naam, cls, lengte, kleur in SCHEEPS_SPEC
        }

        # assets (zorg dat IMG_PAD en CEL_GROOTTE kloppen; bij voorkeur CEL_GROOTTE=64)
        self.img_unknown = tk.PhotoImage(file=os.path.join(IMG_PAD, "Battleship_miss64.png"))
        self._tile_images = []  # optioneel; self.img_unknown vasthouden is in principe genoeg

        # layout
        paneel_links  = tk.Frame(self); paneel_links.grid(row=0, column=0, padx=8, pady=8, sticky="ns")
        paneel_rechts = tk.Frame(self); paneel_rechts.grid(row=0, column=1, padx=8, pady=8, sticky="nsew")

        # palet
        palet = tk.LabelFrame(paneel_links, text="Kies een schip en klik op het bord"); palet.pack(fill="x")
        for sleutel, schip in self.schepen.items():
            schip["knop"] = tk.Button(
                palet, text=f"{schip['naam']} ({schip['lengte']})",
                bg=schip["kleur"], fg="white", activebackground={ "activebackground": schip["kleur"] }.get("activebackground", schip["kleur"]),
                command=lambda s=sleutel: self._selecteer_schip(s)
            )
            schip["knop"].pack(fill="x", pady=3)

        # oriëntatie
        orbox = tk.LabelFrame(paneel_links, text="Oriëntatie"); orbox.pack(fill="x", pady=(6,0))
        tk.Radiobutton(orbox, text="Horizontaal", variable=self.orientatie, value="H").grid(row=0, column=0, padx=6, pady=4, sticky="w")
        tk.Radiobutton(orbox, text="Verticaal",   variable=self.orientatie, value="V").grid(row=0, column=1, padx=6, pady=4, sticky="w")
        tk.Label(orbox, text="Tip: druk 'r' om te roteren", fg="#666").grid(row=1, column=0, columnspan=2, padx=6, sticky="w")

        # actiebalk (links)
        actiebalk = tk.Frame(paneel_links); actiebalk.pack(fill="x", pady=(8, 0))

        links = tk.Frame(actiebalk); links.pack(side="left")
        # Wisknop
        tk.Button(links, text="Alles wissen", command=self._reset_alle_schepen).pack(anchor="w")
        
        # Helpknop
        tk.Button(links, text="Help", width=9, command=self.toon_help).pack(anchor="w", pady=(4, 0))

        tk.Frame(actiebalk).pack(side="left", expand=True, fill="x")  # spacer
        self.start_knop = tk.Button(actiebalk, text="Start spel", state="disabled", command=self._start_spel)
        self.start_knop.pack(side="right")

        # bord (tegelafbeeldingen i.p.v. witte achtergrond)
        self.canvas = tk.Canvas(paneel_rechts, width=BORD_PIXELS, height=BORD_PIXELS, highlightthickness=0)
        self.canvas.pack()

        # Leg per cel een tegel neer + dun grid erbovenop
        self.cell_items = {}  # (r,c) -> canvas item id van de tegel
        for r in range(BORD_GROOTTE):
            for c in range(BORD_GROOTTE):
                x0 = c * CEL_GROOTTE
                y0 = r * CEL_GROOTTE

                # tegel als onderlaag
                img_id = self.canvas.create_image(
                    x0, y0,
                    image=self.img_unknown,
                    anchor="nw",
                    tags=("cell", f"r{r}c{c}", "tile"),
                )
                self.cell_items[(r, c)] = img_id

                # subtiele gridlijn
                self.canvas.create_rectangle(
                    x0, y0, x0 + CEL_GROOTTE, y0 + CEL_GROOTTE,
                    outline="#cccccc", width=1, tags=("grid",)
                )

        # zorg dat de tegel onder de grid ligt (netter)
        self.canvas.tag_lower("tile", "grid")

        # events
        # Als je de handlers al had, laat dit zo. We rekenen (r,c) uit op basis van muispositie.
        self.canvas.bind("<Motion>", self._muis_beweging)
        self.canvas.bind("<Leave>", lambda e: self.canvas.delete("preview"))
        self.canvas.bind("<Button-1>", self._linker_klik)
        self.canvas.bind("<Button-3>", self._rechter_klik)
        master.bind("r", lambda e: self.orientatie.set("V" if self.orientatie.get()=="H" else "H"))

    # ---------- helpers ----------
    def _selecteer_schip(self, sleutel):
        if self.schepen[sleutel]["geplaatst"]:
            return
        self.geselecteerde_sleutel = sleutel
        for k, schip in self.schepen.items():
            schip["knop"].config(relief=("sunken" if k == sleutel else "raised"))

    def _binnen_bord(self, rij, kol): 
        return 0 <= rij < BORD_GROOTTE and 0 <= kol < BORD_GROOTTE

    def _voetafdruk(self, rij, kol, lengte, orient):
        return ([(rij, kol+i) for i in range(lengte)] if orient == "H"
                else [(rij+i, kol) for i in range(lengte)])

    def _plek_vrij(self, coords):
        return all(self._binnen_bord(r, c) and self.bezet[r][c] is None for r, c in coords)

    def _teken_cel(self, rij, kol, **kwargs):
        x0, y0 = kol*CEL_GROOTTE+1, rij*CEL_GROOTTE+1
        x1, y1 = x0+CEL_GROOTTE-2, y0+CEL_GROOTTE-2
        return self.canvas.create_rectangle(x0, y0, x1, y1, **kwargs)

    # ---------- interactie ----------
    def _muis_beweging(self, e):
        self.canvas.delete("preview")
        if not self.geselecteerde_sleutel:
            return
        rij, kol = e.y // CEL_GROOTTE, e.x // CEL_GROOTTE
        schip = self.schepen[self.geselecteerde_sleutel]
        coords = self._voetafdruk(rij, kol, schip["lengte"], self.orientatie.get())
        toegestaan = self._plek_vrij(coords)
        for r, c in coords:
            if self._binnen_bord(r, c):
                self._teken_cel(r, c, outline=("#2a2" if toegestaan else "#a22"),
                                width=2, fill="", tags="preview")

    def _linker_klik(self, e):
        if not self.geselecteerde_sleutel:
            messagebox.showinfo("Kies schip", "Selecteer eerst een schip links."); return
        rij, kol = e.y // CEL_GROOTTE, e.x // CEL_GROOTTE
        schip = self.schepen[self.geselecteerde_sleutel]
        coords = self._voetafdruk(rij, kol, schip["lengte"], self.orientatie.get())
        if not self._plek_vrij(coords):
            self.master.bell(); return

        tag = f"schip_{self.geselecteerde_sleutel}"
        for r, c in coords:
            self.bezet[r][c] = self.geselecteerde_sleutel
            self._teken_cel(r, c, fill=schip["kleur"], width=0, tags=("ship", tag))
        schip["coordinaten"], schip["geplaatst"] = coords, True
        schip["knop"].config(state="disabled", relief="raised")
        self.geselecteerde_sleutel = None
        self.canvas.delete("preview")
        self._update_start_knop()

    def _rechter_klik(self, e):
        rij, kol = e.y // CEL_GROOTTE, e.x // CEL_GROOTTE
        if not self._binnen_bord(rij, kol): 
            return
        sleutel = self.bezet[rij][kol]
        if sleutel is None:
            return
        schip = self.schepen[sleutel]
        for r, c in schip["coordinaten"]:
            self.bezet[r][c] = None
        self.canvas.delete(f"schip_{sleutel}")
        schip["coordinaten"], schip["geplaatst"] = [], False
        schip["knop"].config(state="normal")
        self._update_start_knop()

    def _reset_alle_schepen(self):
        for schip in self.schepen.values():
            schip["coordinaten"] = []
            schip["geplaatst"] = False
            schip["knop"].config(state="normal", relief="raised")
        for r in range(BORD_GROOTTE):
            for c in range(BORD_GROOTTE):
                self.bezet[r][c] = None
        self.geselecteerde_sleutel = None
        self.canvas.delete("ship"); self.canvas.delete("preview")
        self._update_start_knop()

    def _alle_geplaatst(self):
        return all(s["geplaatst"] for s in self.schepen.values())

    def _update_start_knop(self):
        self.start_knop.config(state=("normal" if self._alle_geplaatst() else "disabled"))

    def _start_spel(self):
        # Check: zijn alle schepen geplaatst?
        if not self._alle_geplaatst():
            messagebox.showinfo("Nog niet klaar", "Plaats eerst alle schepen.")
            return

        # Vloot bouwen
        vloot = []
        for schip in self.schepen.values():
            inst = schip["klasse"]()
            inst.set_coordinates(schip["coordinaten"])
            vloot.append(inst)

        # Debug: laat zien wat we doorgeven
        print(">>> VLOOT:", [(s.name, list(s.coordinates)) for s in vloot], flush=True)

        # Maak het spelvenster en bewaar referentie, anders kan het object GC'ed worden
        top = tk.Toplevel(self.master)
        top.title("Zeeslag")
        self.game = ZeeslagGUI(top, ships=vloot)   # <- REFERENTIE BEWAREN!

        # (pas na succesvol aanmaken verbergen we de plaats-UI)
        self.master.withdraw()





    def toon_help(self):
        messagebox.showinfo("Help", "Klik op een vakje om te schieten.")


if __name__ == "__main__":
    root = tk.Tk()
    PlaatsingsUI(root)
    root.mainloop()
