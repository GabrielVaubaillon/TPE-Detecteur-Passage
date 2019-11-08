from config import *
import pygame
from pygame.locals import *


#Initialisations des valeurs :
xCentre = (posCapteur[0] + posDiode1[0]) / 2
#On prend : entree : L'obstacle descend (vitesse selon y positif)
#           sortie : L'obstacle monte (vitesse selon y négatif)
yDepartEntree = min(posDiode1[1] , posDiode2[1] , posDiode2[1]) - tailleObstacle - 10
yDepartSortie = max(posDiode1[1] , posDiode2[1] , posDiode2[1]) + 10

yObstacleRayon1 = (posCapteur[1] / posCapteur[0]) * xCentre
yObstacleRayon2 = ((posCapteur[1] - posDiode2[1]) / posCapteur[0]) * xCentre + posDiode2[1]

valeurRef = intensiteDiode1 + intensiteDiode2

ecartDiode = posDiode2[1] #Diode 1 est l'origine
dtParPassage = (ecartDiode + tailleObstacle + 10) / (vitesseObstacle * dt)
print(dtParPassage)

passageEnCours = False

#Fonctions :
def deplaceObstacle(vitesse, dt, posObstacle):
    return (posObstacle[0], posObstacle[1] + dt * vitesse)

def intensiteCapteur(posObstacle , tailleObstacle, intensiteDiode1 , yObstacleRayon1,intensiteDiode2 , yObstacleRayon2):
    yHaut = posObstacle[1]
    yBas = posObstacle[1] + tailleObstacle
    valeur = 0
    #Rappel : l'axe y est vers le bas
    if not (yObstacleRayon1 > yHaut and yObstacleRayon1 < yBas):
        valeur += intensiteDiode1

    if not (yObstacleRayon2 > yHaut and yObstacleRayon2 < yBas):
        valeur += intensiteDiode2

    return valeur


#Initialisation de l'IHM
pygame.init()

fenetre = pygame.display.set_mode((largeur, hauteur))

skinDiode1 = pygame.Surface((5,5))
skinDiode1.fill((255,0,0))
skinDiode2 = pygame.Surface((5,5))
skinDiode2.fill((255,0,0))
skinCapteur = pygame.Surface((5,5))
skinCapteur.fill((0,255,0))

#BouclePrincipale
continuer = True
while continuer:
    for event in pygame.event.get():
        if event.type == QUIT:
            continuer = False
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                continuer = False

            if not passageEnCours:
                if event.key == keyEntree:
                    temps = 0 #faux temps, temps de la simulation, en dt
                    passageEnCours = True
                    valeurs = []
                    vitesse = vitesseObstacle
                    posObstacle = (xCentre, yDepartEntree)
                    print("entrée")

                if event.key == keySortie:
                    temps = 0
                    passageEnCours = True
                    valeurs = []
                    vitesse = - vitesseObstacle
                    posObstacle = (xCentre, yDepartSortie)
                    print("sortie")

    if passageEnCours:
        posObstacle = deplaceObstacle(vitesse,dt,posObstacle)
        valeur = intensiteCapteur(posObstacle , tailleObstacle, intensiteDiode1 , yObstacleRayon1,intensiteDiode2 , yObstacleRayon2)
        valeurs.append(valeur)
        temps += 1
        if temps >= dtParPassage:
            print(valeurs)
            passageEnCours = False
