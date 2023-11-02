import random
import numpy as np

NPAR = 60
LARGO = 10
VEL = 5

coordenadas_unicas = set()
while len(coordenadas_unicas) < NPAR:
    fila = (random.randint(0, LARGO), random.randint(0, LARGO))
    coordenadas_unicas.add(fila)

matriz1 = list(coordenadas_unicas)
random.shuffle(matriz1)

matriz2 = np.random.randint(-VEL, VEL+1, size=(NPAR, 2))

matriz_final = np.concatenate((matriz1, matriz2), axis=1)

np.savetxt("Datos.dat", matriz_final, fmt="%d", delimiter="\t")
print("Matriz guardada en Datos.dat")
