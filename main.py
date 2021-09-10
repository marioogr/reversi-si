import sys
import pygame
import math
import random
import time


pygame.init()


# Jugador 1 = 1, Agente = 2

class JuegoReversi:
    """Clase Juego Reversi que controlara y registrara todos los eventos del juego"""
    def __init__(self, turno):
        """Constructor de la clase con los atributos principales
         tablero es una matriz que tendra la representacion y los estados del juego durante su ejecución
         0=celda vacia
         1=fichas del jugador 1 (rojo)
         2=fichas del jugador 2 (azul)
         3=posible lugar donde se colocaran fichas segun jugador

        completo es un atributo boleano que representa si el juego termina al estar el tablero lleno

        turno es un atributo que representa el turno de uno de los 2 jugadores
        """
        self.tablero = [
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 1, 2, 0, 0],
            [0, 0, 2, 1, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
        ]
        self.completado = False #  atributo boleano que representa si el juego termina al estar el tablero lleno
        self.turno = turno # atributo que representa el turno de uno de los 2 jugadores
        self.profundidad=0
        self.game=False

    def set_game(self,game):
        self.game=game

    def set_dificultad(self,dificultad):

        if dificultad==1:
            self.profundidad=2
        elif dificultad==2:
            self.profundidad=6

    def cambiar_turno(self):
        """metodo que intercala el turno de los jugadores luego de realizar un movimiento"""
        if self.turno == 1:
            self.turno=2
        else:
            self.turno=1

    def busqueda(self, fila, columna,turno):
        """metodo que permite buscar las posibles casillas donde el jugador puede colocar fichas"""
        if turno == 1:
            otro = 2
        else:
            otro = 1

        casillas = []

        if fila < 0 or fila > 7 or columna < 0 or columna > 7:
            return casillas

        # For each direction search for possible positions to put a piece.
        for (x, y) in [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]:
            pos = self.verifica_direccion(fila, columna, x, y, otro)
            if pos:
                casillas.append(pos)
        return casillas

    def verifica_direccion(self, fila, columna, x, y, otro):
        """metodo que verifica si en la direccion existen fichas del jugador contrario y retorna la celda vacia de existir"""
        i = fila + x
        j = columna + y
        if 0 <= i < 6 and 0 <= j < 6 and self.tablero[i][j] == otro:
            i += x
            j += y
            while 0 <= i < 6 and 0 <= j < 6 and self.tablero[i][j] == otro:
                i += x
                j += y
            if i >= 0 and j >= 0 and i < 6 and j < 6 and (self.tablero[i][j] == 0 or self.tablero[i][j] == 3):
                return i, j

    def generarJugadasPosibles(self,turno):
        """
        Retorna un arreglo de coordenadas de las jugadas posibles segun el turno del jugador

        """
        jugadasPosibles = []
        for i in range(6):
            for j in range(6):
                if self.tablero[i][j] == turno:
                    jugadasPosibles = jugadasPosibles + self.busqueda(i, j,turno)
        jugadasPosibles = list(set(jugadasPosibles))

        return jugadasPosibles

    def jugar(self,jugada):
        self.tablero[jugada[0]][jugada[1]] = 2

    def deshacer_jugada(self,jugada):
        self.tablero[jugada[0]][jugada[1]] = 0

    def minimax(self, etapa, secuencia, secuencias, profundidad):

        if self.endgame() or profundidad >= self.profundidad:

            secuencias.append(secuencia.copy())
            j1, j2, vacio = self.contar_fichas()
            if j1 > j2:
                return [-1]
            elif j2 > j1:
                return [1]
            else:
                return [0]

        if etapa == 1:
            valor = [-1000, None]
            jugadas_posibles = self.generarJugadasPosibles(2)
        else:
            valor = [1000, None]
            jugadas_posibles = self.generarJugadasPosibles(1)



        for jugada in jugadas_posibles:
            self.jugar(jugada)
            secuencia.append(jugada)
            opcion = self.minimax(etapa * -1, secuencia, secuencias,profundidad+1)
            # maximizar

            if etapa == 1:
                if valor[0] < opcion[0]:
                    valor = [opcion[0], jugada]
            else:
                # minimizar
                if valor[0] > opcion[0]:
                    valor = [opcion[0], jugada]
            self.deshacer_jugada(jugada)
            secuencia.pop()
        return valor

    def renderizarTablero(self, screen):

        """Metodo encargado de renderizar en pantalla todos los asets necesarios para la ejecucion de este"""

        CuadradoAzul = pygame.image.load("sprites/CuadradoAzul.png")
        CuadradoAzul = pygame.transform.scale(CuadradoAzul, (100, 100))
        CuadradoRojo = pygame.image.load("sprites/CuadradoRojo.png")
        CuadradoRojo = pygame.transform.scale(CuadradoRojo, (100, 100))
        CuadradoGris = pygame.image.load("sprites/CuadradoGris.png")
        CuadradoGris = pygame.transform.scale(CuadradoGris, (100, 100))
        CuadradoBlanco = pygame.image.load("sprites/CuadradoBlanco.png")
        CuadradoBlanco = pygame.transform.scale(CuadradoBlanco, (100, 100))
        fuente = pygame.font.SysFont("segoe print", 40)
        j1_texto = fuente.render(f"J1", True, [255, 0, 50])
        j1_score= fuente.render(f"{self.contar_fichas()[0]}", True, [255, 0, 50])
        screen.blit(j1_texto, (100, 585))
        screen.blit(j1_score, (100, 630))
        j2_texto = fuente.render(f"J2", True, [0, 0, 255])
        j2_score = fuente.render(f"{self.contar_fichas()[1]}", True, [0, 0, 255])
        screen.blit(j2_texto, (450, 585))
        screen.blit(j2_score, (450, 630))

        if self.turno == 1:
            screen.blit(CuadradoRojo, (250, 600))
        else:
            screen.blit(CuadradoAzul, (250, 600))

        for i in range(0, 6):
            for j in range(0, 6):
                if self.tablero[i][j] == 0:
                    screen.blit(CuadradoGris, (i * 100, j * 100))
                if self.tablero[i][j] == 1:
                    screen.blit(CuadradoRojo, (i * 100, j * 100))
                if self.tablero[i][j] == 2:
                    screen.blit(CuadradoAzul, (i * 100, j * 100))
                if self.tablero[i][j] == 3:
                    screen.blit(CuadradoBlanco, (i * 100, j * 100))

    def marcarPorMouse(self, posMouse):
        """Metodo que obriene las coordenadas del mause dentro de la pantalla y si coincide con la celda del tablero con valor 0 (celda vacia)
            y esta dento de las posibles jugadas lo reemplaza con el valor 3 mostrandoce un cuadrado blanco
        """
        jugadas = self.generarJugadasPosibles(self.turno)
        x = int(math.trunc(posMouse[0] / 100))
        y = int(math.trunc(posMouse[1] / 100))

        for i in range(0, 6):
            for j in range(0, 6):
                if self.tablero[i][j] == 0:
                    if (x, y) in jugadas:
                        self.tablero[x][y] = 3

    def restablecerBlanco(self, posMouse):
        """Metodo que permite restablecer de blanco a  plomo la celda si el jugador retira el mouse de esta"""
        x = int(math.trunc(posMouse[0] / 100))
        y = int(math.trunc(posMouse[1] / 100))

        for i in range(0, 6):
            for j in range(0, 6):
                if not (i == x and j == y):
                    if self.tablero[i][j] == 3:
                        self.tablero[i][j] = 0

    def DepImprimirtablero(self):
        """Metodo que imprime en terminal el tablero"""
        for i in range(0, 6):
            print(self.tablero[i])

    def clickear_tablero(self, posMouse):
        """Metodo que registra si el jugador hace click en una de las celdas posibles
         reemplazandola con el color del jugador para luego voltear las fichas afectadas"""

        jugadas = self.generarJugadasPosibles(self.turno)
        x = int(math.trunc(posMouse[0] / 100))
        y = int(math.trunc(posMouse[1] / 100))
        if pygame.mouse.get_pressed()[0] and self.turno == 1 and y !=6 and self.game==True:

            if self.tablero[x][y] == 3:
                self.tablero[x][y] = 1
                for i in range(1, 9):
                    self.voltear(i, (x, y), 1)
                self.cambiar_turno()


        if self.turno == 2 and y != 6:
            a=[]
            b=[]
            inicio=time.time()
            m=self.minimax(1, a, b, 0)
            fin=time.time()
            print(f"nodos: {len(b)},tiempo ejecucion: {fin-inicio} ")

            jugada=m[1]
            if jugada is None:
                r = random.randint(0,len(jugadas))
                jugada = jugadas[r]

            self.tablero[jugada[0]][jugada[1]] = 2
            for i in range(1, 9):
                self.voltear(i, (jugada[0], jugada[1]), 2)
            self.cambiar_turno()
        self.set_game(True)
        self.endgame()

    def voltear(self, direccion, jugada, jugador):
        """Metodo que obtiene las celdas que seran afectadas por la jugada cambiando su color  """

        if direccion == 1:
            # arriba
            fila_inc = -1
            columna_inc = 0
        elif direccion == 2:
            # arriba,izquierda
            fila_inc = -1
            columna_inc = 1
        elif direccion == 3:
            # izquierda
            fila_inc = 0
            columna_inc = 1
        elif direccion == 4:
            # abajo,izquierda
            fila_inc = 1
            columna_inc = 1
        elif direccion == 5:
            # abajo
            fila_inc = 1
            columna_inc = 0
        elif direccion == 6:
            # abajo,derecha
            fila_inc = 1
            columna_inc = -1
        elif direccion == 7:
            # derecha
            fila_inc = 0
            columna_inc = -1
        elif direccion == 8:
            # derecha,arriba
            fila_inc = -1
            columna_inc = -1

        places = []  # pieces to flip

        i = jugada[0] + fila_inc
        j = jugada[1] + columna_inc

        if jugador == 1:
            otro = 2
        else:
            otro = 1

        if i in range(6) and j in range(6) and self.tablero[i][j] == otro:
            # assures there is at least one piece to flip
            places = places + [(i, j)]
            i = i + fila_inc
            j = j + columna_inc
            while i in range(6) and j in range(6) and self.tablero[i][j] == otro:
                # search for more pieces to flip
                places = places + [(i, j)]
                i = i + fila_inc
                j = j + columna_inc
            if i in range(6) and j in range(6) and self.tablero[i][j] == jugador:
                # found a piece of the right color to flip the pieces between
                for pos in places:
                    # flips
                    self.tablero[pos[0]][pos[1]] = jugador

    def contar_fichas(self):
        """Metodo que obtiene la utilidad de la jugada (fichas de los 2 jugadores y fichas vacias """
        j1=0
        j2=0
        vacio=0

        for x in range(6):
            for y in range(6):
                if self.tablero[x][y] == 1:
                    j1=j1+1
                elif self.tablero[x][y] == 2:
                    j2=j2+1
                elif self.tablero[x][y] == 0 or self.tablero[x][y] == 3:
                    vacio = vacio+1

        return j1, j2, vacio

    def endgame(self):
        """Metodo que verifica si el juego termino bajo diferentes condiciones
            1.-j1 sin fichas en tablero
            2.-j2 si fechas en tablero
            3.- tablero completo(sin casillas vacias)
            4.-j1 sin jugadas posibles
            5- j2 sin jugadas posibles"""

        j1, j2, vacio = self.contar_fichas()

        if j1 == 0 or j2 == 0 or vacio == 0:

            self.completado = True
            return True

        if self.generarJugadasPosibles(1) == [] and self.generarJugadasPosibles(2) == []:

            self.completado = True
            return True

        return False

    def render_ganador(self, screen):
        """Metodo que se activa al terminar el juego y presenta al ganador de este o el empate"""

        if self.completado:
            CuadradoAmarillo = pygame.image.load("sprites/CuadradoAmarillo.png")
            CuadradoAmarillo = pygame.transform.scale(CuadradoAmarillo, (100, 100))
            for x in range(6):
                for y in range(6):
                    screen.blit(CuadradoAmarillo, (x * 100, y * 100))
            j1, j2, empty = self.contar_fichas()
            fuente = pygame.font.SysFont("segoe print", 40)
            texto = fuente.render(f"Ganador:", True, [255, 0, 50])

            if j1 > j2:

                texto = fuente.render(f"Ganador: J1", True, [0, 0, 0])
            elif j2 > j1:

                texto = fuente.render(f"Ganador: J2", True, [0, 0, 0])
            elif j1 == j2:

                texto = fuente.render(f"Empate", True, [0, 0, 0])

            screen.blit(texto, (200, 320))


