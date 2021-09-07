import sys
import pygame
import math


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

    def cambiar_turno(self):
        """metodo que intercala el turno de los jugadores luego de realizar un movimiento"""
        if self.turno == 1:
            self.turno=2
        else:
            self.turno=1

    def busqueda(self, fila, columna):
        """metodo que permite buscar las posibles casillas donde el jugador puede colocar fichas"""
        if self.turno == 1:
            otro = 2
        else:
            otro = 1

        casillas = []

        if fila < 0 or fila > 7 or columna < 0 or columna > 7:
            return casillas

        # For each direction search for possible positions to put a piece.
        for (x, y) in [
            (-1, 0),
            (-1, 1),
            (0, 1),
            (1, 1),
            (1, 0),
            (1, -1),
            (0, -1),
            (-1, -1)
        ]:
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
            if i >= 0 and j >= 0 and i < 6 and j < 6 and self.tablero[i][j] == 0:
                return i, j

    def generarJugadasPosibles(self):
        """
        Retorna un arreglo de coordenadas de las jugadas posibles segun el turno del jugador

        """

        jugadasPosibles = []
        for i in range(6):
            for j in range(6):
                if self.tablero[i][j] == self.turno:
                    jugadasPosibles = jugadasPosibles + self.busqueda(i, j)
        jugadasPosibles = list(set(jugadasPosibles))
        print(jugadasPosibles)
        return jugadasPosibles






    def minMax(self):
        raise NotImplementedError

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

        if self.turno==1:
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
        jugadas = self.generarJugadasPosibles()
        x = int(math.trunc(posMouse[0] / 100))
        y = int(math.trunc(posMouse[1] / 100))

        for i in range(0, 6):
            for j in range(0, 6):
                if i == x and j == y:
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
        """Metodo que registra si el jugador hace click en una de las celdas posibles reemplazandola con el color del jugador"""
        jugadas = self.generarJugadasPosibles()
        x = int(math.trunc(posMouse[0] / 100))
        y = int(math.trunc(posMouse[1] / 100))
        if pygame.mouse.get_pressed()[0] and self.turno == 1 and y !=6:

            print(x, y)
            if self.tablero[x][y] == 3:
                self.tablero[x][y] = 1
                for i in range(1, 7):
                    self.voltear(i, (x, y), 1)
                self.cambiar_turno()


        if pygame.mouse.get_pressed()[0] and self.turno == 2 and y !=6:

            if self.tablero[x][y] == 3:
                self.tablero[x][y] = 2
                for i in range(1, 9):
                    self.voltear(i, (x, y), 2)
                self.cambiar_turno()

        self.endgame()

    def voltear(self, direccion, jugada, jugador):
        """Metodo que obtiene las celdas que seran afectadas por la jugada cambiando su color  """

        if direccion == 1:
            # north
            row_inc = -1
            col_inc = 0
        elif direccion == 2:
            # northeast
            row_inc = -1
            col_inc = 1
        elif direccion == 3:
            # east
            row_inc = 0
            col_inc = 1
        elif direccion == 4:
            # southeast
            row_inc = 1
            col_inc = 1
        elif direccion == 5:
            # south
            row_inc = 1
            col_inc = 0
        elif direccion == 6:
            # southwest
            row_inc = 1
            col_inc = -1
        elif direccion == 7:
            # west
            row_inc = 0
            col_inc = -1
        elif direccion == 8:
            # northwest
            row_inc = -1
            col_inc = -1

        places = []  # pieces to flip

        i = jugada[0] + row_inc
        j = jugada[1] + col_inc

        if jugador == 1:
            otro = 2
        else:
            otro = 1

        if i in range(6) and j in range(6) and self.tablero[i][j] == otro:
            # assures there is at least one piece to flip
            places = places + [(i, j)]
            i = i + row_inc
            j = j + col_inc
            while i in range(6) and j in range(6) and self.tablero[i][j] == otro:
                # search for more pieces to flip
                places = places + [(i, j)]
                i = i + row_inc
                j = j + col_inc
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
                if self.tablero[x][y]==1:
                    j1=j1+1
                elif self.tablero[x][y]==2:
                    j2=j2+1
                elif self.tablero[x][y]==0 or self.tablero[x][y] == 3:
                    vacio=vacio+1


        return j1,j2,vacio

    def endgame(self):
        """Metodo que verifica si el juego termino bajo diferentes condiciones
            1.-j1 sin fichas en tablero
            2.-j2 si fechas en tablero
            3.- tablero completo(sin casillas vacias)
            4.-j1 sin jugadas posibles
            5- j2 sin jugadas posibles"""

        j1,j2,vacio=self.contar_fichas()

        if j1==0 or j2==0 or vacio == 0 :
            print('primer if',j1,j2,vacio)
            self.completado=True
            return True

        if self.generarJugadasPosibles() == []:
            print('segundo if')
            self.completado=True
            return True

        return False

    def render_ganador(self,screen):
        """Metodo que se activa al terminar el juego y presenta al ganador de este o el empate"""

        if self.completado==True:
            CuadradoAmarillo = pygame.image.load("sprites/CuadradoAmarillo.png")
            CuadradoAmarillo = pygame.transform.scale(CuadradoAmarillo, (100, 100))
            for x in range(6):
                for y in range(6):
                    screen.blit(CuadradoAmarillo, (x * 100, y * 100))
            j1, j2, empty = self.contar_fichas()
            fuente = pygame.font.SysFont("segoe print", 40)
            texto = fuente.render(f"Ganador:", True, [255, 0, 50])

            if j1 > j2:
                print("Gano J1")
                texto = fuente.render(f"Ganador: J1", True, [0, 0, 0])
            elif j2 > j1:
                print("Gano J2")
                texto = fuente.render(f"Ganador: J2", True, [0, 0, 0])
            elif j1 == j2:
                print("Empate")
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
    size = width, height = 600, 700
    background = 246, 249, 249
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    juego = JuegoReversi(1)

    while 1:
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
        juego.DepImprimirtablero()
        pygame.display.flip()


main()
