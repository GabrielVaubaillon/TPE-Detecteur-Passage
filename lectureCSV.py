import matplotlib.pyplot as plt

def graph_from_csv(file):
    f = open("courbes/" + file,'r')
    lignes = f.readlines()
    f.close()

    ligne = lignes[0][:-1]
    ligne = ligne.split(',')
    liste = [ float(x) for x in ligne ]

    plt.plot(liste)
    plt.show()

graph_from_csv('201911082059.dec')
