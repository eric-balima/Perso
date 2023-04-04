from tracemalloc import stop
from numpy import where
import pygame
from random import randint

def lire_images():
    # Lecture des images
    images = {}

    # lecture de l'image du perso
    image = pygame.image.load("perso.png").convert_alpha()
    images["perso"]=image
    image = pygame.image.load("background.jpg").convert()
    images["fond"]=image
    image = pygame.image.load("balle.png").convert_alpha()
    images["balle"]=image
    image = pygame.image.load("vie.png").convert_alpha()
    images["vie"]=image
    image = pygame.image.load("vitesse.png").convert_alpha()
    images["vitesse"]=image

    # Choix de la police pour le texte
    font = pygame.font.Font(None, 34)
    image = font.render('<Escape> pour quitter', True, (255, 255, 255))
    images["texte1"]=image

    return images

def Musique():
        sons = {}
        son = pygame.mixer.music.load("ambiance.mp3")
        sons["ambiance"]=son
        return sons


class ElementGraphique:
    def __init__(self,image,fenetre,x=0, y=0):
        self.image=image
        self.fenetre = fenetre
        self.rect = image.get_rect()
        self.rect.x=x
        self.rect.y=y


    def afficher(self):
        self.fenetre.blit(self.image, self.rect)
    
    #Fonction de collision
    def collide(self,other):
        if self.rect.colliderect(other.rect):
            return True
        return False
    


class Perso(ElementGraphique):
    def __init__(self,image,fenetre,x=0,y=0):
        super().__init__(image,fenetre,x=0, y=0)

        self.dx = 6
        self.dy = 6
        self.invulnerable = False
        self.vie = 3
        self.compteur = 0

    def appliquer_degats(self):
        if perso.invulnerable is False:
            self.vie -=1


    #Fonction de deplacement du personnage
    def deplacer(self, perso):
        if (touches[pygame.K_LEFT]):
            perso.rect.x -= self.dx
            print("gauche")
        if (touches[pygame.K_RIGHT]):
            perso.rect.x += self.dx
            print("droite")
        if (touches[pygame.K_UP]):
            perso.rect.y -= self.dy
            print("haut")
        if (touches[pygame.K_DOWN]):
            perso.rect.y += self.dy
            print("bas")

        #Empecher le personnage de sortir de la fenetre
        if perso.rect.x < 0:
            perso.rect.x = 0
        if perso.rect.x + perso.rect.w > largeur:
            perso.rect.x = largeur -perso.rect.w
        if perso.rect.y < 0:
            perso.rect.y = 0
        if perso.rect.y + perso.rect.w > hauteur:
            perso.rect.y = hauteur - perso.rect.w



class Balle(ElementGraphique):
    def __init__(self, image, fenetre, x=randint(25,455), y=randint(25,455)):
        super().__init__(image, fenetre, x, y)
        self.dx = 3.3
        self.dy = 3.3
    
    #Fonction de deplacement de la balle
    def deplacer(self, balle):
        balle.rect.x +=self.dx
        balle.rect.y +=self.dy
        #Permettre a la balle de rebondir
        if balle.rect.y <0 or balle.rect.y + balle.rect.h > hauteur :
            self.dy = -self.dy
        if balle.rect.x <0 or balle.rect.x + balle.rect.w > largeur:
            self.dx = -self.dx

class Bonus(ElementGraphique):
    def __init__(self, image, fenetre, x=randint(25,455), y=0):
        super().__init__(image, fenetre, x, y)
        self.dy = 4
        self.compteur = 0
        self.rapide = False
    
    #Fonction de deplacement des bonus
    def deplacer(self, bonus):
        bonus.rect.y +=self.dy
    
    #Fonction de l'effet du bonus de vie
    def effets(self, bonus):
        if perso.collide(bonus):
            perso.vie +=1
            listeBonus.remove(bonus)

    #Fonction de l'effet du bonus de vitesse
    def effets2(self, bonus):
        if self.rapide is True and self.compteur<=150:
            perso.dx = 10
            perso.dy = 10
            self.compteur+=1
        if self.compteur>150:
            self.rapide = False
            self.compteur = 0
        if self.rapide is False:
            perso.dx = 6
            perso.dy = 6
            
            



# Initialisation de la bibliotheque pygame
pygame.init()

#creation de la fenetre
largeur = 640
hauteur = 480
fenetre=pygame.display.set_mode((largeur,hauteur))

images = lire_images()

sons = Musique()
pygame.mixer.music.play()

