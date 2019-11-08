import matplotlib.pyplot as plt

def graph_from_csv(file):
    f = open("courbes/" + file,'r')
    lignes = f.readlines()
    f.close()

    for i in range(len(lignes)):
        ligne = lignes[i][:-1]
        ligne = ligne.split(',')
        ligne = [ float(x) for x in ligne ]

        """liste = []
        for j in range(0,len(ligne),pas_values):
            liste.append(ligne[j])"""
        plt.plot(ligne)
    plt.show()

graph_from_csv('201911082021.dec')
