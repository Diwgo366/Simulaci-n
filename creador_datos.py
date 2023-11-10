"""Programa para crear los datos iniciales"""
import math
import os
import json
import random
import matplotlib.pyplot as plt
import numpy as np

SISTEMA = 1
NPAR = 50
LONGITUD = 10
VEL = 0.05
DES_VEL = 0.01

#Verifica o crea la ubicacion del sistema
carpeta = f'Sistemas/Sistema_{SISTEMA}'
if not os.path.exists(carpeta):
    os.makedirs(carpeta)

#Limpia las imagenes del sistema anterior
try:
    archivos = os.listdir(carpeta)
    for archivo in archivos:
        if archivo.endswith(".png"):
            ruta_completa = os.path.join(carpeta, archivo)
            os.remove(ruta_completa)
except Exception as e:
        print(f"Error: {e}")

#Crea la matriz de datos

#Crea posiciones que no se repitan
coordenadas_unicas = []
while len(coordenadas_unicas) < NPAR:
    fila = (round(random.uniform(0, LONGITUD), 6), round(
        random.uniform(0, LONGITUD), 6), round(random.uniform(0, LONGITUD), 6))
    if fila not in coordenadas_unicas:
        coordenadas_unicas.append(fila)
matriz1 = coordenadas_unicas

#Crea valores para las velocidades con distribucion gaussiana
valores = np.round(np.random.normal(VEL, DES_VEL, size=(NPAR, 3)), 6)
signos = np.random.choice([-1, 1], size=(NPAR, 3))
matriz2 = valores * signos

#Une ambas matrices y las ordena
matrices_unidas = np.concatenate((matriz1, matriz2), axis=1)
n_columnas = matrices_unidas.shape[1]
orden_actual = np.arange(matrices_unidas.shape[0])
for i in range(n_columnas - 1, -1, -1):
    orden_actual = np.lexsort((orden_actual, matrices_unidas[:, i]))
matriz_final = matrices_unidas[orden_actual]
np.savetxt(carpeta + f"/Datos_{SISTEMA}.dat",
           matriz_final, fmt="%.3f", delimiter="\t")

#Crea grafico para mostrar la frecuencia de las velocidades
velocidades_cuadradas = []
for i in range(NPAR):
    velocidad_cuadrada = matriz_final[i, 3]**2 + matriz_final[i, 4]**2 + + matriz_final[i, 5]**2
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

#Guarda las configuraciones para su ejecucion
configuracion = {
    "NUM_PAR": NPAR,
    "LONGITUD": LONGITUD,
    "MEDIA": round(media,6),
    "DESVIACION": DES_VEL,
    "IMAGENES": 1,
    "MASA": 1,
    "RADIO_CORTE": round(2*LONGITUD/3,6),
    "EPSILON": 1,
    "GAMA": 1,
}
with open(carpeta+f'/config_{SISTEMA}.json', 'w') as file:
    json.dump(configuracion, file, indent=4)
