
#Les positions sont exprimées dans un repère cartésien avec x horizontal vers
#la droite et y vertical vers le bas. La mesure est en centimètres
#L'origine du repere est la diode 1
#L'autre diode est située sur l'axe y.

#Afin de décrire la positions des diodes, il suffit de donner l'écartement entre
#Elles. En centimetres

#Les valeurs des coordonnées sont en centimetres
posCapteur = (100,5)

ecartDiodes = 10

#La vitesse est exprimée en cm/s. La seule vitesse sera selon y
vitesseObstacle = 300.0
#La largeur de l'obstacle qui passe par la porte, en cm
tailleObstacle = 30

#Les intensités des diodes sont les valeurs les plus difficiles à obtenir
#Il faut prendre en compte le cone de dispersion. On simplifie grandement cette
# étape en prenant un capteur ponctuel. Nous avons par conséquent une seule valeur
# d'intensité reçue par le capteur pour chaque diode
intensiteDiode1 = 8.0
intensiteDiode2 = 4.0

rise_time = 0.2 * pow(10, -6)
fall_time = rise_time

#Nombre de secondes simulées entre chaque calcul (float)
dt = 0.001

#Temps entre chaque affichage, pour permettre de voir quelquechose sur l'affichage
timeGap = 0.01

#Propre au programme :
pixelsParCentimetre = 15

#La position apparente de l'origine lors de l'affichage
affichageOrigine = (5,5)

#La distance au dispositif à laquelle l'obstacle commence (en cm)
margeDepart = 10

from pygame.locals import *

keyEntree = K_DOWN
keySortie = K_UP
