class Score:
    def __init__(self, fenetre):
        self.score = 100
        self.fenetre = fenetre
    def dessin(self):
        """
        Docstring for dessin
        """
        self.fenetre.ctx.save()

        self.fenetre.ctx.fillStyle = "#FFFFFF"
        self.fenetre.ctx.font = "24px Arial"
        self.fenetre.ctx.textAlign = "center"
        self.fenetre.ctx.textBaseline = "top"

        self.fenetre.ctx.fillText(f"{self.score} ¤", self.fenetre.main_canvas.width / 2, 5)

        self.fenetre.ctx.restore()