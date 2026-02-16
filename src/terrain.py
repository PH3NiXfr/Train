import random
from src.tuile import Tuile
from src.chemin import resolution
from src.train import Train

class Terrain:
    """
    Terrain de jeu
    """
    def __init__(self, fenetre_de_jeu):
        self.fenetre = fenetre_de_jeu
        self.taille_tuile = 20
        self.nb_tuile = round(max(fenetre_de_jeu.screen_w, fenetre_de_jeu.screen_h)/(self.taille_tuile*2))+1
        self.table_tuile = []
        self.table_chemin = []
        self.trains = []
        self.couleur_chemins = [(255,0,0), (0,255,0), (0,0,255)]
        self.nb_chemin_a = 0
        self.nb_chemin_b = 0
        self.nb_chemin_c = 0
        self.nb_ligne_a = 0
        self.nb_ligne_b = 0
        self.nb_ligne_c = 0
        self.mem_tuile = None
        self.n_couleur_chemin = 0
        self.nb_train_a = 0
        self.nb_train_b = 0
        self.nb_train_c = 0

    # Génère un terrain de tuiles avec des reliefs aléatoires
    def construction_terrain(self):
        """
        Docstring for constructionTerrain
        """
        # Création des tuiles dans une grille hexagonale
        for x in range(self.nb_tuile):
            for y in range(-int(x/2 + (x%2)/2), int(self.nb_tuile - x/2 + (x%2)/2)):
                px = x * (self.taille_tuile * 2)
                py = (y * (self.taille_tuile * 2)) + x * self.taille_tuile

                new_tuile = Tuile(self, x, y, px, py, 1)
                self.table_tuile.append(new_tuile)

        # Remplissage du relief jusqu'à obtenir un ratio de plaines acceptable
        racio_plaine = 0
        while racio_plaine < 60 or racio_plaine > 80:
            seeds = []
            # Ajout de montagnes
            for _ in range(round(self.nb_tuile/2)):  # zones de relief aléatoires
                seed_x = random.randint(0, self.nb_tuile-1)
                seed_y = random.randint(-int(seed_x/2), int(self.nb_tuile - seed_x/2))
                altitude = random.randint(180, 255)
                seeds.append((seed_x, seed_y, altitude))
            # Ajout de lacs
            for _ in range(round(self.nb_tuile/4)):  # lacs
                seed_x = random.randint(0, self.nb_tuile-1)
                seed_y = random.randint(-int(seed_x/2), int(self.nb_tuile - seed_x/2))
                altitude = random.randint(0, 50)
                seeds.append((seed_x, seed_y, altitude))
            # Application du bruit de hauteur à chaque tuile
            for tuile in self.table_tuile:
                valeur = 0
                total_poids = 0
                for sx, sy, alt in seeds:
                    d = self.distance_pos(tuile, (sx, sy))
                    # distance atténuée
                    poids = max(0.001, 1 / (d**2 + 1))
                    valeur += alt * poids
                    total_poids += poids
                # bruit local
                tuile.set_type(int(valeur / total_poids + random.randint(-5, 5)))
                # clamp
                tuile.set_type(max(0, min(255, tuile.hauteur)))

            # Vérification du ratio de plaines
            nombre_plaine = 0
            for tuile in self.table_tuile:
                if tuile.type_terrain == "plaine":
                    nombre_plaine += 1
            racio_plaine = (nombre_plaine/len(self.table_tuile))*100
        # Ajout de villes sur le terrain
        self.generer_villes(self.table_tuile,round(self.nb_tuile/2))

    # Calcule la distance entre une tuile et une position
    @staticmethod
    def distance_pos(t1, t2):
        """
        Docstring for distance

        :param t1: Tuile 1
        :param t2: Tuile 2
        """
        dx = t1.x - t2[0]
        dy = t1.y - t2[1]
        return (dx**2 + dy**2) ** 0.5
    
    # Place un certain nombre de villes sur des tuiles de type plaine
    @staticmethod
    def generer_villes(table_tuile, nb_ville):
        """
        Docstring for generer_villes
        
        :param table_tuile: Table des tuiles
        :param nb_ville: nombre de ville
        """
        for _ in range(nb_ville):
            ville = random.choice(table_tuile)
            while ville.solution != 0:
                ville = random.choice(table_tuile)
            ville.type_terrain = "ville"
            ville.solution = 0
            ville.couleur = (random.randint(175, 200), random.randint(175, 200), 0)
            ville.couleur_temp = ville.couleur

    def get_tuile(self, x, y):
        for tuile in self.table_tuile:
            if tuile.x == x and tuile.y == y:
                return tuile
        return Tuile(self, 1000,1000,1000,1000,100)
    
    def detection_tuile_clique(self, mx, my):
        for tuile in self.table_tuile:
            if tuile.collision(mx, my):
                if self.fenetre.outil == "ligne":
                    if self.mem_tuile is None:
                        self.mem_tuile = tuile
                        self.mem_tuile.couleur_temp = (self.mem_tuile.couleur_temp[0] + 20, self.mem_tuile.couleur_temp[1] + 20, self.mem_tuile.couleur_temp[2] + 20)
                    else:
                        self.mem_tuile.couleur_temp = self.mem_tuile.couleur
                        if tuile == self.mem_tuile:
                            # Suppression des chemins
                            for _ in range(len(tuile.chemins)):
                                # if tuile.chemins[0].couleur == self.couleur_chemins[0] and self.nb_chemin_a > 1:
                                #     Ecran.argent += round(len(tuile.chemins[0].tuiles) * round(self.nb_ligne_a*0.3))
                                # if tuile.chemins[0].couleur == self.couleur_chemins[1] and self.nb_chemin_b > 1:
                                #     Ecran.argent += round(len(tuile.chemins[0].tuiles) * round(self.nb_ligne_b*0.3))
                                # if tuile.chemins[0].couleur == self.couleur_chemins[2] and self.nb_chemin_b > 1:
                                #     Ecran.argent += round(len(tuile.chemins[0].tuiles) * round(self.nb_ligne_b*0.3))
                                self.table_chemin.remove(tuile.chemins[0])
                                if tuile.chemins[0].couleur == self.couleur_chemins[0]:
                                    self.nb_ligne_a -= len(tuile.chemins[0].tuiles)
                                    self.nb_chemin_a -= 1
                                if tuile.chemins[0].couleur == self.couleur_chemins[1]:
                                    self.nb_ligne_b -= len(tuile.chemins[0].tuiles)
                                    self.nb_chemin_b -= 1
                                if tuile.chemins[0].couleur == self.couleur_chemins[2]:
                                    self.nb_ligne_c -= len(tuile.chemins[0].tuiles)
                                    self.nb_chemin_c -= 1
                                tuile.chemins[0].suppr_chemin()
                        else:
                            # Création d’un nouveau chemin
                            nouveau_chemin, chemin_valide = resolution(self, tuile, self.mem_tuile, 1)
                            if nouveau_chemin != [] and chemin_valide:
                                self.table_chemin.append(nouveau_chemin)
                                if nouveau_chemin.couleur == self.couleur_chemins[0]:
                                    # Ecran.argent -= len(nouveau_chemin.tuiles) * round(self.nb_ligne_a*0.5)
                                    self.nb_ligne_a += len(nouveau_chemin.tuiles)
                                    self.nb_chemin_a += 1
                                if nouveau_chemin.couleur == self.couleur_chemins[1]:
                                    # Ecran.argent -= len(nouveau_chemin.tuiles) * round(self.nb_ligne_b*0.5)
                                    self.nb_ligne_b += len(nouveau_chemin.tuiles)
                                    self.nb_chemin_b += 1
                                if nouveau_chemin.couleur == self.couleur_chemins[2]:
                                    # Ecran.argent -= len(nouveau_chemin.tuiles) * round(self.nb_ligne_c*0.5)
                                    self.nb_ligne_c += len(nouveau_chemin.tuiles)
                                    self.nb_chemin_c += 1
                        self.mem_tuile = None
                    break
                elif self.fenetre.outil == "train":
                    # Ecran.prix = 0
                    # Si une tuile valide est sélectionnée pour poser un train
                    if len(tuile.chemins) > 0:
                        # if Ecran.argent >= len(Train.trains)*10:
                            chemins_possible = []
                            # Si il y a moins de trains que de tuile pour sur la ligne
                            for chemin in tuile.chemins:
                                if chemin.couleur == self.couleur_chemins[0]: # and self.nb_train_a < Tuile.nbVille[0]:
                                    chemins_possible.append(chemin)
                                if chemin.couleur == self.couleur_chemins[1]: # and self.nb_train_b < Tuile.nbVille[1]:
                                    chemins_possible.append(chemin)
                                if chemin.couleur == self.couleur_chemins[2]: # and self.nb_train_c < Tuile.nbVille[2]:
                                    chemins_possible.append(chemin)
                            # Choix du chemin aléatoire parmi les chemins possibles
                            if len(chemins_possible) != 0:
                                chemin_train = random.choice(chemins_possible)
                                # Ecran.argent -= len(Train.trains)*8
                                self.trains.append(Train(self, tuile, chemin_train))
                            # else:
                            #     # Notification si trop de trains sur la ligne
                            #     Notif.notifTropDeTrain.montrer = True
                        # else:
                        #     # Notification si pas assez d'argent pour poser un train
                        #     Notif.notifPasAssezArgent.montrer = True
                    self.fenetre.outil = "ligne"
                    for bouton in self.fenetre.menu.boutons:
                        if bouton.nom == "montagne":
                            bouton.activer = 0
    
    # Dessin du jeu
    def dessin(self):
        """
        Docstring for dessin
        """
        self.fenetre.ctx.clearRect(0, 0, self.fenetre.main_canvas.width, self.fenetre.main_canvas.height)
        for tuile in self.table_tuile:
            tuile.dessin()
        for chemin in self.table_chemin:
            chemin.dessin(self, self.table_chemin)
        for train in self.trains:
            train.dessin()
        self.fenetre.score.dessin()
        
