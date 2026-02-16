import random

# Classe représentant un train individuel
class Train:
    def __init__(self, terrain, tuile, chemin):
        # La tuile de départ du train
        self.tuile = tuile
        # Chemin du train
        self.chemin = chemin
        self.terrain = terrain
        # Decompte du nombre de trains de chaque ligne
        if chemin.couleur == self.terrain.couleur_chemins[0]:
            terrain.nb_train_a += 1
        elif chemin.couleur == self.terrain.couleur_chemins[1]:
            terrain.nb_train_b += 1
        elif chemin.couleur == self.terrain.couleur_chemins[2]:
            terrain.nb_train_c += 1
        # Définition des couleurs du train
        self.couleur = (max(0,self.chemin.couleur[0]-100), max(0,self.chemin.couleur[1]-100), max(0,self.chemin.couleur[2]-50))
        self.couleur_ligne = self.chemin.couleur
        # Direction de parcours du chemin
        self.direction = 1
        # Détermine la prochaine tuile à atteindre
        self.next_tuile = self.chemin.get_next_tuile(self)
        # Position actuelle sur l’écran
        self.x = tuile.centre[0]
        self.y = tuile.centre[1]
        # Temps d'arrêt restant
        self.arret = 0
        # Nombre de déplacements entre 2 villes
        self.nb_deplacements = 0
    # Gère le déplacement du train vers la prochaine tuile
    def mouvement(self):
        if self.arret > 0:
            # Si le train est à l'arrêt, on décrémente le timer
            self.arret -= 1
        else:
            # Attendre si un train est déjà sur la prochaine tuile de type ville
            attendre = False
            for train in self.terrain.trains:
                if train != self and train.tuile == self.next_tuile and train.tuile.type_terrain == "ville" and self.tuile.type_terrain != "ville" and train.couleur_ligne == self.couleur_ligne:
                    attendre = True
            if not attendre:
                # Mouvement du train pixel par pixel vers la tuile cible
                if self.x < self.next_tuile.centre[0] and self.x+2 < self.next_tuile.centre[0]:
                    if self.y < self.next_tuile.centre[1] and self.y+2 < self.next_tuile.centre[1]:
                        self.x += 2
                        self.y += 1
                    elif self.y > self.next_tuile.centre[1] and self.y-2 > self.next_tuile.centre[1]:
                        self.x += 2
                        self.y -= 1
                    else:
                        self.x += 2
                elif self.x > self.next_tuile.centre[0] and self.x-2 > self.next_tuile.centre[0]:
                    if self.y < self.next_tuile.centre[1] and self.y+2 < self.next_tuile.centre[1]:
                        self.x -= 2
                        self.y += 1
                    elif self.y > self.next_tuile.centre[1] and self.y-2 > self.next_tuile.centre[1]:
                        self.x -= 2
                        self.y -= 1
                    else:
                        self.x -= 2
                elif self.y < self.next_tuile.centre[1] and self.y+2 < self.next_tuile.centre[1]:
                    self.y += 2
                elif self.y > self.next_tuile.centre[1] and self.y-2 > self.next_tuile.centre[1]:
                    self.y -= 2
                # Si le train est proche de la prochaine tuile, on la rejoint
                if abs(self.x - self.next_tuile.centre[0]) < 4 and abs(self.y - self.next_tuile.centre[1]) < 4:
                    self.changer_tuile()
    
    # Fonction appelée lorsque le train atteint une tuile cible
    def changer_tuile(self):
        # Calcule le vecteur de déplacement entre les deux dernières tuiles
        transorfmation_x = self.next_tuile.x-self.tuile.x
        transorfmation_y = self.next_tuile.y-self.tuile.y
        transorfmation_z = self.next_tuile.z-self.tuile.z
        # Coordonnées théoriques de la tuile dans la continuité du déplacement
        pos_tuile_oposee = [self.next_tuile.x + transorfmation_x,self.next_tuile.y + transorfmation_y,self.next_tuile.z + transorfmation_z]
        # Tuiles prioritaires pour continuer en ligne droite
        tuile_prio_a = []
        # Tuiles secondaires pour bifurquer
        tuile_prio_b = []

        # Recherche des prochaines tuiles valides sur la carte
        for tuile in self.terrain.table_tuile:
            contient_chemin_valide = False
            # On cherche un chemin qui continue sur la même ligne
            for chemin_a in tuile.chemins:
                for chemin_b in self.next_tuile.chemins:
                    if chemin_a.couleur == self.couleur_ligne and chemin_b.couleur == self.couleur_ligne and chemin_a == chemin_b:
                        self.chemin = chemin_a
                        contient_chemin_valide = True
            # Vérifie si cette tuile est voisine de la tuile actuelle
            if contient_chemin_valide and (abs(self.next_tuile.x-tuile.x)+abs(self.next_tuile.y-tuile.y)+abs(self.next_tuile.z-tuile.z))/2 == 1:
                # Si c'est la tuile directement en face du train
                if tuile.x == pos_tuile_oposee[0] and tuile.y == pos_tuile_oposee[1] and tuile.z == pos_tuile_oposee[2]:
                    tuile_prio_a.append(tuile)
                # Tuile diagonale admissible
                if (abs(pos_tuile_oposee[0]-tuile.x)+abs(pos_tuile_oposee[1]-tuile.y)+abs(pos_tuile_oposee[2]-tuile.z))/2 == 1.0 and \
                    (abs(self.tuile.x-tuile.x)+abs(self.tuile.y-tuile.y)+abs(self.tuile.z-tuile.z))/2 == 2.0 and tuile != self.next_tuile:
                    tuile_prio_a.append(tuile)
                # Tuile plus éloignée, cas B
                if (abs(pos_tuile_oposee[0]-tuile.x)+abs(pos_tuile_oposee[1]-tuile.y)+abs(pos_tuile_oposee[2]-tuile.z))/2 == 2.0 and \
                     (abs(self.tuile.x-tuile.x)+abs(self.tuile.y-tuile.y)+abs(self.tuile.z-tuile.z))/2 == 1.0 and tuile != self.next_tuile:
                    tuile_prio_b.append(tuile)
        # Priorité A : continuer en ligne
        if len(tuile_prio_a) > 0:
            self.tuile = self.next_tuile
            self.next_tuile = tuile_prio_a[random.randint(0,len(tuile_prio_a)-1)]
        # Sinon, détour possible
        elif len(tuile_prio_b) > 0:
            self.tuile = self.next_tuile
            self.next_tuile = tuile_prio_b[random.randint(0,len(tuile_prio_b)-1)]
        # Sinon, le train fait demi-tour
        else:
            tuile_temp = self.tuile
            self.tuile = self.next_tuile
            self.next_tuile = tuile_temp
            self.direction *= -1
        # Ajout d'un déplacement
        self.nb_deplacements += 1
        # Bonus : si la nouvelle tuile est une ville, le joueur gagne de l'argent en fonction du nombre de déplacements
        if self.tuile.type_terrain == "ville":
            # Ecran.argent += self.nb_deplacements
            self.nb_deplacements = 0
            self.arret = 100

    # Dessine le train comme un petit cercle sur l'écran
    def dessin(self):
        fenetre = self.terrain.fenetre
        fenetre.ctx.save()

        fenetre.ctx.beginPath()
        fenetre.ctx.arc(self.x, self.y, 5, 0, 2 * 3.1416)
        fenetre.ctx.closePath()

        fenetre.ctx.fillStyle = (
            f"rgba({self.couleur[0]}, {self.couleur[1]}, {self.couleur[2]}, 1)"
        )
        fenetre.ctx.fill()

        fenetre.ctx.restore()
