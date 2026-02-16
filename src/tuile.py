"""
Module définissant la classe Tuile et les constantes associées
à la génération du terrain.
"""

import random

# Constantes de configuration des types de terrain
TERRAIN_TYPES = ["plaine", "mer", "montagne"]

# Tableau global des tuiles du jeu
tableTuile = []

# Indicateurs de pose manuelle de reliefs
pose_mer = False
pose_plaine = False
pose_montagne = False

# Nombre de villes par type de chemin
nb_ville = [0, 0, 0]
nb_ville_totale_relier = 0


class Tuile:
    """
    Représente une tuile hexagonale du terrain.

    :param terrain: Instance du terrain contenant la tuile.
    :type terrain: Terrain
    :param x: Coordonnée axiale X.
    :type x: int
    :param y: Coordonnée axiale Y.
    :type y: int
    :param x_pos: Position X à l'écran.
    :type x_pos: float
    :param y_pos: Position Y à l'écran.
    :type y_pos: float
    :param hauteur: Valeur de hauteur utilisée pour déterminer le type de terrain.
    :type hauteur: float
    """

    def __init__(self, terrain, x, y, x_pos, y_pos, hauteur=0):
        """
        Initialise une tuile avec ses coordonnées et son type de terrain.
        """
        self.terrain = terrain
        self.x = x
        self.y = y
        self.z = x + y - 1

        self.x_pos = x_pos
        self.y_pos = y_pos

        self.centre = (
            self.x_pos + (terrain.taille_tuile / 3) * 2,
            self.y_pos + terrain.taille_tuile,
        )

        self.hauteur = hauteur
        self.test = 0

        if hauteur < 0.02:
            self.type_terrain = "mer"
            self.solution = 1000
            self.couleur = (50, 50, random.randint(150, 200))
        elif hauteur < 0.20:
            self.type_terrain = "plaine"
            self.solution = 0
            self.couleur = (50, random.randint(150, 175), 50)
        else:
            self.type_terrain = "montagnes"
            self.solution = 1000
            self.couleur = (random.randint(50, 100), 50, 0)

        self.couleur_temp = self.couleur

        self.verticle = [
            (x_pos, y_pos),
            (x_pos - (self.terrain.taille_tuile / 3) * 2, y_pos + self.terrain.taille_tuile),
            (x_pos, y_pos + self.terrain.taille_tuile * 2),
            (x_pos + (self.terrain.taille_tuile / 3) * 4, y_pos + self.terrain.taille_tuile * 2),
            (x_pos + (self.terrain.taille_tuile / 3) * 6, y_pos + self.terrain.taille_tuile),
            (x_pos + (self.terrain.taille_tuile / 3) * 4, y_pos),
        ]

        self.chemins = []

    def set_type(self, hauteur):
        """
        Met à jour le type de terrain en fonction d'une nouvelle hauteur.

        :param hauteur: Nouvelle valeur de hauteur.
        :type hauteur: float
        """
        self.hauteur = hauteur

        if hauteur < 100:
            self.type_terrain = "mer"
            self.solution = 1000
            self.couleur = (50, 50, 155 + hauteur)
        elif hauteur < 190:
            self.type_terrain = "plaine"
            self.solution = 0
            self.couleur = (50, 300 - hauteur, 50)
        else:
            self.type_terrain = "montagnes"
            self.solution = 1000
            self.couleur = (300 - hauteur, round(160 - hauteur / 2), 0)

        self.couleur_temp = self.couleur

    def distance_de(self, autre_tuile):
        """
        Calcule la distance hexagonale entre deux tuiles.

        :param autre_tuile: Tuile cible.
        :type autre_tuile: Tuile
        :return: Distance hexagonale.
        :rtype: float
        """
        return (
            abs(self.x - autre_tuile.x)
            + abs(self.y - autre_tuile.y)
            + abs(self.z - autre_tuile.z)
        ) / 2

    def test_tuile(self, solution_tuile_mere, table_tuile_a_traiter, table_tuile_traitee):
        """
        Teste la tuile pour une propagation de solution.

        :param solution_tuile_mere: Valeur de solution de la tuile mère.
        :type solution_tuile_mere: int
        :param table_tuile_a_traiter: Liste des tuiles à traiter.
        :type table_tuile_a_traiter: list
        :param table_tuile_traitee: Liste des tuiles déjà traitées.
        :type table_tuile_traitee: list
        :return: Tuple (état_modifié, table_tuile_a_traiter).
        :rtype: tuple
        """
        if self.solution == 0 and self.x != 1000:
            self.solution = solution_tuile_mere + 1
            table_tuile_a_traiter.insert(0, self)
            table_tuile_traitee.append(self)
            return True, table_tuile_a_traiter

        return False, table_tuile_a_traiter

    def collision(self, mx, my):
        """
        Détecte si un point est à l'intérieur de la tuile.

        :param mx: Coordonnée X du point.
        :type mx: float
        :param my: Coordonnée Y du point.
        :type my: float
        :return: True si le point est dans le polygone.
        :rtype: bool
        """
        inside = False
        n = len(self.verticle)

        for i in range(n):
            x1, y1 = self.verticle[i]
            x2, y2 = self.verticle[(i + 1) % n]

            if ((y1 > my) != (y2 > my)) and (
                mx < (x2 - x1) * (my - y1) / (y2 - y1 + 1e-9) + x1
            ):
                inside = not inside

        return inside

    def dessin(self):
        """
        Dessine la tuile sur le canvas.
        """
        fenetre = self.terrain.fenetre
        fenetre.ctx.save()

        fenetre.ctx.beginPath()
        fenetre.ctx.moveTo(self.verticle[0][0], self.verticle[0][1])

        for x, y in self.verticle[1:]:
            fenetre.ctx.lineTo(x, y)

        fenetre.ctx.closePath()

        fenetre.ctx.fillStyle = (
            f"#{format(self.couleur_temp[0], '02X')}"
            f"{format(self.couleur_temp[1], '02X')}"
            f"{format(self.couleur_temp[2], '02X')}"
        )
        fenetre.ctx.fill()

        fenetre.ctx.restore()
