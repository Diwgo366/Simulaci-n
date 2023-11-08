import random
import math
import numpy as np
import matplotlib.pyplot as plt
import os

SISTEMA = 3
NPAR = 50
LARGO = 10
VELMIN = -20
VELMAX = 20

coordenadas_unicas = set()
while len(coordenadas_unicas) < NPAR:
    fila = (random.randint(0, LARGO), random.randint(0, LARGO))
    if fila not in coordenadas_unicas:
        coordenadas_unicas.add(fila)

matriz1 = list(coordenadas_unicas)
random.shuffle(matriz1)
matriz2 = np.random.randint(0, LARGO, size=(NPAR, 1))
matriz3 = np.random.randint(VELMIN, VELMAX, size=(NPAR, 3))
matriz_final = np.concatenate((matriz1, matriz2, matriz3), axis=1)
np.savetxt(f"Datos/Datos_{SISTEMA}.dat", matriz_final, fmt="%d", delimiter="\t")

print("Matriz guardada")

velocidades_cuadradas = []
for i in range(NPAR):
    velocidad_cuadrada =  matriz_final[i,0]**2 + matriz_final[i,1]**2
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
    cantidad = 0
    for j in range(NPAR):
        if velocidades_cuadradas[j] != "Na":
            if velocidades_cuadradas[j] < limite:
                cantidad = cantidad + 1
                velocidades_cuadradas[j] = "Na"
    frecuencia[i] = cantidad
plt.bar(intervalos, frecuencia, width=amplitud*0.9, align='edge')
plt.title('Grafica de dispersion de las velocidades')
plt.xlabel('Velocidad al cuadrado')
plt.ylabel('Frecuencia')
plt.axvline(x=media, color='red', linestyle='--', linewidth=1)
carpeta = f'Graficas/Sistema_{SISTEMA}'
if not os.path.exists(carpeta):
    os.makedirs(carpeta)
ruta_imagen = os.path.join(carpeta, f"Dispersion_vel_ini_{SISTEMA}.png")
plt.savefig(ruta_imagen)
plt.show()