"""
0 = Gris no seleccionado
1 = Rojo / Jugador 1
2 = Azul / Jugador 2
3 = Seleccion de mouse
"""


def main():
    """Funcion main que ejecuta el juego"""

    #print("Elija nivel de dificultad")
    #dificultad = int(input())

    size = width, height = 600, 700
    background = 246, 249, 249
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    juego = JuegoReversi(1)

    menu=True

    CuadradoAmarillo = pygame.image.load("sprites/CuadradoAmarillo.png")
    btnfacil=pygame.image.load("sprites/btnfacil.png")
    btndificil=pygame.image.load("sprites/btndificil.png")
    CuadradoAmarillo = pygame.transform.scale(CuadradoAmarillo, (100, 100))
    btnfacil = pygame.transform.scale(btnfacil, (100, 100))
    btndificil= pygame.transform.scale(btndificil, (100, 100))
    fuente = pygame.font.SysFont("segoe print", 40)
    fuente2 = pygame.font.SysFont("segoe print", 80)
    texto = fuente.render(f"Elija la dificultad:", True, [0, 0, 0])
    titulo = fuente2.render("Reversi Games",True,[0,0,0])
    desarrolladores =fuente.render("Devs:Mario,Pablo,Jaime,Ariel",True,[0,0,0])

    while menu==True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        posMouse = pygame.mouse.get_pos()
        m = int(math.trunc(posMouse[0] / 100))
        n = int(math.trunc(posMouse[1] / 100))

        for x in range(6):
            for y in range(6):
                screen.blit(CuadradoAmarillo, (x * 100, y * 100))

        screen.blit(texto, (120, 200))
        screen.blit(btnfacil,(100,300))
        screen.blit(btndificil,(400,300))
        screen.blit(titulo,(5,50))
        screen.blit(desarrolladores,(0,500))

        if pygame.mouse.get_pressed()[0] and m == 1 and n == 3:
            print('facil')
            juego.set_dificultad(1)
            menu=False
        elif pygame.mouse.get_pressed()[0] and m == 4 and n == 3:
            print('dificil')

            juego.set_dificultad(2)
            menu=False

        clock.tick(30)
        pygame.display.flip()

    while not menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        screen.fill(background)

        posMouse = pygame.mouse.get_pos()

        juego.marcarPorMouse(posMouse)
        juego.clickear_tablero(posMouse)
        clock.tick(30)

        juego.renderizarTablero(screen)

        juego.render_ganador(screen)
        juego.restablecerBlanco(posMouse)
        # juego.DepImprimirtablero()

        pygame.display.flip()


main()
