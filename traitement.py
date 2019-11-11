from config import *

import statistics
from statistics import mean



def fromCsvToList(file):
    f = open("courbes/" + file, 'r')
    lignes = f.readlines()
    f.close()
    #On prend la deuxieme ligne parceque la premiere contient l'entete avec les
    #Valeurs de configurations que l'on avait rentrée
    ligne = lignes[0][:-1]
    ligne = ligne[:-1]
    ligne = ligne.split(',')
    liste = [ float(x) for x in ligne ]

    return liste

def egal(nombre1, nombre2):
    return abs(nombre1 - nombre2) <= EPSILON

def superieur(nombre1, nombre):
    return nombre1 < (EPSILON + nombre2)

def inferieur(nombre1, nombre2):
    return nombre1 > (EPSILON + nombre2)


def escalier(liste):
    palier = []
    tmp = []
    for val in liste:
        if (len(tmp) == 0): #Si le tableau temp est vide
            tmp.append(val)

        if egal(val, mean(tmp)):
            tmp.append(val)
        elif len(tmp) >= STANDBY_ITERATION:
            palier.append(mean(tmp))
            tmp = []
        else:
            tmp = []

    if len(tmp) >= TEMPSSTANDBY:
        palier.append(mean(tmp))

    return palier



def analyse(liste):
    if liste[0] < liste[2]:
        if ENTREEDOWNUP:
            res = 'entree'
        else:
            res = 'sortie'
    elif liste[0] > liste[2]:
        if ENTREEDOWNUP:
            res = 'sortie'
        else:
            res = 'entree'
    else:
        res = 'erreur'
    return res

#----------------------------------
#Programme Principal :
#----------------------------------
EPSILON = 0.213
STANDBY_ITERATION = 4 #nb de dtnécessaire pour avoir un état stationnaire

#Si lors d'une entrée le premier palier est plus bas que le second :
ENTREEDOWNUP = True

file = '201911111808.dec'

valeurs = fromCsvToList(file)

nbValeurs = len(valeurs)
t = 0

cptPersonnes = 0

tampon = []
tailleTampon = ((ecartDiodes + tailleObstacle + 2 * margeDepart) / vitesseObstacle) // dt

#Premier elementt
val = valeurs[t]
tampon.append(val)
vref = val
t += 1
while t < nbValeurs:

    if val < vref :
        passageEnCours = True  #On part du principe que l'obstacle est assez large
        #pour obstruer les deux diodes en meme temps lorsque qu'il passe
        liste = []
        while passageEnCours:
            passageEnCours = not egal(vref,val)

            #Obtenir element
            liste.append(val)
            if (len(tampon) < tailleTampon):
                tampon.append(val)
            else:
                tampon = [val] + tampon[:-1]
            val = valeurs[t]
            t += 1

        print("1",liste)
        liste = escalier(liste)
        print("2",liste)
        typePassage = analyse(liste)
        print(typePassage)

        if typePassage == 'entree':
            cptPersonnes += 1
        elif typePassage == 'sortie' :
            cptPersonnes -= 1
        print(cptPersonnes)




    #Obtenir Element suivant

    # TODO: Obtenir Vref

    #On met à jour la liste tampon :
    if (len(tampon) < tailleTampon):
        tampon.append(val)
    else:
        tampon = [val] + tampon[:-1]
    #On obtient la valeur suivante :
    val = valeurs[t]
    t += 1
