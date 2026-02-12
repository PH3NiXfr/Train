from browser import timer
from browser import window
from browser import bind
import fenetre
import terrain

# Création de la fenetre
fenetreDeJeu = fenetre.Fenetre()
fenetreDeJeu.setup()

# Création des éléments du jeu
terrain_de_jeu = terrain.Terrain(fenetreDeJeu)

# Réinitailisation du jeu
def nouvelle_partie():
    """
    Lancement d'une nouvelle partie
    """
    # recréation du terrain
    terrain_de_jeu.construction_terrain()

nouvelle_partie()

def boucle_de_jeu():
    """
    Boucle principale du jeu
    """
    terrain_de_jeu.dessin()

# Mise à jour automatique quand on change la taille
@bind(window, "resize")
def on_resize(_):
    "Redimentionnement de la fenêtre"
    fenetreDeJeu.resize()

# Boucle du jeu (60 fps)
timer.set_interval(boucle_de_jeu, 1000//60)
