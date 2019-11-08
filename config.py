
#Les positions sont exprimées dans un repère cartésien avec x horizontal vers
#la droite et y vertical vers le bas
#Les valeurs des coordonnées sont en centimetres
posCapteur = (10,5)

#On suppose que les diodes ont toujours la même position en x.
#On choisit à priori tout le temps l'origine à la diode 1
posDiode1 = (0,0)

posDiode2 = (0,10)

#La vitesse est exprimée en m/s. La seule vitesse sera selon y
vitesseObstacle = 1.0
#La largeur de l'obstacle qui passe par la porte
tailleObstacle = 30

#Les intensités des diodes sont les valeurs les plus difficiles à obtenir
#Il faut prendre en compte le cone de dispersion. On simplifie grandement cette
# étape en prenant un capteur ponctuel. Nous avons par conséquent une seule valeur
# d'intensité reçue par le capteur pour chaque diode
intensiteDiode1 = 8.0

intensiteDiode2 = 4.0

#Nombre de secondes entre chaque calcul (float)
dt = 0.5

#Propre au programme :
from pygame.locals import *

#Taille de la fenetre (plus tard calculé en fonction des points donnés)
#Les valeurs sont en pixel
largeur = 1000
hauteur = 1000

keyEntree = K_UP
keySortie = K_DOWN
