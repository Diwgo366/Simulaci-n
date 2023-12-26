"""Programa para simular particulas"""
import math
import os
import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from alive_progress import alive_bar

# Declaración de parámetros
SISTEMA = 1
TIEMPO = 120
DT = 0.04
ANIMAR = False
IMAGENES = False
RESULTADOS = False
GUARDADO = f"{TIEMPO}_{IMAGENES}"

#Lectura de la configuracion
CARPETA = f"Sistemas/Sistema_{SISTEMA}"
RUTA_DATOS = CARPETA + f"/Datos_{SISTEMA}.dat"

def lectura(json_data, variable):
    return json_data.get(variable)

with open(CARPETA + f'/config_{SISTEMA}.json', 'r') as archivo:
    data = json.load(archivo)

PARTICULAS_LADO = lectura(data,"PARTICULAS_LADO")
LONGITUD = lectura(data,"LONGITUD")
MASA = lectura(data,"MASA")
RADIO_CORTE = lectura(data,"RADIO_CORTE")
EPSILON = lectura(data,"EPSILON")
SIGMA = lectura(data,"SIGMA")
NPAR = lectura(data,"NUM_PAR")
UNIDADES = lectura(data, "UNIDADES")

# Obtención de condiciones iniciales
datos = np.loadtxt(RUTA_DATOS)
posicion_x = datos[:, 0]
posicion_y = datos[:, 1]
posicion_z = datos[:, 2]
velocidad_x = datos[:, 3]
velocidad_y = datos[:, 4]
velocidad_z = datos[:, 5]
distancia_media = []
velocidad_cuadrada = []
PARES = NPAR*(NPAR-1)/2

def graficar(vector, variable, nombre):
    """Función para crear gráficas"""
    eje_x = list(range(len(vector)))
    eje_x = [i * DT for i in eje_x]
    carpeta = f'Sistemas/Sistema_{SISTEMA}'
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)
    plt.figure(figsize=(12, 6))
    plt.scatter(eje_x, vector, marker='o', color='red', s=3)
    plt.xlabel('Tiempo')
    plt.ylabel(variable)
    plt.title(f"Tiempo vs {variable}")
    ruta_imagen = os.path.join(carpeta, f'{nombre}.png')
    plt.savefig(ruta_imagen)
    if RESULTADOS:
        plt.show()

def crear_imagenes(part):
    sectores = []
    for z in [LONGITUD, 0, -LONGITUD]:
        for y in [LONGITUD, 0, -LONGITUD]:
            for x in [LONGITUD, 0, -LONGITUD]:
                sector = [np.array(posicion_x) + x, np.array(posicion_y) + y, np.array(posicion_z) + z]
                sectores.append(sector)

    listas = {
        (True, True, True): [0,1,3,4,9,10,12],
        (True, False, True): [3,4,6,7,12,15,16],
        (False, True, True): [1,2,4,5,10,11,14],
        (False, False, True): [4,5,7,8,14,16,17],
        (True, True, False): [9,10,12,18,19,21,22],
        (True, False, False): [12,15,16,21,22,24,25],
        (False, True, False): [14,16,17,22,23,25,26],
        (False, False, False): [10,11,14,19,20,22,23]
    }
    
    condiciones = (posicion_x[part] > LONGITUD/2, posicion_y[part] > LONGITUD/2, posicion_z[part] > LONGITUD/2)
    lista = listas[condiciones]
    
    for indice in lista:
        fuerza_imag_x = 0
        fuerza_imag_y = 0
        fuerza_imag_z = 0
        sector = sectores[indice]
        pos_x_sector = sector[0]
        pos_y_sector = sector[1]
        pos_z_sector = sector[2]
        
        for i in range(NPAR):
            distancia_x = posicion_x[part] - pos_x_sector[i]
            distancia_y = posicion_y[part] - pos_y_sector[i]
            distancia_z = posicion_z[part] - pos_z_sector[i]
            distancia = math.sqrt(distancia_x**2 + distancia_y**2 + distancia_z**2)
            if distancia <= RADIO_CORTE:
                fuerza_imag_x = fuerza_imag_x + 4 * (12*distancia**(-14) - 6*distancia**(-8)) * distancia_x
                fuerza_imag_y = fuerza_imag_y + 4 * (12*distancia**(-14) - 6*distancia**(-8)) * distancia_y
                fuerza_imag_z = fuerza_imag_z + 4 * (12*distancia**(-14) - 6*distancia**(-8)) * distancia_z
    
    return fuerza_imag_x, fuerza_imag_y, fuerza_imag_z

