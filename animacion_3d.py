"""Programa para simular particulas"""
import math
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Declaración de parámetros
SISTEMA = 4
TIEMPO = 10
DT = 0.01
IMAGENES = 1
LONGITUD = 10
MASA = 1
RADIO_CORTE = 7
EPSILON = 1
GAMA = 1
ANIMAR = False
RUTA_DATOS = f"Sistemas/Sistema_{SISTEMA}/Datos_{SISTEMA}.dat"

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
NPAR = len(posicion_x)
PARES = NPAR*(NPAR-1)/2

def graficar(vector, variable, nombre):
    """Función para crear imagenes"""
    eje_x = list(range(len(vector)))
    eje_x = [i * DT for i in eje_x]
    carpeta = f'Sistemas/Sistema_{SISTEMA}'
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)
    plt.figure(figsize=(12, 6))
    plt.scatter(eje_x, vector, marker='o', color='red', s=5)
    plt.xlabel('Tiempo')
    plt.ylabel(variable)
    plt.title(f"Tiempo vs {variable}")
    ruta_imagen = os.path.join(carpeta, f'{nombre}.png')
    plt.savefig(ruta_imagen)
    plt.show()

def actualizar_posiciones(act_pos_x, act_pos_y, act_pos_z, act_vel_x, act_vel_y, act_vel_z, part):
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
            fuerza_x = fuerza_x + 24*EPSILON*GAMA**6 * \
                (2*GAMA**6*distancia**(-14)-distancia**(-8)) * distancia_x
            fuerza_y = fuerza_y + 24*EPSILON*GAMA**6 * \
                (2*GAMA**6*distancia**(-14)-distancia**(-8)) * distancia_y
            fuerza_z = fuerza_z + 24*EPSILON*GAMA**6 * \
                (2*GAMA**6*distancia**(-14)-distancia**(-8)) * distancia_z
    acl_x = fuerza_x / MASA
    acl_y = fuerza_y / MASA
    acl_z = fuerza_z / MASA
    act_vel_x = act_vel_x + acl_x * DT
    act_vel_y = act_vel_y + acl_y * DT
    act_vel_z = act_vel_z + acl_z * DT
    act_pos_x = act_pos_x + act_vel_x * DT
    act_pos_y = act_pos_y + act_vel_y * DT
    act_pos_z = act_pos_z + act_vel_z * DT
    return act_pos_x, act_pos_y, act_pos_z, distancia_media_parcial

if ANIMAR:
    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_subplot(111, projection='3d')
    grafico, = ax.plot([], [], [], "o", markersize=5)
    ax.set_xlim(0 - LONGITUD*(IMAGENES-1)/2,
                LONGITUD + LONGITUD*(IMAGENES-1)/2)
    ax.set_ylim(0 - LONGITUD*(IMAGENES-1)/2,
                LONGITUD + LONGITUD*(IMAGENES-1)/2)
    ax.set_zlim(0 - LONGITUD*(IMAGENES-1)/2,
                LONGITUD + LONGITUD*(IMAGENES-1)/2)
    def animate(frame):
        """Funcion para animar"""
        distancia_media_total1 = 0
        for j in range(NPAR):
            posicion_x[j], posicion_y[j], posicion_z[j], media_par1 = actualizar_posiciones(
                posicion_x[j], posicion_y[j], posicion_z[j],
                velocidad_x[j], velocidad_y[j], velocidad_z[j], j)
            posicion_x[j] = posicion_x[j] % LONGITUD
            posicion_y[j] = posicion_y[j] % LONGITUD
            posicion_z[j] = posicion_z[j] % LONGITUD
            distancia_media_total1 = distancia_media_total1 + media_par1
        distancia_media.append(distancia_media_total1/PARES)
        grafico.set_data(posicion_x, posicion_y)
        grafico.set_3d_properties(posicion_z)
        return grafico,
    ani = animation.FuncAnimation(
        fig, animate, frames=int(TIEMPO/DT), blit=True, repeat=False)
    plt.title("Vista 3D")
    plt.show()
else:
    for step in range(int(TIEMPO / DT)):
        DISTANCIA_MEDIA_TOTAL2 = 0
        for i in range(NPAR):
            posicion_x[i], posicion_y[i], posicion_z[i], media_par2 = actualizar_posiciones(
                posicion_x[i], posicion_y[i], posicion_z[i],
                velocidad_x[i], velocidad_y[i], velocidad_z[i], i)
            posicion_x[i] = posicion_x[i] % LONGITUD
            posicion_y[i] = posicion_y[i] % LONGITUD
            posicion_z[i] = posicion_z[i] % LONGITUD
            DISTANCIA_MEDIA_TOTAL2 = DISTANCIA_MEDIA_TOTAL2 + media_par2
        distancia_media.append(DISTANCIA_MEDIA_TOTAL2/PARES)
    graficar(distancia_media, "Distancia media", f"Distancia_media_{SISTEMA}")
