from config import *

import statistics
from statistics import mean


#--------------------------
#Configuration du traitement :
#--------------------------

#Nom du fichier csv que l'on analyse :
file = 'donneexpARAA.dec'
#Précision pour les égalités :
EPSILON = 50
#Nombre nécessaire de valeurs pour que ça soit considéré comme un palier
STANDBY_ITERATION = 4

#Si lors d'une entrée le premier palier est plus bas que le second :
#(permet de changer le sens entree sortie)
ENTREEDOWNUP = True

#--------------------------
#Fonctions :
#--------------------------

def fromCsvToList(file):
    #But de la fonction : renvoyer la liste correspondant au fichier csv passé
    #   en paramètre
    f = open("courbes/" + file, 'r')
    lignes = f.readlines()
    f.close()
    #On prend la deuxieme ligne parceque la premiere contient l'entete avec les
    #Valeurs de configurations que l'on avait rentrée
    ligne = lignes[1][:-1]
    ligne = ligne[:-1]
    ligne = ligne.split(',')
    liste = [ float(x) for x in ligne ]
    return liste

def egal(nombre1, nombre2):
    #Regarde si les deux nombres sont égaux, à EPSILON près
    return abs(nombre1 - nombre2) <= EPSILON

def escalier(liste):
    #Permet de ne conserver que les valeurs des paliers de la liste entrée en paramètre
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

    if len(tmp) >= STANDBY_ITERATION:
        palier.append(mean(tmp))

    return palier

def analyse(liste):
    #Définie à partir des paliers si l'on a détecté une entrée ou une sortie

    if len(liste) < 3 or len(liste) > 4:
        res = 'erreur'
        print("Faux passage")
    else:
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
#Initialisation :
#----------------------------------

valeurs = fromCsvToList(file)

nbValeurs = len(valeurs)
#Compteur :
t = 0 #Afin de savoir à quelle valeur on est

cptPersonnes = 0 #Nombre de personnes déjà dans la salle

#On a prévu de garder plusieurs valeurs dans un tableau python, pour recalculer
#Vref au besoin, ce que nous n'avons pas encore mis dans le programme
#tampon = []
#tailleTampon = ((ecartDiodes + tailleObstacle + 2 * margeDepart) / vitesseObstacle) // dt

#Premier element
val = valeurs[t]
#tampon.append(val)
vref = val
t += 1
while t < nbValeurs:
    if val < vref - EPSILON :
        passageEnCours = True  #On part du principe que l'obstacle est assez large
        #pour obstruer les deux diodes en meme temps lorsque qu'il passe. Ce qui
        #veut dire que le passage est terminé lorsque la valeur courante revient
        #à Vref. On considere que Vref ne change pas sur la durée du passage
        liste = []
        while passageEnCours:
            passageEnCours = not egal(vref,val)

            #Obtenir element
            liste.append(val)
            #if (len(tampon) < tailleTampon):
            #    tampon.append(val)
            #else:
            #    tampon = [val] + tampon[:-1]
            val = valeurs[t]
            t += 1
        liste = escalier(liste) #On ne conserve que les paliers des valeurs
        typePassage = analyse(liste) #On défini le sens du passage

        if typePassage == 'entree':
            cptPersonnes += 1
        elif typePassage == 'sortie' :
            cptPersonnes -= 1
        print("Il y a ",cptPersonnes," personnes dans la salle.")

    #On met à jour la liste tampon :
    #if (len(tampon) < tailleTampon):
    #    tampon.append(val)
    #else:
    #    tampon = [val] + tampon[:-1]

    #On obtient la valeur suivante :
    val = valeurs[t]
    t += 1
