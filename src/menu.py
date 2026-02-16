"""
Module définissant le menu latéral du jeu et ses boutons.
"""

from browser import html
from browser import window


class Menu:
    """
    Représente le menu latéral interactif du jeu.

    :param fenetre: Instance de la fenêtre principale.
    :type fenetre: Fenetre
    """

    def __init__(self, fenetre):
        """
        Initialise le menu et ses composants graphiques.
        """
        self.fenetre = fenetre
        self.couleur_font = (50, 50, 50)
        self.ouvert = 1
        self.taille_icon = None
        self.pos_x_menu = None
        self.pos_icon = None
        self.icon_select = html.IMG(src="images/menu.png")
        self.boutons = []

        # Ajout des boutons du menu
        self.boutons.append(Bouton("montagne"))
        self.boutons.append(Bouton("plaine"))

        self.rezise()

    def rezise(self):
        """
        Met à jour les dimensions et positions du menu
        en fonction de la taille de la fenêtre.
        """
        if self.ouvert == 1:
            self.pos_x_menu = window.innerWidth
        else:
            self.pos_x_menu = window.innerWidth * 0.8

        self.taille_icon = max(
            window.innerWidth * 0.03,
            window.innerHeight * 0.03,
        )
        self.pos_icon = (self.pos_x_menu - self.taille_icon, 0)

        for bouton in self.boutons:
            bouton.taille = window.innerWidth * 0.08
            match bouton.nom:
                case "montagne":
                    bouton.pos = (
                        self.pos_x_menu + window.innerWidth * 0.06,
                        window.innerHeight * 0.2,
                    )
                case "plaine":
                    bouton.pos = (
                        self.pos_x_menu + window.innerWidth * 0.06,
                        window.innerHeight * 0.4,
                    )

    def detection_icon_clique(self, mx, my):
        """
        Détecte un clic sur l'icône du menu ou sur un bouton.

        :param mx: Position X de la souris.
        :type mx: float
        :param my: Position Y de la souris.
        :type my: float
        :return: True si un élément du menu a été cliqué.
        :rtype: bool
        """
        # Détection du clic sur l'icône du menu
        if (
            self.pos_icon[0] < mx < self.pos_icon[0] + self.taille_icon
            and self.pos_icon[1] < my < self.pos_icon[1] + self.taille_icon
        ):
            self.ouvert = 1 - self.ouvert
            self.rezise()
            return True

        # Détection du clic sur un bouton
        for bouton in self.boutons:
            if (
                bouton.pos[0] < mx < bouton.pos[0] + bouton.taille
                and bouton.pos[1] < my < bouton.pos[1] + bouton.taille
            ):
                match bouton.nom:
                    case "montagne":
                        bouton.activer = 1 - bouton.activer
                        self.fenetre.outil = "train" if bouton.activer == 1 else "ligne"
                    case "plaine":
                        if bouton.activer == 2:
                            bouton.activer = 0
                        else:
                            bouton.activer += 1
                        self.fenetre.terrain.n_couleur_chemin = bouton.activer
                return True

        return False

    def dessin(self):
        """
        Dessine le menu et ses boutons sur le canvas.
        """
        fenetre = self.fenetre
        fenetre.ctx.save()

        fenetre.ctx.fillStyle = (
            f"rgba({self.couleur_font[0]}, "
            f"{self.couleur_font[1]}, "
            f"{self.couleur_font[2]}, 0.5)"
        )

        fenetre.ctx.fillRect(
            self.pos_x_menu,
            0,
            window.innerWidth * 0.2,
            window.innerHeight,
        )

        fenetre.ctx.drawImage(
            self.icon_select,
            self.pos_icon[0],
            self.pos_icon[1],
            self.taille_icon,
            self.taille_icon,
        )

        for bouton in self.boutons:
            match bouton.nom:
                case "montagne":
                    if bouton.activer == 0:
                        fenetre.ctx.filter = "grayscale(100%)"
                    fenetre.ctx.drawImage(
                        bouton.image,
                        bouton.pos[0],
                        bouton.pos[1],
                        bouton.taille,
                        bouton.taille,
                    )
                    fenetre.ctx.filter = "none"
                case "plaine":
                    if bouton.activer == 0:
                        fenetre.ctx.filter = "grayscale(100%) sepia(100%) " \
                            "hue-rotate(-50deg) saturate(500%)"
                    elif bouton.activer == 1:
                        fenetre.ctx.filter = "grayscale(100%) sepia(100%) " \
                            "hue-rotate(60deg) saturate(500%)"
                    elif bouton.activer == 2:
                        fenetre.ctx.filter = "grayscale(100%) sepia(100%) " \
                            "hue-rotate(180deg) saturate(500%)"
                    fenetre.ctx.drawImage(
                        bouton.image,
                        bouton.pos[0],
                        bouton.pos[1],
                        bouton.taille,
                        bouton.taille
                    )
                    fenetre.ctx.filter = "none"

        fenetre.ctx.restore()


class Bouton:
    """
    Représente un bouton du menu latéral.

    :param nom: Nom du bouton (utilisé pour charger l'image).
    :type nom: str
    """

    def __init__(self, nom):
        """
        Initialise un bouton avec son image associée.
        """
        self.nom = nom
        self.image = html.IMG(src=f"images/{self.nom}.png")
        self.taille = None
        self.pos = None
        self.activer = 0
