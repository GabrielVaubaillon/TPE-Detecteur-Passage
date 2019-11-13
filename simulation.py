#--------------------------
#Imports :
#--------------------------

from config import *
import pygame
from time import sleep,localtime
from pygame.locals import *

#--------------------------
#Classes :
#--------------------------

class Diode:
    def __init__(self, pos, intensite):
        self.x = pos[0]
        self.y = pos[1]
        self.intensite = intensite
        #Pour l'affichage :
        self.skin = pygame.Surface((5,5))
        self.skin.fill(couleurDiode)

    def affiche(self,decal):
        pixelPosition = ((self.x + decal[0]) * pixelsParCentimetre, (self.y + decal[1]) * pixelsParCentimetre)
        fenetre.blit(self.skin, pixelPosition)


class Capteur:
    def __init__(self, pos):
        self.x = pos[0]
        self.y = pos[1]
        #Pour l'affichage :
        self.skin = pygame.Surface((5,5))
        self.skin.fill(couleurCapteur)

    def affiche(self,decal):
        pixelPosition = ((self.x + decal[0]) * pixelsParCentimetre, (self.y + decal[1]) * pixelsParCentimetre)
        fenetre.blit(self.skin, pixelPosition)


class Obstacle:
    def __init__(self, taille, position, vitesse):
        self.taille = taille
        self.x = position[0]
        self.y = position[1]
        self.vitesse = vitesse
        #Pour l'affichage :
        self.skin = pygame.Surface((5,self.taille * pixelsParCentimetre))
        self.skin.fill(couleurObstacle)

    def affiche(self,decal):
        pixelPosition = ((self.x + decal[0]) * pixelsParCentimetre, (self.y + decal[1]) * pixelsParCentimetre)
        fenetre.blit(self.skin, pixelPosition)

    def avance(self,dt):
        #L'obstacle ne se déplace que selon l'axe y
        self.y = self.y + dt * self.vitesse

    def isLoinDuDispositif(self):
        return self.y > startBas or self.y < startHaut

#--------------------------
#Fonctions :
#--------------------------

def str_nb(n,taille = 2):
    #But de la fonction : écrit les nombres à la bonne taille,
    #    avec des 0 devant si ils sont trops courts
    #IN : n , float or int, le nombre que l'on veut écrire
    #     taille , int , la taille du nombre écrit (2 par défaut)
    ch = str(n)
    while len(ch) < taille:
        ch = '0' + ch
    return ch

def intensiteCapteur(obstacle,diode1,diode2,intersection1,intersection2):
    yHaut = obstacle.y
    yBas = obstacle.y + obstacle.taille
    valeur = 0
    #Rappel : l'axe y est vers le bas
    if not (intersection1 > yHaut and intersection1 < yBas):
        valeur += diode1.intensite

    if not (intersection2 > yHaut and intersection2 < yBas):
        valeur += diode2.intensite

    return valeur

def affiche(fond,diode1,diode2,obstacle,capteur,valeur,passage = False):
    fenetre.blit(fond,(0,0))
    decalage = affichageOrigine
    diode1.affiche(decalage)
    diode2.affiche(decalage)
    obstacle.affiche(decalage)
    capteur.affiche(decalage)
    afficheTexte((10,10),str(valeur))
    if passage:
        afficheTexte((10,25),"Passage en cours ")

    pygame.display.flip()

def afficheTexte(pos,ch,flip = False):
    message = police.render(ch + "   ",True, (255,255,255), (0,0,0))
    fenetre.blit(message, pos)
    if flip:
        pygame.display.flip()

def entete():
    #Permet de générer l'entete du fichier contenant la configuration
    ch = ''
    ch += 'posCapteur : ' + str(posCapteur) + "; "
    ch += 'ecartDiodes : ' + str(ecartDiodes) + "; "
    ch += 'vitesseObstacle : ' + str(vitesseObstacle) + "; "
    ch += 'tailleObstacle : ' + str(tailleObstacle) + "; "
    ch += 'intensiteDiode1 : ' + str(intensiteDiode1) + "; "
    ch += 'intensiteDiode2 : ' + str(intensiteDiode2) + "; "
    ch += 'dt : ' + str(dt) + "; "
    ch += 'riseTime : ' + str(riseTime) + "; "
    ch += 'fallTime : ' + str(fallTime) + "; \n"
    return ch

def fromListToCSV(liste):
    #sauvegarde la liste des valeurs dans un fichier csv
    print("Ne pas eteindre, sauvegarde des données en cours")
    D = localtime()
    name = str(D[0]) + str_nb(D[1]) + str_nb(D[2]) + str_nb(D[3])+ str_nb(D[4]) + ".dec"
    f = open("courbes/" + name, "w")
    f.write(entete())
    for el in liste:
        f.write(str(el) + ',')
    f.close()
    print(name, "sauvegardé")

#--------------------------
#Initialisations des valeurs :
#--------------------------

diode1 = Diode((0,0), intensiteDiode1)
diode2 = Diode((0, ecartDiodes), intensiteDiode2)
capteur = Capteur(posCapteur)
obstacle = None
xCentre = capteur.x / 2.0

#On prend : entree : L'obstacle descend (vitesse selon y positif)
#           sortie : L'obstacle monte (vitesse selon y négatif)
#Coordonnée y de départ de l'obstacle :
startHaut = min(diode1.y , diode2.y , capteur.y) - (tailleObstacle + margeDepart)
startBas = max(diode1.y , diode2.y , capteur.y) + margeDepart

#Niveau y où la trajectoire de l'obstacle coupe celle des rayons lumineux diode/capteur
intersection1 = (capteur.y / capteur.x) * xCentre
intersection2 = ((capteur.y - diode2.y) / capteur.x) * xCentre + diode2.y

#intensite reçue par le capteur lorsqu'aucune diode est obstruée
valeurRef = diode1.intensite + diode2.intensite

#Temps nécessaire à l'objet pour passer
dtParPassage = (vitesseObstacle / (startBas - startHaut + tailleObstacle)) / dt
#Vitesse divisée par distance, divisé par dt

mesures = []

#--------------------------
#Initialisation de l'IHM
#--------------------------

pygame.init()
hauteur = (max(diode1.y , diode2.y , capteur.y) + 10) * pixelsParCentimetre
largeur = (capteur.x + 10) * pixelsParCentimetre


fenetre = pygame.display.set_mode((largeur, hauteur))

fond = pygame.Surface((largeur, hauteur))
fond.fill((0,0,0))

police = pygame.font.Font(pygame.font.get_default_font(),pixelsParCentimetre)

#--------------------------
#BouclePrincipale :
#--------------------------

continuer = True
while continuer:
    sleep(max(timeGap,dt))
    for event in pygame.event.get():
        if event.type == QUIT:
            continuer = False
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                continuer = False

            if obstacle == None: # on ne lance pas plusieurs obstacle en même temps
                if event.key == keyEntree:
                    obstacle = Obstacle(tailleObstacle, (xCentre, startHaut), vitesseObstacle)

                if event.key == keySortie:
                    obstacle = Obstacle(tailleObstacle,(xCentre, startBas), - vitesseObstacle)

    if obstacle != None:
        obstacle.avance(dt)
        valeur = intensiteCapteur(obstacle,diode1,diode2,intersection1,intersection2)
        mesures.append(valeur)
        affiche(fond,diode1,diode2,obstacle,capteur,valeur,passage = True)
        if obstacle.isLoinDuDispositif():
            obstacle = None
    else:
        afficheTexte((10,25),"Passage fini       ",flip = True)
        mesures.append(valeurRef)

fromListToCSV(mesures)