def actualizar_posiciones(part):
    """Función para actualizar las posiciones"""
    fuerza_x = 0
    fuerza_y = 0
    fuerza_z = 0
    distancia_media_parcial = 0
    
    for k in range(NPAR):
        distancia_x = posicion_x[part] - posicion_x[k]
        distancia_y = posicion_y[part] - posicion_y[k]
        distancia_z = posicion_z[part] - posicion_z[k]
        distancia = math.sqrt(distancia_x**2 + distancia_y**2 + distancia_z**2)
        if k > part:
            distancia_media_parcial = distancia_media_parcial + distancia
        if k != part and distancia <= RADIO_CORTE:
            fuerza_x = fuerza_x + 4 * (12*distancia**(-14) - 6*distancia**(-8)) * distancia_x
            fuerza_y = fuerza_y + 4 * (12*distancia**(-14) - 6*distancia**(-8)) * distancia_y
            fuerza_z = fuerza_z + 4 * (12*distancia**(-14) - 6*distancia**(-8)) * distancia_z
    
    if IMAGENES:
        fuerza_x_img, fuerza_y_img, fuerza_z_img = crear_imagenes(part)
        fuerza_x = fuerza_x + fuerza_x_img
        fuerza_y = fuerza_y + fuerza_y_img
        fuerza_z = fuerza_z + fuerza_z_img
    
    velocidad_x[part] = velocidad_x[part] + (fuerza_x / MASA) * DT
    velocidad_y[part] = velocidad_y[part] + (fuerza_y / MASA) * DT
    velocidad_z[part] = velocidad_z[part] + (fuerza_z / MASA) * DT
    posicion_x[part] = posicion_x[part] + velocidad_x[part] * DT
    posicion_y[part] = posicion_y[part] + velocidad_y[part] * DT
    posicion_z[part] = posicion_z[part] + velocidad_z[part] * DT
    return distancia_media_parcial

if ANIMAR:
    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_subplot(111, projection='3d')
    grafico, = ax.plot([], [], [], "o", markersize=5)
    ax.set_xlim(0, LONGITUD)
    ax.set_ylim(0, LONGITUD)
    ax.set_zlim(0, LONGITUD)
    
    def animate(frame):
        """Funcion para animar"""
        for j in range(NPAR):
            _ = actualizar_posiciones(j)
            posicion_x[j] = posicion_x[j] % LONGITUD
            posicion_y[j] = posicion_y[j] % LONGITUD
            posicion_z[j] = posicion_z[j] % LONGITUD
        grafico.set_data(posicion_x, posicion_y)
        grafico.set_3d_properties(posicion_z)
        return grafico,
    
    ani = animation.FuncAnimation(
        fig, animate, frames=int(TIEMPO/DT), blit=True, repeat=False)
    plt.title("Vista 3D")
    plt.show()
else:
    with alive_bar(int(TIEMPO / DT)) as bar:
        for step in range(int(TIEMPO / DT)):
            bar()
            DISTANCIA_MEDIA_TOTAL = 0
            VELOCIDAD_MEDIA = 0
            for i in range(NPAR):
                vel_cua = 0
                dis_par = actualizar_posiciones(i)
                posicion_x[i] = posicion_x[i] % LONGITUD
                posicion_y[i] = posicion_y[i] % LONGITUD
                posicion_z[i] = posicion_z[i] % LONGITUD
                DISTANCIA_MEDIA_TOTAL = DISTANCIA_MEDIA_TOTAL + dis_par
                vel_cua = velocidad_x[i]**2 + velocidad_y[i]**2 + velocidad_z[i]**2
                VELOCIDAD_MEDIA = VELOCIDAD_MEDIA + vel_cua
            distancia_media.append(DISTANCIA_MEDIA_TOTAL/PARES)
            velocidad_cuadrada.append(VELOCIDAD_MEDIA/NPAR)
        graficar(velocidad_cuadrada, "Velocidad al cuadrado", f"Velocidad_cuadrada_{SISTEMA}_{GUARDADO}")
        graficar(distancia_media, "Distancia media", f"Distancia_media_{SISTEMA}_{GUARDADO}")
