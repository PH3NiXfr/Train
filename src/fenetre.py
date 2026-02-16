from browser import document, window
from src import score as Score

class Fenetre:
    """
    Fenêtre de jeu
    """
    def __init__(self):
        self.main_canvas = None
        self.ctx = None
        self.interface_canvas = None
        self.interface_ctx = None
        self.screen_w = window.innerWidth
        self.screen_h = window.innerHeight
        self.score = Score.Score(self)
        self.outil = "ligne"
        self.menu = None
    
    def setup(self, menu):
        """
        Docstring for setup
        """
        self.menu = menu
        self.main_canvas = document["game"]
        self.main_canvas.style.background = "#00AA00"
        self.ctx = self.main_canvas.getContext("2d")

        self.resize()

    def resize(self):
        """
        Docstring for resize
        """
        ratio = window.devicePixelRatio or 1

        width = window.innerWidth
        height = window.innerHeight

        self.main_canvas.attrs["width"] = int(width * ratio)
        self.main_canvas.attrs["height"] = int(height * ratio)

        self.main_canvas.style.width = f"{width}px"
        self.main_canvas.style.height = f"{height}px"

        self.ctx.setTransform(ratio, 0, 0, ratio, 0, 0)