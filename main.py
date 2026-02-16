from src import fenetre
from src import menu
from src import terrain
from src import evenement
from browser import timer
from browser import window
from browser import bind

# Création de la fenetre
fenetreDeJeu = fenetre.Fenetre()
# Menu
menuDeJeu = menu.Menu(fenetreDeJeu)

fenetreDeJeu.setup(menuDeJeu)

# Création des éléments du jeu
terrain_de_jeu = terrain.Terrain(fenetreDeJeu)

# Réinitailisation du jeu
def nouvelle_partie():
    """
    Lancement d'une nouvelle partie
    """
    # recréation du terrain
    terrain_de_jeu.construction_terrain()
    # recréation des événement
    evenement.creer_evenement(terrain_de_jeu, fenetreDeJeu, menuDeJeu)

# Fonction globale appelée en thread pour faire bouger tous les trains
def mouvement_des_trains(timestamp):
    for train in terrain_de_jeu.trains:
        train.mouvement()
    window.requestAnimationFrame(mouvement_des_trains)

nouvelle_partie()
window.requestAnimationFrame(mouvement_des_trains)

def boucle_de_jeu():
    """
    Boucle principale du jeu
    """
    terrain_de_jeu.dessin()
    menuDeJeu.dessin()

# Mise à jour automatique quand on change la taille
@bind(window, "resize")
def on_resize(_):
    "Redimentionnement de la fenêtre"
    fenetreDeJeu.resize()
    menuDeJeu.rezise()

# Boucle du jeu (60 fps)
timer.set_interval(boucle_de_jeu, 1000//60)
