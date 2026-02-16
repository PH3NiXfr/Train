"""
Module définissant la classe Train.

Un train se déplace le long d'un chemin entre différentes tuiles
du terrain et gère ses propres règles de déplacement.
"""

import random


class Train:
    """
    Représente un train circulant sur le terrain.

    :param terrain: Instance du terrain contenant le train.
    :type terrain: Terrain
    :param tuile: Tuile de départ du train.
    :type tuile: Tuile
    :param chemin: Chemin emprunté par le train.
    :type chemin: Chemin
    """

    def __init__(self, terrain, tuile, chemin):
        """
        Initialise un train avec sa position, son chemin et ses paramètres.
        """
        self.tuile = tuile
        self.chemin = chemin
        self.terrain = terrain

        # Décompte du nombre de trains par ligne
        if chemin.couleur == self.terrain.couleur_chemins[0]:
            terrain.nb_train_a += 1
        elif chemin.couleur == self.terrain.couleur_chemins[1]:
            terrain.nb_train_b += 1
        elif chemin.couleur == self.terrain.couleur_chemins[2]:
            terrain.nb_train_c += 1

        # Couleur du train (légèrement assombrie par rapport à la ligne)
        self.couleur = (
            max(0, self.chemin.couleur[0] - 100),
            max(0, self.chemin.couleur[1] - 100),
            max(0, self.chemin.couleur[2] - 50),
        )
        self.couleur_ligne = self.chemin.couleur

        self.direction = 1
        self.next_tuile = self.chemin.get_next_tuile(self)

        self.x = tuile.centre[0]
        self.y = tuile.centre[1]

        self.arret = 0
        self.nb_deplacements = 0

    def mouvement(self):
        """
        Gère le déplacement du train vers la prochaine tuile.
        """
        if self.arret > 0:
            self.arret -= 1
            return

        attendre = False
        for train in self.terrain.trains:
            if (
                train != self
                and train.tuile == self.next_tuile
                and train.tuile.type_terrain == "ville"
                and self.tuile.type_terrain != "ville"
                and train.couleur_ligne == self.couleur_ligne
            ):
                attendre = True

        if attendre:
            return

        # Déplacement progressif vers la tuile cible
        if self.x < self.next_tuile.centre[0] and self.x + 2 < self.next_tuile.centre[0]:
            if self.y < self.next_tuile.centre[1] and self.y + 2 < self.next_tuile.centre[1]: #testm
                self.x += 2
                self.y += 1
            elif self.y > self.next_tuile.centre[1] and self.y - 2 > self.next_tuile.centre[1]:
                self.x += 2
                self.y -= 1
            else:
                self.x += 2
        elif self.x > self.next_tuile.centre[0] and self.x - 2 > self.next_tuile.centre[0]:
            if self.y < self.next_tuile.centre[1] and self.y + 2 < self.next_tuile.centre[1]:
                self.x -= 2
                self.y += 1
            elif self.y > self.next_tuile.centre[1] and self.y - 2 > self.next_tuile.centre[1]:
                self.x -= 2
                self.y -= 1
            else:
                self.x -= 2
        elif self.y < self.next_tuile.centre[1] and self.y + 2 < self.next_tuile.centre[1]:
            self.y += 2
        elif self.y > self.next_tuile.centre[1] and self.y - 2 > self.next_tuile.centre[1]:
            self.y -= 2

        if (
            abs(self.x - self.next_tuile.centre[0]) < 4
            and abs(self.y - self.next_tuile.centre[1]) < 4
        ):
            self.changer_tuile()

    def changer_tuile(self):
        """
        Met à jour la tuile courante lorsque le train atteint sa destination.
        """
        transformation_x = self.next_tuile.x - self.tuile.x
        transformation_y = self.next_tuile.y - self.tuile.y
        transformation_z = self.next_tuile.z - self.tuile.z

        pos_tuile_oposee = [
            self.next_tuile.x + transformation_x,
            self.next_tuile.y + transformation_y,
            self.next_tuile.z + transformation_z,
        ]

        tuile_prio_a = []
        tuile_prio_b = []

        for tuile in self.terrain.table_tuile:
            contient_chemin_valide = False

            for chemin_a in tuile.chemins:
                for chemin_b in self.next_tuile.chemins:
                    if (
                        chemin_a.couleur == self.couleur_ligne
                        and chemin_b.couleur == self.couleur_ligne
                        and chemin_a == chemin_b
                    ):
                        self.chemin = chemin_a
                        contient_chemin_valide = True

            if (
                contient_chemin_valide
                and (
                    abs(self.next_tuile.x - tuile.x)
                    + abs(self.next_tuile.y - tuile.y)
                    + abs(self.next_tuile.z - tuile.z)
                )
                / 2
                == 1
            ):
                if (
                    tuile.x == pos_tuile_oposee[0]
                    and tuile.y == pos_tuile_oposee[1]
                    and tuile.z == pos_tuile_oposee[2]
                ):
                    tuile_prio_a.append(tuile)

                if (
                    (
                        abs(pos_tuile_oposee[0] - tuile.x)
                        + abs(pos_tuile_oposee[1] - tuile.y)
                        + abs(pos_tuile_oposee[2] - tuile.z)
                    )
                    / 2
                    == 1.0
                    and (
                        abs(self.tuile.x - tuile.x)
                        + abs(self.tuile.y - tuile.y)
                        + abs(self.tuile.z - tuile.z)
                    )
                    / 2
                    == 2.0
                    and tuile != self.next_tuile
                ):
                    tuile_prio_a.append(tuile)

                if (
                    (
                        abs(pos_tuile_oposee[0] - tuile.x)
                        + abs(pos_tuile_oposee[1] - tuile.y)
                        + abs(pos_tuile_oposee[2] - tuile.z)
                    )
                    / 2
                    == 2.0
                    and (
                        abs(self.tuile.x - tuile.x)
                        + abs(self.tuile.y - tuile.y)
                        + abs(self.tuile.z - tuile.z)
                    )
                    / 2
                    == 1.0
                    and tuile != self.next_tuile
                ):
                    tuile_prio_b.append(tuile)

        if tuile_prio_a:
            self.tuile = self.next_tuile
            self.next_tuile = random.choice(tuile_prio_a)
        elif tuile_prio_b:
            self.tuile = self.next_tuile
            self.next_tuile = random.choice(tuile_prio_b)
        else:
            tuile_temp = self.tuile
            self.tuile = self.next_tuile
            self.next_tuile = tuile_temp
            self.direction *= -1

        self.nb_deplacements += 1

        if self.tuile.type_terrain == "ville":
            self.nb_deplacements = 0
            self.arret = 50

    def dessin(self):
        """
        Dessine le train sous forme de cercle sur le canvas.
        """
        fenetre = self.terrain.fenetre
        fenetre.ctx.save()

        fenetre.ctx.beginPath()
        fenetre.ctx.arc(self.x, self.y, 5, 0, 2 * 3.1416)
        fenetre.ctx.closePath()

        fenetre.ctx.fillStyle = (
            f"rgba({self.couleur[0]}, "
            f"{self.couleur[1]}, "
            f"{self.couleur[2]}, 1)"
        )
        fenetre.ctx.fill()

        fenetre.ctx.restore()
