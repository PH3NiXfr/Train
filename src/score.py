"""
Module définissant la gestion et l'affichage du score.
"""


class Score:
    """
    Représente le score du joueur.

    :param fenetre: Instance de la fenêtre principale.
    :type fenetre: Fenetre
    """

    def __init__(self, fenetre):
        """
        Initialise le score avec une valeur par défaut.
        """
        self.score = 100
        self.fenetre = fenetre

    def dessin(self):
        """
        Affiche le score courant en haut de l'écran.
        """
        self.fenetre.ctx.save()

        self.fenetre.ctx.fillStyle = "#FFFFFF"
        self.fenetre.ctx.font = "24px Arial"
        self.fenetre.ctx.textAlign = "center"
        self.fenetre.ctx.textBaseline = "top"

        self.fenetre.ctx.fillText(
            f"{self.score} ¤",
            self.fenetre.main_canvas.width / 2,
            5,
        )

        self.fenetre.ctx.restore()
