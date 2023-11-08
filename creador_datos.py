"""Programa para crear los datos iniciales"""
import math
import os
import random
import matplotlib.pyplot as plt
import numpy as np

SISTEMA = 4
NPAR = 70
LARGO = 10
VEL = 5
DES_VEL = 1

carpeta = f'Sistemas/Sistema_{SISTEMA}'
if not os.path.exists(carpeta):
    os.makedirs(carpeta)

coordenadas_unicas = []
while len(coordenadas_unicas) < NPAR:
    fila = (round(random.uniform(0, LARGO), 3), round(
        random.uniform(0, LARGO), 3), round(random.uniform(0, LARGO), 3))
    if fila not in coordenadas_unicas:
        coordenadas_unicas.append(fila)

matriz1 = coordenadas_unicas
parte_entera = np.round(np.random.normal(VEL, DES_VEL, size=(NPAR, 3)), 3)
signos = np.random.choice([-1, 1], size=(NPAR, 3))
matriz2 = parte_entera * signos
matrices_unidas = np.concatenate((matriz1, matriz2), axis=1)
n_columnas = matrices_unidas.shape[1]
orden_actual = np.arange(matrices_unidas.shape[0])
for i in range(n_columnas - 1, -1, -1):
    orden_actual = np.lexsort((orden_actual, matrices_unidas[:, i]))
matriz_final = matrices_unidas[orden_actual]
np.savetxt(carpeta + f"/Datos_{SISTEMA}.dat",
           matriz_final, fmt="%.3f", delimiter="\t")

velocidades_cuadradas = []
for i in range(NPAR):
    velocidad_cuadrada = matriz_final[i, 3]**2 + matriz_final[i, 4]**2
    velocidades_cuadradas.append(velocidad_cuadrada)

maximo = max(velocidades_cuadradas)
minimo = min(velocidades_cuadradas)
rango = maximo - minimo
Ninter = int(1 + 3.3*math.log(len(velocidades_cuadradas)))
amplitud = rango/Ninter
intervalos = [0] * Ninter
frecuencia = [0] * Ninter
media = sum(velocidades_cuadradas)/len(velocidades_cuadradas)

for i in range(Ninter):
    limite = minimo + i*amplitud
    intervalos[i] = limite
    CANTIDAD = 0
    for j in range(NPAR):
        if velocidades_cuadradas[j] != "Na":
            if velocidades_cuadradas[j] < limite:
                CANTIDAD = CANTIDAD + 1
                velocidades_cuadradas[j] = "Na"
    frecuencia[i] = CANTIDAD

plt.bar(intervalos, frecuencia, width=amplitud*0.9, align='edge')
plt.title('Grafica de dispersion de las velocidades')
plt.xlabel('Velocidad al cuadrado')
plt.ylabel('Frecuencia')
plt.axvline(x=media, color='red', linestyle='--', linewidth=1)
ruta_imagen = os.path.join(carpeta, f"Dispersion_vel_ini_{SISTEMA}.png")
plt.savefig(ruta_imagen)
plt.show()
