"""
Module principal du jeu.

Ce module initialise la fenêtre, le menu et le terrain,
puis lance la boucle principale ainsi que l'animation des trains.
"""

from src.fenetre import Fenetre
from src.menu import Menu
from src.terrain import Terrain
from src.evenement import creer_evenement
from browser import timer
from browser import window
from browser import bind
f = Fenetre()
print(f)

# Création de la fenêtre principale du jeu
fenetreDeJeu = Fenetre()

# Création du menu principal
menuDeJeu = Menu(fenetreDeJeu)

# Création du terrain de jeu
terrain_de_jeu = Terrain(fenetreDeJeu)

# Initialisation de la fenêtre avec le menu
fenetreDeJeu.setup(menuDeJeu, terrain_de_jeu)

def nouvelle_partie():
    """
    Démarre une nouvelle partie.

    Cette fonction reconstruit le terrain et recrée
    les événements associés au jeu.
    """
    # Recréation du terrain
    terrain_de_jeu.construction_terrain()

    # Recréation des événements
    creer_evenement(terrain_de_jeu, fenetreDeJeu, menuDeJeu)


def mouvement_des_trains(timestamp):
    """
    Met à jour le mouvement de tous les trains.

    Cette fonction est appelée via requestAnimationFrame
    afin d'assurer une animation fluide.

    :param timestamp: Horodatage fourni par le navigateur.
    :type timestamp: float
    """
    for train in terrain_de_jeu.trains:
        train.mouvement()

    window.requestAnimationFrame(mouvement_des_trains)


def boucle_de_jeu():
    """
    Boucle principale du jeu.

    Cette fonction met à jour l'affichage du terrain
    et du menu à une fréquence régulière.
    """
    terrain_de_jeu.dessin()
    menuDeJeu.dessin()


@bind(window, "resize")
def on_resize(_event):
    """
    Gère le redimensionnement de la fenêtre.

    :param _event: Événement de redimensionnement (non utilisé).
    """
    fenetreDeJeu.resize()
    menuDeJeu.rezise()


# Initialisation d'une nouvelle partie
nouvelle_partie()

# Lancement de l'animation des trains
window.requestAnimationFrame(mouvement_des_trains)

# Lancement de la boucle principale (60 FPS)
timer.set_interval(boucle_de_jeu, 1000 // 60)