# Reversi

import random
import sys
import os

size = 3

def dibujarTablero(tablero):
    # Esta funcion dibuja el tablero recibido. Devuelve None.

    str1 = ""
    print (" " + str1.join(['   ' + str(x) for x in range(size)]))
    str2 = ""
    LINEAH = "  +" + str2.join(['---+' + str1 for _ in range(size)])


    print(LINEAH)
    for y in range(size):
        print(y+1, end=' ')
        for x in range(size):
            print('| %s' % (tablero[x][y]), end=' ')
        print('|')
        print(LINEAH)


def reiniciarTablero(tablero):
    # Deja en blanco el tablero recibido como argumento, excepto la posición inicial.
    for x in range(size):
        for y in range(size):
            tablero[x][y] = ' '

    # Piezas iniciales:
    tablero[int(size/2 - 1)][int(size/2 - 1 )] = 'X'
    tablero[int(size/2 - 1)][int(size/2)] = 'O'
    tablero[int(size/2)][int(size/2 - 1)] = 'O'
    tablero[int(size/2)][int(size/2)] = 'X'


def obtenerNuevoTablero():
    # Crea un tablero nuevo, vacío.
    tablero = []
    for i in range(size):
        tablero.append([' '] * size)

    return tablero


def esJugadaVálida(tablero, baldosa, comienzox, comienzoy):
    # Devuelve False si la jugada del jugador en comienzox, comienzoy es invalida.
    # Si es una jugada válida, devuelve una lista de espacios que pasarían a ser del jugador si moviera aquí.
    if tablero[comienzox][comienzoy] != ' ' or not estáEnTablero(comienzox, comienzoy):
        return False

    tablero[comienzox][comienzoy] = baldosa # coloca temporariamente la baldosa sobre el tablero.

    if baldosa == 'X':
        otraBaldosa = 'O'
    else:
        otraBaldosa = 'X'

    baldosasAConvertir = []
    for direcciónx, direccióny in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
        x, y = comienzox, comienzoy
        x += direcciónx # primer paso en la dirección
        y += direccióny # primer paso en la dirección
        if estáEnTablero(x, y) and tablero[x][y] == otraBaldosa:
            # Hay una pieza perteneciente al otro jugador al lado de nustra pieza
            x += direcciónx
            y += direccióny
            if not estáEnTablero(x, y):
                continue
            while tablero[x][y] == otraBaldosa:
                x += direcciónx
                y += direccióny
                if not estáEnTablero(x, y): # sale del bucle while y continua en el bucle for.
                    break
            if not estáEnTablero(x, y):
                continue
            if tablero[x][y] == baldosa:
                # Hay fichas a convertir. Caminar en dirección opuesta hasta llegar al casillero original, registrando todas las posiciones en el camino.
                while True:
                    x -= direcciónx
                    y -= direccióny
                    if x == comienzox and y == comienzoy:
                        break
                    baldosasAConvertir.append([x, y])

    tablero[comienzox][comienzoy] = ' ' # restablecer el espacio vacío
    if len(baldosasAConvertir) == 0: # Si no se convirtió ninguna baldosa, la jugada no es válida.
        return False
    return baldosasAConvertir


def estáEnTablero(x, y):
    # Devuelve True si las coordenadas se encuentran dentro del tablero
    return x >= 0 and x < size and y >= 0 and y < size


def obtenerTableroConJugadasVálidas(tablero, baldosa):
    # Devuelve un nuevo tablero, marcando con "." las jugadas válidas que el jugador puede realizar.
    replicaTablero = obtenerCopiaTablero(tablero)

    for x, y in obtenerJugadasVálidas(replicaTablero, baldosa):
        replicaTablero[x][y] = '.'
    return replicaTablero


def obtenerJugadasVálidas(tablero, baldosa):
    # Devuelve una lista de listas [x,y] de jugadas válidas para el jugador en el tablero dado.
    jugadasVálidas = []

    for x in range(size):
        for y in range(size):
            if esJugadaVálida(tablero, baldosa, x, y) != False:
                jugadasVálidas.append([x, y])
    return jugadasVálidas

clear = lambda: os.system('clear')

def obtenerPuntajeTablero(tablero):
    # Determina el puntaje contando las piezas. Devuelve un diccionario con claves 'X' y 'O'.
    puntajex = 0
    puntajeo = 0
    for x in range(size):
        for y in range(size):
            if tablero[x][y] == 'X':
                puntajex += 1
            if tablero[x][y] == 'O':
                puntajeo += 1
    return {'X':puntajex, 'O':puntajeo}


def ingresarBaldosaJugador():
    # Permite al jugador elegir que baldosa desea ser.
    # Devuelve una lista con la baldosa del jugador como primer elemento y el de la computadora como segundo.
    baldosa = ''
    while not (baldosa == 'X' or baldosa == 'O'):
        print('¿Deseas ser X ó O?')
        baldosa = input().upper()

    #  El primer elemento en la lista es la baldosa del juegador, el segundo es la de la computadora.
    if baldosa == 'X':
        return ['X', 'O']
    else:
        return ['O', 'X']


def quienComienza():
    # Elije al azar que jugador comienza.
    if random.randint(0, 1) == 0:
        return 'La computadora'
    else:
        return 'El jugador'


def jugarDeNuevo():
    # Esta función devuelve True si el jugador quiere jugar de nuevo, de lo contrario devuelve False.
    print('¿Quieres jugar de nuevo? (sí o no)')
    return input().lower().startswith('s')


