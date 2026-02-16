"""
Module définissant la fenêtre principale du jeu.
"""

from browser import document
from browser import window
from src import score as Score


class Fenetre:
    """
    Représente la fenêtre principale du jeu et gère le canvas.

    Cette classe encapsule la gestion du canvas HTML, du contexte
    de dessin et des paramètres d'affichage.
    """

    def __init__(self):
        """
        Initialise les attributs principaux de la fenêtre.
        """
        self.main_canvas = None
        self.ctx = None
        self.interface_canvas = None
        self.interface_ctx = None
        self.screen_w = window.innerWidth
        self.screen_h = window.innerHeight
        self.score = Score.Score(self)
        self.outil = "ligne"
        self.menu = None
        self.terrain = None

    def setup(self, menu, terrain):
        """
        Configure le canvas principal et associe le menu.

        :param menu: Instance du menu principal.
        :type menu: Menu
        """
        self.menu = menu
        self.terrain = terrain
        self.main_canvas = document["game"]
        self.main_canvas.style.background = "#00AA00"
        self.ctx = self.main_canvas.getContext("2d")

        self.resize()

    def resize(self):
        """
        Adapte la taille du canvas à la fenêtre du navigateur.

        Cette méthode applique également le device pixel ratio
        afin d'assurer un rendu net sur les écrans haute densité.
        """
        ratio = window.devicePixelRatio or 1

        width = window.innerWidth
        height = window.innerHeight

        self.main_canvas.attrs["width"] = int(width * ratio)
        self.main_canvas.attrs["height"] = int(height * ratio)

        self.main_canvas.style.width = f"{width}px"
        self.main_canvas.style.height = f"{height}px"

        self.ctx.setTransform(ratio, 0, 0, ratio, 0, 0)
