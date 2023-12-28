import os
import re
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import tkinter as tk
import numpy as np
from tkinter import ttk

# Declaración de parámetros
SISTEMA = 0
NUM_PART = 5

# Colores de gráfica
color_antes = "green"
color_despues = "blue"
mayor_antes = "yellow"
mayores_despues = "red"

#Carpeta de Alertas
carpeta_principal = f"Sistemas\\Sistema_{SISTEMA}\\Alertas"


indice = 0
# Lista para almacenar las carpetas
carpetas = [os.path.join(carpeta_principal, carpeta) for carpeta in os.listdir(carpeta_principal) if os.path.isdir(os.path.join(carpeta_principal, carpeta))]

#Extrae el numero de alerta y las ordena de acuerdo a ello
def extraer_numero(carpeta):
    nombre_carpeta = os.path.basename(carpeta)
    match = re.search(r'Alerta (\d+)', nombre_carpeta)
    if match:
        numero = int(match.group(1))
        return numero
    return 0

carpetas.sort(key=extraer_numero)

def leer_coordenadas(archivo):
    """Función para leer las coordenadas de cada archivo, devuelve una matriz"""
    with open(archivo, 'r') as f:
        data = f.readlines()
    coords = []
    for line in data:
        coord = list(map(float, line.strip().split()))
        coords.append(coord)
    return np.array(coords)

def calcular_distancias(coords1, coords2):
    """Función para calcular la distancia entre las particulas"""
    return np.sqrt(np.sum((coords1 - coords2)**2, axis=1))

def avanzar():
    """Función para el botón avanzar"""
    global indice
    if indice < len(carpetas) - 1:
        indice += 1
        graficar_carpeta()

def retroceder():
    """Función para el botón retroceder"""
    global indice
    if indice > 0:
        indice -= 1
        graficar_carpeta()

def cerrar():
    """Función para cerrar la ventana"""
    root.quit()
    root.destroy()

#Se crea la figura de la gráfica
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

texto_en_figura = None

def graficar_carpeta():
    """Función para graficar la comparación de coordenadas"""
    global ax, texto_en_figura
    ax.cla()
    carpeta = carpetas[indice]
    nombre_carpeta = os.path.basename(carpeta) 
    coords1 = leer_coordenadas(os.path.join(carpeta, 'antiguas.dat'))
    coords2 = leer_coordenadas(os.path.join(carpeta, 'nuevas.dat'))
    distancias = calcular_distancias(coords1, coords2)
    
    # Ordenar las distancias
    mayor_mov = np.argsort(distancias)[-NUM_PART:]
    menor_mov = np.array([i for i in range(len(distancias)) if i not in mayor_mov])
    
    # Grafica las particulas que no se han movido más
    ax.scatter(coords1[menor_mov, 0], coords1[menor_mov, 1], coords1[menor_mov, 2], c = color_antes, s = 10, marker='o')
    ax.scatter(coords2[menor_mov, 0], coords2[menor_mov, 1], coords2[menor_mov, 2], c = color_despues, s = 10, marker='o')
    
    # Grafica las partículas que se han movido más
    ax.scatter(coords1[mayor_mov, 0], coords1[mayor_mov, 1], coords1[mayor_mov, 2], c = mayor_antes, s = 10, marker='o')
    ax.scatter(coords2[mayor_mov, 0], coords2[mayor_mov, 1], coords2[mayor_mov, 2], c = mayores_despues, s = 10, marker='o')

    # Añade el número de partícula como anotación
    for i in range(len(mayor_mov)):
        ax.text(coords1[mayor_mov[i], 0] + 0.5, coords1[mayor_mov[i], 1] + 0.5, coords1[mayor_mov[i], 2] +0.5 , str(mayor_mov[i]))
        ax.text(coords2[mayor_mov[i], 0] + 0.5, coords2[mayor_mov[i], 1] + 0.5, coords2[mayor_mov[i], 2] + 0.5 , str(mayor_mov[i]))

    if texto_en_figura:
        texto_en_figura.remove()
    texto_en_figura = plt.figtext(0.05, 0.95, f"Datos extraídos de la {nombre_carpeta}", verticalalignment='top')
    canvas.draw()

# Crear la interfaz
root = tk.Tk()
root.title("Visualizador de datos")

# Estilo de los botones
style = ttk.Style()
style.configure("TButton",
                foreground="midnight blue",
                background="light sky blue",
                font=("Helvetica", 16),
                padding=10)

# Se modifican los grid
root.grid_rowconfigure(0, weight=1)

root.grid_columnconfigure(0, weight=1) 
root.grid_columnconfigure(1, weight=0)
root.grid_columnconfigure(2, weight=0)

root.grid_columnconfigure(0, minsize=600)
root.grid_columnconfigure(1, minsize=80)
root.grid_columnconfigure(2, minsize=80)

# Se ubican los botones
boton_avanzar = ttk.Button(root, text="Avanzar", command=avanzar)
boton_retroceder = ttk.Button(root, text="Retroceder", command=retroceder)
boton_avanzar.grid(row=1, column=2)
boton_retroceder.grid(row=1, column=1)

# Crea el gráfico y lo añade a la interfaz
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(row=0, column=0, columnspan=3, sticky='nsew')

# Añade la barra de herramientas
toolbar_frame = tk.Frame(root)
toolbar_frame.grid(row=1, column=0)
toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)

# Inicia el programa
graficar_carpeta()
root.protocol("WM_DELETE_WINDOW", cerrar)
root.mainloop()
