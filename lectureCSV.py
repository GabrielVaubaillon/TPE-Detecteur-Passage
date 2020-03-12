import matplotlib.pyplot as plt

def graph_from_csv(file):
    name = file[0:4] + "/" + file[4:6] + "/" + file[6:8] + " à " + file[8:10] + ":" + file[10:12]

    f = open("courbes/" + file,'r')
    lignes = f.readlines()
    f.close()

    #Les valeurs sont sur la deuxieme ligne, la premiere correspond à l'entete
    ligne = lignes[1][:-1]
    ligne = ligne.split(',')
    liste = [ float(x) for x in ligne[:-1] ]

    plt.plot(liste)
    plt.title(name)
    plt.xlabel("Temps (t)")
    plt.ylabel("Tension (U)")
    plt.show()

graph_from_csv('donneexpARAA.dec')
