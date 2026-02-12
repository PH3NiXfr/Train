# import Train, Ecran, Notif

max_n_couleur = 1

class Chemin:
    """
    Classe représentant un chemin de tuiles
    """
    def __init__(self, terrain, couleur):
        """
        Liste ordonnée des tuiles composant le chemin
        """
        self.tuiles = []
        self.terrain = terrain
        self.couleur = couleur

    def add_tuile(self,tuile):
        """
        Ajoute la tuile au chemin si elle ne fait pas déjà partie d’un autre chemin
        
        :param tuile: tuile à ajouter
        """
        if self not in tuile.chemins:
            tuile.chemins.append(self)
        self.tuiles.append(tuile)

    def suppr_chemin(self):
        """
        Suppretion d'un chemin
        """
        # Supprime visuellement et logiquement le chemin
        for tuile in self.tuiles:
            if tuile.type_terrain == "plaine":
                tuile.solution = 0
            else:
                tuile.solution = 1000
            tuile.chemins.remove(self)
        # Supprime aussi les trains liés à ce chemin
        # for train in Train.trains.copy():
        #     if train.chemin == self:
        #         Ecran.argent += round(len(Train.trains)/2)
        #         # Suppretion du train dans la liste des trains
        #         if train.chemin.couleur == couleur_chemins[0]:
        #             Train.nbTrainA -= 1
        #         if train.chemin.couleur == couleur_chemins[1]:
        #             Train.nbTrainB -= 1
        #         if train.chemin.couleur == couleur_chemins[2]:
        #             Train.nbTrainC -= 1
        #         Train.trains.remove(train)
        #         del train
        del self

    # def get_next_tuile(self, train):
    #     """
    #     Renvoie la tuile suivante dans la direction du train
        
    #     :param train: train à traiter
    #     """
    #     for i in range(len(self.tuiles)):
    #         if train.direction == 1:
    #             if train.tuile == self.tuiles[i]:
    #                 if i+1 < len(self.tuiles):
    #                     return self.tuiles[i+1]
    #                 else:
    #                     train.direction *= -1
    #                     return self.tuiles[i-1]
    #         else:
    #             if train.tuile == self.tuiles[i]:
    #                 if i-1 >= 0:
    #                     return self.tuiles[i-1]
    #                 else:
    #                     train.direction *= -1
    #                     return self.tuiles[i+1]
    #     return None
    def dessin(self, terrain, table_chemin):
        """
        Dessin d'un chemin
        """
        for i in range(len(self.tuiles)-1):
            nb_chemin_similaire = 1
            # Vérifie si un autre chemin avec une autre couleur existe entre les mêmes tuiles
            for chemin_comp in table_chemin:
                if chemin_comp.couleur != self.couleur:
                    for j in range(len(chemin_comp.tuiles)-1):
                        if (self.tuiles[i] == chemin_comp.tuiles[j] and self.tuiles[i+1] == chemin_comp.tuiles[j+1]) or (self.tuiles[i+1] == chemin_comp.tuiles[j] and self.tuiles[i] == chemin_comp.tuiles[j+1]):
                            nb_chemin_similaire += 1
            point_a = self.tuiles[i].centre
            point_b = self.tuiles[i+1].centre
            # Dessin du chemin avec décalage s’il y a plusieurs chemins
            if nb_chemin_similaire == 1:
                self.dessin_ligne(point_a, point_b, self.couleur, 2)
            else:
                # Décalages visuels pour éviter les superpositions
                if point_a[0] == point_b[0]:
                    if self.couleur == terrain.couleur_chemins[0]:
                        self.dessin_ligne((point_a[0],point_a[1]), (point_b[0],point_b[1]), self.couleur, 2)
                    if self.couleur == terrain.couleur_chemins[1]:
                        self.dessin_ligne((point_a[0]+2,point_a[1]), (point_b[0]+2,point_b[1]), self.couleur, 2)
                    elif self.couleur == terrain.couleur_chemins[2]:
                        self.dessin_ligne((point_a[0]-3,point_a[1]), (point_b[0]-3,point_b[1]), self.couleur, 2)
                elif (point_a[0]>point_b[0] and point_a[1]<point_b[1]) or (point_a[0]<point_b[0] and point_a[1]>point_b[1]):
                    if self.couleur == terrain.couleur_chemins[0]:
                        self.dessin_ligne((point_a[0],point_a[1]), (point_b[0],point_b[1]), self.couleur, 2)
                    if self.couleur == terrain.couleur_chemins[1]:
                        self.dessin_ligne((point_a[0]+4-1,point_a[1]+1), (point_b[0]+4-1,point_b[1]+1), self.couleur, 2)
                    elif self.couleur == terrain.couleur_chemins[2]:
                        self.dessin_ligne((point_a[0]-4+1,point_a[1]-1), (point_b[0]-4+1,point_b[1]-1), self.couleur, 2)
                else:
                    if self.couleur == terrain.couleur_chemins[0]:
                        self.dessin_ligne((point_a[0],point_a[1]), (point_b[0],point_b[1]), self.couleur, 2)
                    if self.couleur == terrain.couleur_chemins[1]:
                        self.dessin_ligne((point_a[0]+4-1,point_a[1]-1), (point_b[0]+4-1,point_b[1]-1), self.couleur, 2)
                    elif self.couleur == terrain.couleur_chemins[2]:
                        self.dessin_ligne((point_a[0]-4+1,point_a[1]+1), (point_b[0]-4+1,point_b[1]+1), self.couleur, 2)

    def dessin_ligne(self, point_a, point_b, couleur, epaisseur):
        fenetre = self.terrain.fenetre
        fenetre.ctx.save()
        fenetre.ctx.beginPath()
        fenetre.ctx.moveTo(point_a[0], point_a[1])
        fenetre.ctx.lineTo(point_b[0], point_b[1])
        fenetre.ctx.lineWidth = epaisseur
        fenetre.ctx.strokeStyle = (
            f"#{format(couleur[0], '02X')}"
            f"{format(couleur[1], '02X')}"
            f"{format(couleur[2], '02X')}"
        )
        fenetre.ctx.stroke()
        fenetre.ctx.restore()

