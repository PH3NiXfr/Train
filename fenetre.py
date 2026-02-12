from browser import document, window

class Fenetre:
    """
    Fenêtre de jeu
    """
    def __init__(self):
        self.canvas = None
        self.ctx = None
        self.screen_w = window.innerWidth
        self.screen_h = window.innerHeight
    
    def setup(self):
        """
        Docstring for setup
        """
        self.canvas = document["game"]
        self.canvas.style.background = "#00FF00"
        self.ctx = self.canvas.getContext("2d")
        self.resize()

    # Choisir un ratio fixe
    def resize(self):
        """
        Docstring for resize
        """
        ratio = window.devicePixelRatio or 1

        width = window.innerWidth
        height = window.innerHeight

        self.canvas.attrs["width"] = int(width * ratio)
        self.canvas.attrs["height"] = int(height * ratio)

        self.canvas.style.width = f"{width}px"
        self.canvas.style.height = f"{height}px"

        self.ctx.setTransform(ratio, 0, 0, ratio, 0, 0)