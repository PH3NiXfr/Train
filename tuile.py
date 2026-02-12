import random

# Constantes de configuration
TERRAIN_TYPES = ["plaine", "mer", "montagne"]
# Tableau global des tuiles du jeu
tableTuile = []
# Indicateurs de pose manuelle de reliefs
pose_mer = False
pose_plaine = False
pose_montagne = False
# Nombre de villes par type de chemin
nb_ville = [0,0,0]
nb_ville_totale_relier = 0
# Classe représentant une tuile hexagonale
class Tuile:
    """
    Docstring for Tuile
    """
    def __init__(self, terrain, x, y, x_pos, y_pos, hauteur = 0):
        self.terrain = terrain
        self.x = x
        self.y = y
        self.z = x+y-1
        self.x_pos = x_pos
        self.y_pos = y_pos
        # Coordonnées du centre de la tuile pour la sélection souris
        self.centre = (self.x_pos+(terrain.taille_tuile/3)*2,self.y_pos+terrain.taille_tuile)
        self.hauteur = hauteur
        self.test = 0
        # Attribution du type de terrain en fonction de la hauteur
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
        # Couleur temporaire utilisée pour l'affichage
        self.couleur_temp = self.couleur
        # Forme hexagonale représentée par ses 6 sommets
        self.verticle = [
            (x_pos, y_pos),
            (x_pos - (self.terrain.taille_tuile/3)*2, y_pos + self.terrain.taille_tuile),
            (x_pos, y_pos + self.terrain.taille_tuile*2),
            (x_pos + (self.terrain.taille_tuile/3)*4, y_pos + self.terrain.taille_tuile*2),
            (x_pos + (self.terrain.taille_tuile/3)*6, y_pos + self.terrain.taille_tuile),
            (x_pos + (self.terrain.taille_tuile/3)*4, y_pos)
        ]
        # Liste des chemins qui passent par cette tuile
        self.chemins = []
    # Mise à jour du type de terrain en fonction d'une nouvelle hauteur
    def set_type(self,hauteur):
        """
        Docstring for set_type
        
        :param hauteur: Description
        """
        self.hauteur = hauteur
        if hauteur < 100:
            self.type_terrain = "mer"
            self.solution = 1000
            self.couleur = (50, 50, 155+hauteur)
        elif hauteur < 190:
            self.type_terrain = "plaine"
            self.solution = 0
            self.couleur = (50, 300-hauteur, 50)
        else:
            self.type_terrain = "montagnes"
            self.solution = 1000
            self.couleur = (300-hauteur, round(160-hauteur/2), 0)
        # DEBUG CONSTRUCTION TERRAIN
        # self.couleur = (int(hauteur),int(hauteur),int(hauteur))
        self.couleur_temp = self.couleur
    # Distance hexagonale entre deux tuiles
    def distance_de(self,autre_tuile):
        """
        Docstring for distance_de
        
        :param autre_tuile: Description
        """
        return (abs(self.x-autre_tuile.x)+abs(self.y-autre_tuile.y)+abs(self.z-autre_tuile.z))/2

    # Dessin d'une tuile
    def dessin(self):
        """
        Docstring for dessin
        """
        fenetre = self.terrain.fenetre
        fenetre.ctx.save()

        fenetre.ctx.beginPath()
        fenetre.ctx.moveTo(self.verticle[0][0], self.verticle[0][1])
        for x, y in self.verticle[1:]:
            fenetre.ctx.lineTo(x, y)
        fenetre.ctx.closePath()

        fenetre.ctx.fillStyle = (
            f"#{format(self.couleur[0], '02X')}"
            f"{format(self.couleur[1], '02X')}"
            f"{format(self.couleur[2], '02X')}"
        )
        fenetre.ctx.fill()

        fenetre.ctx.restore()
        