def hacerJugada(tablero, baldosa, comienzox, comienzoy):
    # Coloca la baldosa sobre el tablero en comienzox, comienzoy, y convierte cualquier baldosa del oponente.
    # Devuelve False si la jugada es inválida, True si es válida.
    baldosasAConvertir = esJugadaVálida(tablero, baldosa, comienzox, comienzoy)

    if baldosasAConvertir == False:
        return False

    tablero[comienzox][comienzoy] = baldosa
    for x, y in baldosasAConvertir:
        tablero[x][y] = baldosa
    return True


def obtenerCopiaTablero(tablero):
    # Duplica la lista del tablero y devuelve el duplicado.
    replicaTablero = obtenerNuevoTablero()

    for x in range(size):
        for y in range(size):
            replicaTablero[x][y] = tablero[x][y]

    return replicaTablero


def esEsquina(x, y):
    # Devuelve True si la posicion es una de las esquinas.
    return (x == 0 and y == 0) or (x == 7 and y == 0) or (x == 0 and y == 7) or (x == 7 and y == 7)


def obtenerJugadaJugador(tablero, baldosaJugador):
    # Permite al jugador tipear su jugada.
    # Devuelve la jugada como [x, y] (o devuelve las cadenas 'pistas' o 'salir')
    
    CIFRAS1A8 = [str(x) for x in range(size)]
    while True:
        print('Ingresa tu jugada, salir para terminar el juego, o pistas para activar/desactivar las pistas.')
        jugada = input().lower()
        if jugada == 'salir':
            return 'salir'
        if jugada == 'pistas':
            return 'pistas'

        if len(jugada) == 2 and jugada[0] in CIFRAS1A8 and jugada[1] in CIFRAS1A8:
            x = int(jugada[0]) - 1
            y = int(jugada[1]) - 1
            if esJugadaVálida(tablero, baldosaJugador, x, y) == False:
                continue
            else:
                break
        else:
            print('Esta no es una jugada válida. Ingresa la coordenada x (1-8), luego la coordenada y (1-8).')
            print('Por ejemplo, 81 corresponde a la esquina superior derecha.')

    return [x, y]


def obtenerJugadaComputadora(tablero, baldosaComputadora):
    # Dado un tablero y la baldosa de la computadora, determinar dónde
    # jugar y devolver esa jugada como una lista [x, y].
    jugadasPosibles = obtenerJugadasVálidas(tablero, baldosaComputadora)

    # ordena al azar el orden de las jugadas posibles
    random.shuffle(jugadasPosibles)

    # siempre jugar en una esquina si está disponible.
    for x, y in jugadasPosibles:
        if esEsquina(x, y):
            return [x, y]

    # Recorrer la lista de jugadas posibles y recordar la que da el mejor puntaje
    mejorPuntaje = -1
    for x, y in jugadasPosibles:
        replicaTablero = obtenerCopiaTablero(tablero)
        hacerJugada(replicaTablero, baldosaComputadora, x, y)
        puntaje = obtenerPuntajeTablero(replicaTablero)[baldosaComputadora]
        if puntaje > mejorPuntaje:
            mejorJugada = [x, y]
            mejorPuntaje = puntaje
    return mejorJugada


def mostrarPuntajes(baldosaJugador, baldosaComputadora):
    # Imprime el puntaje actual.
    puntajes = obtenerPuntajeTablero(tableroPrincipal)
    print('Tienes %s puntos. La computadora tiene %s puntos.' % (puntajes[baldosaJugador], puntajes[baldosaComputadora]))

#Definir el tamaño del tablero 

clear = lambda: os.system('clear')

size = int(input('Ingresa el tamaño del tablero: ')) 
clear()

while (size < 8 or size%2 != 0):
    size = int(input('Ingresa el tamaño del tablero: '))
    clear()

print('¡Bienvenido a Reversi!')

victoriasx = 0
victoriaso = 0
empates = 0
numPartidas = int(input('Ingresa el número de partidas a jugar: '))

for partida in range(numPartidas):
    print('Partida #%s:' % (partida), end=' ')
    # Reiniciar el tablero y la partida.
    tableroPrincipal = obtenerNuevoTablero()
    reiniciarTablero(tableroPrincipal)
    if quienComienza() == 'jugador':
        turno = 'X'
    else:
        turno = 'O'
    
    while True:
        dibujarTablero(tableroPrincipal)
        if turno == 'X':
            # Turno de X.
            otraBaldosa = 'O'
            x, y = obtenerJugadaComputadora(tableroPrincipal, 'X')
            hacerJugada(tableroPrincipal, 'X', x, y)
        else:
            # Turno de O.
            otraBaldosa = 'X'
            x, y = obtenerJugadaComputadora(tableroPrincipal, 'O')
            hacerJugada(tableroPrincipal, 'O', x, y)

        if obtenerJugadasVálidas(tableroPrincipal, otraBaldosa) == []:
            break
        else:
            turno = otraBaldosa

        # Mostrar el puntaje final. 
        puntajes = obtenerPuntajeTablero(tableroPrincipal)
        print('X ha obtenido %s puntos. O ha obtenido %s puntos.' %(puntajes['X'], puntajes['O']))
        
    if puntajes['X'] > puntajes['O']:
        victoriasx += 1
    elif puntajes['X'] < puntajes['O']:
        victoriaso += 1
    else:
        empates += 1
        
numPartidas = float(numPartidas)
porcentajex = round(((victoriasx / numPartidas) * 100), 2)
porcentajeo = round(((victoriaso / numPartidas) * 100), 2)
porcentajeempate = round(((empates / numPartidas) * 100), 2)
print('X ha ganado %s partidas (%s%%), O ha ganado %s partidas (%s%%),empates en %s partidas (%s%%) sobre un total de %s partidas.' % (victoriasx,porcentajex, victoriaso, porcentajeo, empates, porcentajeempate, numPartidas))
