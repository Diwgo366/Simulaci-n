"""Programa para crear los datos iniciales"""
import math
import os
import shutil
import json
import matplotlib.pyplot as plt
import numpy as np
from colorama import Fore, Style

#Seleccionar el sistema a trabajar
SISTEMA = 3

#Introducción de parametros
PAR_LADO = 2
DES_VEL = 1
MASA = 1
RADIO_CORTE = 10
DELTA_ORIGEN = 2                # Distancia al origen
UND_LONGITUD = 2.405*10**-10    # m
UND_ENERGIA = 165.324*10**-23   # kg m² s-²
UND_MASA = 1                    # kg
BOLTZMANN= 1.38*10**-23         # kg m² s-² K-¹
T = 0.5

#Calculo de parametros adicionales
VEL = 0
NPAR = 4*PAR_LADO**3
LONGITUD = 2*RADIO_CORTE
PART_DISTANCIA = LONGITUD/PAR_LADO
UND_TIEMPO = math.sqrt((UND_LONGITUD**2*MASA)/UND_ENERGIA)  # s
UND_FUERZA = UND_ENERGIA/UND_LONGITUD                       # kg m s-²
UND_TEMPERATURA = UND_ENERGIA/BOLTZMANN                     # K

#Verifica o crea la ubicacion del sistema
carpeta = f'Sistemas/Sistema_{SISTEMA}'
if not os.path.exists(carpeta):
    os.makedirs(carpeta)

#Limpia la carpeta anterior
try:
    if os.path.exists(carpeta):
        shutil.rmtree(carpeta)
        os.makedirs(carpeta)
except Exception as e:
    print(f"Error: {e}")

#Crea la matriz de datos

#Crea posiciones de forma homogénea
coordenadas_unicas = []
for i in range(PAR_LADO):
    for j in range(PAR_LADO):
        for k in range(PAR_LADO):
            fila = (DELTA_ORIGEN + PART_DISTANCIA/2 + PART_DISTANCIA*i, DELTA_ORIGEN + PART_DISTANCIA/2 + PART_DISTANCIA*j, DELTA_ORIGEN + PART_DISTANCIA/2 + PART_DISTANCIA*k)
            coordenadas_unicas.append(fila)
            
            fila = (DELTA_ORIGEN + PART_DISTANCIA + PART_DISTANCIA*i, DELTA_ORIGEN + PART_DISTANCIA + PART_DISTANCIA*j, DELTA_ORIGEN + PART_DISTANCIA/2 + PART_DISTANCIA*k)
            coordenadas_unicas.append(fila)
            
            fila = (DELTA_ORIGEN + PART_DISTANCIA + PART_DISTANCIA*i, DELTA_ORIGEN + PART_DISTANCIA/2 + PART_DISTANCIA*j, DELTA_ORIGEN + PART_DISTANCIA + PART_DISTANCIA*k)
            coordenadas_unicas.append(fila)
            
            fila = (DELTA_ORIGEN + PART_DISTANCIA/2 + PART_DISTANCIA*i, DELTA_ORIGEN + PART_DISTANCIA + PART_DISTANCIA*j, DELTA_ORIGEN + PART_DISTANCIA + PART_DISTANCIA*k)
            coordenadas_unicas.append(fila)
            
matriz1 = coordenadas_unicas

#Crea valores para las velocidades con distribucion gaussiana
matriz2 = np.random.normal(VEL, DES_VEL, size=(NPAR, 3))
#Une ambas matrices
matriz_final = np.concatenate((matriz1, matriz2), axis=1)

#Definir una funcion para graficar las diferentes dispersiones
def grafica_dispersion(vector, nombre, guardado):
    lista = []
    for i in range(NPAR):
        lista.append(vector[i])
    #Calculo de los datos para graficar
    maximo = max(vector)
    minimo = min(vector)
    rango = maximo - minimo
    Ninter = int(1 + 3.3*math.log(len(vector)))
    amplitud = rango/Ninter
    intervalos = [0] * Ninter
    frecuencia = [0] * Ninter
    media = sum(vector)/len(vector)

    #Se realiza el recuento de cada intervalo
    for i in range(Ninter):
        limite = minimo + i*amplitud
        intervalos[i] = limite
        CANTIDAD = 0
        for j in range(NPAR):
            if lista[j] != "Na":
                if lista[j] < limite:
                    CANTIDAD = CANTIDAD + 1
                    lista[j] = "Na"
        frecuencia[i] = CANTIDAD

    #Se grafica la dispersion
    plt.bar(intervalos, frecuencia, width=amplitud*0.95, align='edge')
    plt.title("Grafica de dispersion de las " + nombre)
    plt.xlabel(nombre)
    plt.ylabel('Frecuencia')
    plt.axvline(x=media, color='red', linestyle='--', linewidth=1)
    ruta_imagen = os.path.join(carpeta,"Dispersiones/")
    if not os.path.exists(ruta_imagen):
        os.makedirs(ruta_imagen)
    plt.savefig(ruta_imagen + guardado)
    plt.close()

#Actualiza velocidades para la velocidad media = 0
for i in range(3,6):
    media = (np.sum(matriz_final[:,i]))/(len(matriz_final[:,i]))
    for j in range (len(matriz_final[:,i])):
        matriz_final[j,i] = matriz_final[j,i] - media

sum_cuadrados = 0
for i in range (NPAR):
    sum_cuadrados += matriz_final[i,3]**2 + matriz_final[i,4]**2 + matriz_final[i,5]**2

parametro_escala = math.sqrt((3*(NPAR-1))/(sum_cuadrados))*math.sqrt(T)

for i in range (NPAR):
    for j in range(3,6):
        matriz_final[i,j] = matriz_final[i,j]*parametro_escala
        
#Se guarda la matriz
np.savetxt(carpeta + f"/Datos_{SISTEMA}.dat", matriz_final, delimiter="\t")

#Crea grafico para mostrar la frecuencia de las velocidades
grafica_dispersion(matriz_final[:,3], "Velocidades en x", "vel_ini_x")
grafica_dispersion(matriz_final[:,4], "Velocidades en y", "vel_ini_y")
grafica_dispersion(matriz_final[:,5], "Velocidades en z", "vel_ini_z")

#Guarda las configuraciones para su ejecución
configuracion = {
    "NUM_PAR": NPAR,
    "PARTICULAS_LADO": PAR_LADO,
    "LONGITUD": LONGITUD,
    "DESVIACION": DES_VEL,
    "RADIO_CORTE": RADIO_CORTE,
    "MASA": MASA,
    "UND_MASA": UND_MASA,
    "UND_ENERGIA": UND_ENERGIA,
    "UND_LONGITUD": UND_LONGITUD,
    "UND_TIEMPO": UND_TIEMPO,
    "UND_FUERZA": UND_FUERZA,
    "UND_TEMPERATURA": UND_TEMPERATURA,
}

with open(carpeta+f'/config_{SISTEMA}.json', 'w') as file:
    json.dump(configuracion, file, indent=4)

print(Fore.GREEN + "Partículas creadas exitosamente: " + Fore.YELLOW + f"{NPAR}" + Style.RESET_ALL)
