import numpy as np
import heapq #proporciona una implementación de heap queue (cola de prioridad basada en montículos).

# PASO1: funcion para que las filas y columnas puedan variar mas facilmente
def crear_mapa(filas, columnas):
    return np.zeros((filas,columnas), dtype=int)

# PASO5: funcion para que la coordenada ingresada por el usuario pueda ser modificada a 1
def agregar_obstaculo(mapa, x, y):
     mapa[x,y] = 1

# PASO10: funcion para que la coordenada ingresada por el usuario pueda ser modificada a 2 
def agregar_punto_partida(mapa, x_inicio, y_inicio):
    mapa[x_inicio,y_inicio] = 2

# PASO11: funcion para que la coordenada ingresada por el usuario pueda ser modificada a 3
def agregar_destino(mapa, x_fin, y_fin):
    mapa[x_fin,y_fin] = 3

# Paso12: funcion para calcular la distancia entre dos puntos
def obtener_distancia(pos_a, pos_b):
    return abs(pos_a[0] - pos_b[0]) + abs(pos_a[1] - pos_b[1])

# Paso13: funcion para calcular las posiciones de los vecinos de la cordenada actual
def obtener_vecinos(mapa,pos_actual):
    vecinos = []
    for direccion_x, direccion_y in [(0,1),(1,0),(0,-1),(-1,0)]: # 4 direcciones
        x,y = pos_actual[0] + direccion_x, pos_actual[1] + direccion_y

        if 0 <= x < filas and 0 <= y < columnas and mapa[x,y] != 1: #verificar que este dentro del mapa y no sea un obstaculo
            vecinos.append((x,y)) # agrega cada nuevo elemento al final de la lista

    return vecinos

# PASO14: Funcion principal. Implementacion del algoritmo A*  
def encontrar_camino(mapa, punt_partida, destino):
    puntaje_g = {punt_partida: 0} # la coordenada inicial comienza con puntuacion 0
    puntaje_f = {punt_partida: obtener_distancia(punt_partida,destino)} 
    list_abierta = [{0, punt_partida}] # el menor costo que se obtine de puntaje_g inicia con 0
    vino_desde = {}

    while list_abierta:
        # Mientras haya cordenadas en la lista abierta se saca la corrdenada con menor puntaje_f
        punt_actual_f, pos_actual = heapq.heappop(list_abierta)

        # Si la posicion actual es el destino, se reconstruye y devuelve el camino.
        if pos_actual == destino:
            camino = []

            while pos_actual in vino_desde:
                camino.append(pos_actual)
                pos_actual = vino_desde[pos_actual]
            camino.append(punt_partida)
            return camino[::-1]

        # Si no, se exploran los vecinos del nodo actual.

        # Para cada vecino, se calcula un g_score tentativo.
        for vecinos in obtener_vecinos(mapa, pos_actual):
            punt_tentativo_g = puntaje_g[pos_actual] + 1  # Asumimos costo de 1 para moverse

            # Si este puntaje_g es mejor que el anterior conocido, se actualiza la información del vecino.
            if vecinos not in puntaje_g or punt_tentativo_g < puntaje_g[vecinos]:
                vino_desde[vecinos] = pos_actual
                puntaje_g[vecinos] = punt_tentativo_g
                puntaje_f[vecinos] = puntaje_g[vecinos] + obtener_distancia(vecinos,destino)

                # Se añade el vecino a list_abierta con su puntaje_f actualizado.
                heapq.heappush(list_abierta,(puntaje_f[vecinos],vecinos))

    return None # Si no se encuentra un camino, se devuelve None.

#PASO18: Mejorar la presentacion del mapa
    #Paso 18.1 Función para convertir el mapa numérico en una representación de caracteres
def agregar_simbolos(mapa):
    # Guardamos en el diccionario los numeros como claves y lo simbolos como valores
    simbolos = {
        0: '\u25A1',  # Espacio vacío (□)
        1: '\u25A0',  # Obstáculo (■)
        2: 'p',       # Punto de partida 
        3: 'D',       # Destino 
        4: '\u25CF'   # Camino (●)
    }
    return np.array([[simbolos.get(celda, str(celda)) for celda in fila] for fila in mapa])

    # Paso 18.2: Modificar la funcion para imprimir el mapa
def imprimir_mapa(mapa):
    mapa_convertido = agregar_simbolos(mapa)
    for fila in mapa_convertido:
        print(' '.join(fila)) # para dar espacio entre elementos
        
# PASO2: Solicitar al usuario que ingrese las dimenciones del mapa y validamos que los datos ingresados sean correctos
# Utiliza un bucle while con manejo de excepciones para asegurarse de que el usuario ingrese números enteros positivos válidos.
while True:
    
    try:
        
        print("Ingrese las dimensiones del mapa")

        #Solicitar al usuarios que ingrese el numero de filas
        filas = int(input("Numero de Filas: "))

        #Numero de columnas
        columnas = int(input("Numero de Columnas: "))

        if filas > 0 and columnas > 0:
            break
        else:
            print()
            print("Error: (┬┬﹏┬┬) Solo se aceptan numeros positivos. Intentelo nuevamente")
            print()
       
    except ValueError:
            print()
            print("Error: Ambos valores deben ser numeros enteros. Intentelo nuevamente ( ´･･)ﾉ(._.`)")
            print()


