"""Programa para crear los datos iniciales"""
import math
import os
import json
import matplotlib.pyplot as plt
import numpy as np

#Seleccionar el sistema a trabajar
SISTEMA = 1

#Introducción de parametros
SIGMA = 1       # m
EPSILON = 1     # kg m² s-²
MASA = 1        # kg
PAR_LADO = 3
M = 10
VEL = 0
DES_VEL = 0.01
DECIMALES = 10

#Calculo de parametros adicionales
NPAR = PAR_LADO**3
RADIO_CORTE = M*SIGMA
LONGITUD = 2*RADIO_CORTE
PART_DISTANCIA = LONGITUD/PAR_LADO
TAU = math.sqrt((SIGMA**2*MASA**2)/EPSILON) #s

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
for i in range(PAR_LADO):
    for j in range(PAR_LADO):
        for k in range(PAR_LADO):
            fila = (PART_DISTANCIA/2 + PART_DISTANCIA*i, PART_DISTANCIA/2 + PART_DISTANCIA*j, PART_DISTANCIA/2 + PART_DISTANCIA*k)
            coordenadas_unicas.append(fila)
matriz1 = coordenadas_unicas

#Crea valores para las velocidades con distribucion gaussiana
matriz2 = np.round(np.random.normal(VEL, DES_VEL, size=(NPAR, 3)), DECIMALES)
#Une ambas matrices y las ordena
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

#Actualizar velocidades para tener velocidad media de 0
for i in range(3,6):
    media = (np.sum(matriz_final[:,i]))/(len(matriz_final[:,i]))
    for j in range (len(matriz_final[:,i])):
        matriz_final[j,i] = round(matriz_final[j,i] - media, DECIMALES)

#Se guarda la nueva matriz
np.savetxt(carpeta + f"/Datos_{SISTEMA}.dat",
           matriz_final, fmt=f"%.{DECIMALES}f", delimiter="\t")

#Crea grafico para mostrar la frecuencia de las velocidades
grafica_dispersion(matriz_final[:,3], "Velocidades en x", "vel_ini_x")
grafica_dispersion(matriz_final[:,4], "Velocidades en y", "vel_ini_y")
grafica_dispersion(matriz_final[:,5], "Velocidades en z", "vel_ini_z")

#Guarda las configuraciones para su ejecucioMASAn
configuracion = {
    "NUM_PAR": NPAR,
    "PARTICULAS_LADO": PAR_LADO,
    "LONGITUD": LONGITUD,
    "DESVIACION": DES_VEL,
    "RADIO_CORTE": RADIO_CORTE,
    "MASA": MASA,
    "EPSILON": EPSILON,
    "SIGMA": SIGMA,
    "TAU": TAU,
    "UNIDADES": round(EPSILON/SIGMA, DECIMALES),
}

with open(carpeta+f'/config_{SISTEMA}.json', 'w') as file:
    json.dump(configuracion, file, indent=4)

print("Datos creados exitosamente")
print(f"Numero de particulas: {NPAR}")