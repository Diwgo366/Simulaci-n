"""Programa para simular particulas"""
import math
import numpy as np
import matplotlib.animation as animation
import matplotlib.pyplot as plt

# Declaración de parámetros
TIEMPO = 1
DT = 0.01
IMAGENES = 3
LONGITUD = 10
MASA = 1
RADIO_CORTE = 4
EPSILON = 1
GAMA = 1
ANIMAR = True
RUTA_DATOS = "Datos.dat"

# Obtención de condiciones iniciales
datos = np.loadtxt(RUTA_DATOS)
posicion_x = datos[:, 0]
posicion_y = datos[:, 1]
velocidad_x = datos[:, 2]
velocidad_y = datos[:, 3]
distancia_media = []
NPAR = len(posicion_x)
PARES = NPAR*(NPAR-1)/2

def graficar(vector, variable):
    """Función para crear imagenes"""
    eje_x = list(range(len(vector)))
    eje_x = [i * DT for i in eje_x]
    plt.scatter(eje_x, vector, marker='o', color='red', s=10)
    plt.xlabel('Tiempo')
    plt.ylabel(variable)
    plt.show()

def actualizar_posiciones(act_pos_x, act_pos_y, act_vel_x, act_vel_y, part):
    """Función para actualizar las posiciones"""
    fuerza_x = 0
    fuerza_y = 0
    distancia_media_parcial = 0
    for i in range(NPAR):
        distancia_x = posicion_x[part] - posicion_x[i]
        distancia_y = posicion_y[part] - posicion_y[i]
        distancia = math.sqrt(distancia_x**2 + distancia_y**2)
        if i > part:
            distancia_media_parcial = distancia_media_parcial + distancia
        if i != part and distancia <= RADIO_CORTE:
            fuerza_x = fuerza_x + 24*EPSILON*GAMA**6 * \
                (2*GAMA**6*distancia**(-14)-distancia**(-8))*distancia_x
            fuerza_y = fuerza_y + 24*EPSILON*GAMA**6 * \
                (2*GAMA**6*distancia**(-14)-distancia**(-8))*distancia_y
    acl_x = fuerza_x / MASA
    acl_y = fuerza_y / MASA
    act_vel_x = act_vel_x + acl_x * DT
    act_vel_y = act_vel_y + acl_y * DT
    act_pos_x = act_pos_x + act_vel_x * DT
    act_pos_y = act_pos_y + act_vel_y * DT
    return act_pos_x, act_pos_y, distancia_media_parcial

if ANIMAR:
    fig = plt.figure(figsize=(6, 6))
    grafico, = plt.plot([], [], "o", markersize=5)
    plt.xlim(0 - LONGITUD*(IMAGENES-1)/2, LONGITUD + LONGITUD*(IMAGENES-1)/2)
    plt.ylim(0 - LONGITUD*(IMAGENES-1)/2, LONGITUD + LONGITUD*(IMAGENES-1)/2)
    for i in range(IMAGENES):
        x = i * LONGITUD
        plt.axvline(x, color='red', linestyle='--', alpha=0.5)
    for i in range(IMAGENES):
        y = i * LONGITUD
        plt.axhline(y, color='red', linestyle='--', alpha=0.5)
    def animate(frame):
        """Funcion para animar"""
        distancia_media_total1 = 0
        for i in range(NPAR):
            posicion_x[i], posicion_y[i], media_par1 = actualizar_posiciones(
                posicion_x[i], posicion_y[i], velocidad_x[i], velocidad_y[i], i)
            posicion_x[i] = posicion_x[i] % LONGITUD
            posicion_y[i] = posicion_y[i] % LONGITUD
            distancia_media_total1 = distancia_media_total1 + media_par1
        distancia_media.append(distancia_media_total1/PARES)
        grafico.set_data(posicion_x, posicion_y)
        return grafico,
    ani = animation.FuncAnimation(
        fig, animate, frames=int(TIEMPO/DT), blit=True)
    plt.show()
else:
    for step in range(int(TIEMPO / DT)):
        distancia_media_total2 = 0
        for i in range(NPAR):
            posicion_x[i], posicion_y[i], media_par2 = actualizar_posiciones(
                posicion_x[i], posicion_y[i], velocidad_x[i], velocidad_y[i], i)
            posicion_x[i] = posicion_x[i] % LONGITUD
            posicion_y[i] = posicion_y[i] % LONGITUD
            distancia_media_total2 = distancia_media_total2 + media_par2
        distancia_media.append(distancia_media_total2/PARES)
    graficar(distancia_media, "Distancia media")
    