# PASO3: Crear una variable y llamamos a funcion crear_mapa enviandole los paramentros de filas y columnas
mapa = crear_mapa(filas, columnas)

# PASO4: Imprimir mapa original
print()
print("Mapa Creado ╰(*°▽°*)╯")
#print(mapa)
imprimir_mapa(mapa)
print()


# PASO6: Solicitar al usuario que ingrese las cordenadas en donde quiera agregar un obstaculo y validamos que los datos ingresados sean correctos
while True:
    try:
        respuesta = input("Desea agregar un obstaculo? (s = si / n = no): ").lower() #lower() para aceptar respuestas en minusculas y mayusculas
        if respuesta != 's':
            break

        x = int(input(f"Ingrese la cordenada x ( de 0 a {filas-1}): "))
        y = int(input(f"Ingrese la cordenada y (de 0 a {columnas - 1}): "))

        # Verificamos que las corrdenadas esten dentro del rango y le pasamos los parametros a la funcion agregar_obstaculo
        if 0 <= x < filas and 0 <= y < columnas and mapa[x,y] != 1:
             agregar_obstaculo(mapa, x, y)
        else:
             print()
             print("Cordenadas fuera de rando o ya fue elegido como obstaculo (⊙_⊙;)")
             print()

    except ValueError:
        print()
        print("Error: Ambos valores deben ser numeros enteros. Intentelo nuevamente ( ´･･)ﾉ(._.`)")
        print()

# PASO7: Imprimir mapa con obstaculos
print()
print("Mapa Creado ╰(*°▽°*)╯")
#print(mapa)
imprimir_mapa(mapa)

# PASO8: Solicitamos al usuario que ingrese el punto de inicio como coordenadas
while True:
    try:
        print()
        print("Ingrese el punto de partida")
        x_inicio = int(input(f"Ingrese la cordenada x ( de 0 a {filas-1}): "))
        y_inicio = int(input(f"Ingrese la cordenada y (de 0 a {columnas-1}): "))

        # Verificamos que las cordenadas esten dentro del rango y le pasamos los parametros a la funcion agregar_punto_partida
        if 0 <= x_inicio < filas and 0 <= y_inicio < columnas and mapa[x_inicio, y_inicio] != 1:
            agregar_punto_partida(mapa, x_inicio, y_inicio)
            break
             
        else:
            print()
            print("Cordenadas fuera de rando o ya fue elegido como obstaculo (⊙_⊙;)")

    except ValueError:
        print()
        print("Error: Ambos valores deben ser numeros enteros. Intentelo nuevamente ( ´･･)ﾉ(._.`)")
        print()

# PASO9: Solicitamos al usuario que ingrese el destino como coordenadas
while True:
    try:
        
        print()
        print("Ingrese el destino")
        x_fin = int(input(f"Ingrese la cordenada x ( de 0 a {filas-1}): "))
        y_fin = int(input(f"Ingrese la cordenada y (de 0 a {columnas-1}): "))

        # Verificamos que las cordenadas esten dentro del rango y le pasamos los parametros a la funcion agregar_destino
        if 0 <= x_fin < filas and 0 <= y_fin < columnas and mapa[x_fin, y_fin] != 1:
            agregar_destino(mapa, x_fin, y_fin)
            break
             
        else:
            print()
            print("Cordenadas fuera de rando o ya fue elegido como obstaculo (⊙_⊙;)")
            print()

    except ValueError:
        print()
        print("Error: Ambos valores deben ser numeros enteros. Intentelo nuevamente ( ´･･)ﾉ(._.`)")
        print()

# PASO10: Imprimir mapa final
print()
print("Mapa Creado ╰(*°▽°*)╯")
#print(mapa)
imprimir_mapa(mapa)

# PASO15: crear variables que recibiran las coordenadas del punto de partida y el destino
punt_partida = (x_inicio, y_inicio)
destino = (x_fin, y_fin)

# PASO16: llamar a la funcion principal 
camino = encontrar_camino(mapa, punt_partida, destino)


# PASO17: imprimir camino y mostrar mensaje en caso haber encontrado un camino
if camino:
    print(f"Puedes ir de {punt_partida} a {destino} tomando este camino ☜(ﾟヮﾟ☜)")

    for x, y in camino:
        if (x,y) != punt_partida and (x, y) != destino:
            mapa[x,y] = 4 # Marcar el camino con puntos
    #print(mapa)
    imprimir_mapa(mapa) 
else:
    print("No se encontro un camino.")

            