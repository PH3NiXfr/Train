from browser import html, window

class Menu:
    def __init__(self, fenetre):
        self.fenetre = fenetre
        self.couleur_font = (50,50,50)
        self.ouvert = 1
        self.taille_icon = None
        self.pos_x_menu = None
        self.pos_icon = None
        self.icon_select = html.IMG(src="images/menu.png")
        self.boutons = []
        self.boutons.append(Bouton("montagne"))
        self.rezise()
    
    def rezise(self):
        if self.ouvert == 1:
            self.pos_x_menu = window.innerWidth
        else:
            self.pos_x_menu = window.innerWidth*0.8
        self.taille_icon = max(window.innerWidth*0.03, window.innerHeight*0.03)
        self.pos_icon = (self.pos_x_menu - self.taille_icon, 0)
        for bouton in self.boutons:
            bouton.taille = window.innerWidth*0.08
            bouton.pos = (self.pos_x_menu + window.innerWidth*0.06, window.innerHeight*0.4)

    def detection_icon_clique(self, mx, my):
        if self.pos_icon[0] < mx < self.pos_icon[0] + self.taille_icon and \
            self.pos_icon[1] < my < self.pos_icon[1] + self.taille_icon:
            self.ouvert = 1 - self.ouvert
            self.rezise()
            return True
        else:
            for bouton in self.boutons:
                if bouton.pos[0] < mx < bouton.pos[0] + bouton.taille and \
                    bouton.pos[1] < my < bouton.pos[1] + bouton.taille:
                    bouton.activer = 1 - bouton.activer
                    if bouton.activer == 1:
                        self.fenetre.outil = "train"
                    return True
        return False

    def dessin(self):
        fenetre = self.fenetre
        fenetre.ctx.save()

        fenetre.ctx.fillStyle = (
            f"rgba({self.couleur_font[0]}, {self.couleur_font[1]}, {self.couleur_font[2]}, 0.5)"
        )

        fenetre.ctx.fillRect(self.pos_x_menu, 0, window.innerWidth*0.2, window.innerHeight)
        fenetre.ctx.drawImage(self.icon_select, self.pos_icon[0], self.pos_icon[1], self.taille_icon, self.taille_icon)
        for bouton in self.boutons:
            if bouton.activer == 1:
                fenetre.ctx.drawImage(bouton.image, bouton.pos[0], bouton.pos[1], bouton.taille, bouton.taille)
            else:
                fenetre.ctx.filter = "grayscale(100%)"
                fenetre.ctx.drawImage(bouton.image, bouton.pos[0], bouton.pos[1], bouton.taille, bouton.taille)


        fenetre.ctx.restore()

class Bouton:
    def __init__(self, nom):
        self.nom = nom
        self.image = html.IMG(src=f"images/{self.nom}.png")
        self.taille = None
        self.pos = None
        self.activer = 0