def resolution(terrain, tuile_source, tuile_destination, mem_chemin):
    """
    Algorithme de résolution de chemin entre deux tuiles
    
    :param terrain: Terrain
    :param tuile_source: Tuile de depart
    :param tuile_destination: Tuile d'arrivée
    :param mem_chemin: A definir
    """
    chemin_existe = False
    # Vérifie que la destination est disponible
    tuile_disponible = False
    for dx, dy in [(1,0), (-1,0), (0,1), (0,-1), (1,-1), (-1,1)]:
        tuile_test = terrain.get_tuile(tuile_destination.x+dx,tuile_destination.y+dy)
        if tuile_test.solution == 0:
            tuile_disponible = True
    
    # Tables de traitenement
    table_tuile_a_traiter = [tuile_source]
    table_tuile_traitee = []
    if tuile_disponible:
        # Niveau de la case
        solution_number = 1
        # Attribution des niveau des case de départ et arrivées
        tuile_source.solution = solution_number
        tuile_destination.solution = 0
        # Tant que la solution n'est pas trouvée donner un numéros a toutes les cases
        while tuile_destination not in table_tuile_a_traiter:
            # Test des case autours de celles déjà traités
            table_tuile_a_traiter_temp = table_tuile_a_traiter.copy()
            tuile_la_plus_proche = table_tuile_a_traiter_temp[0]
            for tuile in table_tuile_a_traiter_temp:
                if abs(tuile_la_plus_proche.x-tuile_destination.x) + abs(tuile_la_plus_proche.y-tuile_destination.y) + abs(tuile_la_plus_proche.z-tuile_destination.z) > abs(tuile.x-tuile_destination.x) + abs(tuile.y-tuile_destination.y) + abs(tuile.z-tuile_destination.z):
                    tuile_la_plus_proche = tuile
            solution_exist = False
            solution_number += 1
            # Vérifie les 6 voisins hexagonaux
            for dx, dy in [(1,0), (-1,0), (0,1), (0,-1), (1,-1), (-1,1)]:
                solution_exist,table_tuile_a_traiter = terrain.get_tuile(tuile_la_plus_proche.x+dx,tuile_la_plus_proche.y+dy).test_tuile(tuile_la_plus_proche.solution,table_tuile_a_traiter,table_tuile_traitee)
            # Suppretion des cases à traiter si la case n'a plus de cases à coté
            if not solution_exist and tuile_destination != tuile_source:
                table_tuile_a_traiter.remove(tuile_la_plus_proche)
            if tuile_destination in table_tuile_a_traiter:
                chemin_existe = True
                break

            # S'il n'y a plus de case à traiter (pas de solution)
            if table_tuile_a_traiter == []:
                break
            solution_number += 1
    
    # Si un chemin est trouvé
    if chemin_existe:
        # Vérification si le chemin est relier à un autre de la même couleur
        tuile_source_relie = True
        tuile_destination_relie = True
        if (terrain.n_couleur_chemin == 0 and terrain.nb_ligne_a != 0) or (terrain.n_couleur_chemin == 1 and terrain.nb_ligne_b != 0) or (terrain.n_couleur_chemin == 2 and terrain.nb_ligne_c != 0):
            tuile_source_relie = False
            tuile_destination_relie = False
            # Véfification pour la source
            for chemin in tuile_source.chemins:
                if chemin.couleur == terrain.couleur_chemins[terrain.n_couleur_chemin]:
                    tuile_source_relie = True
                    break
            # Véfification pour la destination
            for chemin in tuile_destination.chemins:
                if chemin.couleur == terrain.couleur_chemins[terrain.n_couleur_chemin]:
                    tuile_destination_relie = True
                    break
        if tuile_source_relie or tuile_destination_relie:
            chemin_final = Chemin(terrain, terrain.couleur_chemins[terrain.n_couleur_chemin])
            tuile_analysee = tuile_destination
            chemin_final.add_tuile(tuile_analysee)
            # Remonte le chemin du plus petit niveau vers la source
            while (tuile_analysee != tuile_source):
                possiblitees = []
                # Vérifie les voisins avec un niveau inférieur
                if tuile_analysee.solution < 1000:
                    for dx, dy in [(1,0), (-1,0), (0,1), (0,-1), (1,-1), (-1,1)]:
                        if terrain.get_tuile(tuile_analysee.x+dx,tuile_analysee.y+dy).solution < tuile_analysee.solution and terrain.get_tuile(tuile_analysee.x+dx,tuile_analysee.y+dy).solution > 0:
                            possiblitees.append(terrain.get_tuile(tuile_analysee.x+dx,tuile_analysee.y+dy))
                # Choisit le voisin le plus proche de la source
                if len(possiblitees) > 0:
                    tuile_analysee = possiblitees[0]
                    for possiblitee in possiblitees:
                        if (abs(possiblitee.x-tuile_source.x) + abs(possiblitee.y-tuile_source.y) + abs(possiblitee.z-tuile_source.z))/2 <= (abs(tuile_analysee.x-tuile_source.x) + abs(tuile_analysee.y-tuile_source.y) + abs(tuile_analysee.z-tuile_source.z))/2:
                            tuile_analysee = possiblitee
                    if tuile_analysee not in chemin_final.tuiles:
                        chemin_final.add_tuile(tuile_analysee)
                else:
                    mem_chemin = False
                    print("ERROR")
                    break
            # if mem_chemin:
            #     if chemin_final.couleur == terrain.couleur_chemins[0]:
            #         if len(chemin_final.tuiles) * round(nb_ligne_a*0.5) > Ecran.argent:
            #             mem_chemin = False
            #             # Notif.notif_pas_assez_argent.montrer = True
            #     elif chemin_final.couleur == terrain.couleur_chemins[1]:
            #         if len(chemin_final.tuiles) * round(nb_ligne_b*0.5) > Ecran.argent:
            #             mem_chemin = False
            #             # Notif.notif_pas_assez_argent.montrer = True
            #     elif chemin_final.couleur == terrain.couleur_chemins[2]:
            #         if len(chemin_final.tuiles) * round(nb_ligne_c*0.5) > Ecran.argent:
            #             mem_chemin = False
            #             # Notif.notif_pas_assez_argent.montrer = True
            # Nettoie les niveaux des tuiles
            if tuile_source.type_terrain == "mer" or tuile_source.type_terrain == "montagnes":
                tuile_source.solution = 1000
            else:
                tuile_source.solution = 0
            if mem_chemin:
                for tuile in table_tuile_traitee:
                    tuile.solution = 0
                    # Tuile.actualiserNbVille()
                return chemin_final, True
            else:
                for tuile in table_tuile_traitee:
                    if tuile.type_terrain == "mer" or tuile.type_terrain == "montagnes":
                        tuile.solution = 1000
                    else:
                        tuile.solution = 0
                for tuile in chemin_final.tuiles:
                    tuile.chemins.remove(chemin_final)
                return chemin_final, False
        else:
            # Chemin non relié à un autre chemin
            # if mem_chemin:
            #     Notif.notifCheminNonRelie.montrer = True
            for tuile in table_tuile_traitee:
                tuile.solution = 0
            return [], False
    else:
        # Aucun chemin trouvé
        # if mem_chemin:
        #     Notif.notifCheminNonTrouve.montrer = True
        for tuile in table_tuile_traitee:
            tuile.solution = 0
        return [], False