perso = Perso(images["perso"],fenetre,x=60,y=80)

# lecture de l'image du fond
fond = ElementGraphique(images["fond"],fenetre)

font = pygame.font.Font(None, 34)

texte = font.render('Vies : '+str(perso.vie), True, (204, 204, 255))
texte1 = ElementGraphique(texte,fenetre,x=300,y=10)

# servira a regler l'horloge du jeu
horloge = pygame.time.Clock()

bonus2 = Bonus(images["vitesse"],fenetre,x=randint(5,455),y=0)

listeBonus = []

listeBonusv = []

listeBalles = []

#Creation premiere balle
balle = Balle(images["balle"],fenetre,x=randint(40,455),y=randint(40,455))
listeBalles.append(balle)

#Creation deuxieme balle
balle2 = Balle(images["balle"],fenetre,x=randint(40,455),y=randint(40,455))
listeBalles.append(balle2)

#Creation troisieme balle
balle3 = Balle(images["balle"],fenetre,x=randint(40,455),y=randint(40,455))
listeBalles.append(balle3)


# la boucle dont on veut sortir :
#   - en appuyant sur ESCAPE
#   - en cliquant sur le bouton de fermeture
i=1;
continuer=True
while continuer == True:

    # fixons le nombre max de frames / secondes
    horloge.tick(30)

    i=i+1
    print (i)

    # on recupere l'etat du clavier
    touches = pygame.key.get_pressed();

    # si la touche ESC est enfoncee, on sortira
    # au debut du prochain tour de boucle
    if touches[pygame.K_ESCAPE] :
        continuer=False


    # Affichage du fond
    fond.afficher()

    # Affichage Perso
    perso.afficher()
    perso.deplacer(perso)


    # Apparition première balle
    if i >= 30:
        listeBalles[0].afficher()
        listeBalles[0].deplacer(listeBalles[0])


    #Apparition deuxième balle
    if i >= 60:
        listeBalles[1].afficher()
        listeBalles[1].deplacer(listeBalles[1])


    #Apparition troisième balle
    if i >= 90:
        listeBalles[2].afficher()
        listeBalles[2].deplacer(listeBalles[2])

    #Condition de passage à l'invulnerabilite
    if perso.collide(listeBalles[0]) or perso.collide(listeBalles[1]) or perso.collide(listeBalles[2]):
        perso.appliquer_degats()
        perso.invulnerable = True
    if perso.invulnerable is True:
        if (touches[pygame.K_LEFT] or touches[pygame.K_RIGHT] or touches[pygame.K_UP] or touches[pygame.K_DOWN]):
            perso.compteur +=1
    
    #Condition d'annulation de l'invulnerabilite 
    if perso.compteur >= 30:
        perso.compteur = 0
        perso.invulnerable = False

    #Condition d'arret du jeux
    if perso.vie == 0:
        continuer = False

    #Ajout du bonus de vie
    if len(listeBonus)<2 and randint(1,1000)<=2:
        listeBonus.append(Bonus(images["vie"],fenetre,x=randint(20,455),y=0))
    
    #Afficher et faire disparaitre le bonus de vie
    for bon in listeBonus:
        bon.deplacer(bon)
        if bon.rect.top >= 480 :
            listeBonus.remove(bon)
        else:
            bon.afficher()
        bon.effets(bon)

    #Ajout du bonus de vitesse
    if len(listeBonusv)<1 and randint(1,1000)<=3 and bonus2.rapide is False:
        listeBonusv.append(bonus2)

    #Afficher et faire disparaitre le bonus de vitesse
    for bon in listeBonusv:
        bon.deplacer(bon)
        if bon.rect.top >= 480 :
            listeBonusv.remove(bon)
        else:
            bon.afficher()
        if perso.collide(bon):
            listeBonusv.remove(bon)
    
    if perso.collide(bonus2):
        bonus2.rapide = True
    bonus2.effets2(bonus2)
    
    """print(bonus2.compteur)"""
    print(perso.vie)
    
    # Affichage du Texte
    texte1.afficher()

    # rafraichissement
    pygame.display.flip()

    # Si on a clique sur le bouton de fermeture on sortira
    # au debut du prochain tour de boucle
    # Pour cela, on parcours la liste des evenements
    # et on cherche un QUIT...
    for event in pygame.event.get():   # parcours de la liste des evenements recus
        if event.type == pygame.QUIT:     #Si un de ces evenements est de type QUIT
            continuer = False	   # On arrete la boucle

# fin du programme principal...
pygame.quit()
