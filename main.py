import sys
import pygame
import math
import pandas as pd

pygame.init()


# Jugador 1 = 1, Agente = 2

class JuegoOtello:
    def __init__(self, turno):
        self.tablero = [
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 1, 2, 0, 0],
            [0, 0, 2, 1, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
        ]
        self.completado = False
        self.turno = turno

    def cambiar_turno(self):
        if self.turno == 1:
            self.turno=2
        else:
            self.turno=1

    def busqueda(self, fila, columna):

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
        Retorna un arreglo de coordenadas de las jugadas posibles 

        """

        jugadasPosibles = []
        for i in range(6):
            for j in range(6):
                if self.tablero[i][j] == self.turno:
                    jugadasPosibles = jugadasPosibles + self.busqueda(i, j)
        jugadasPosibles = list(set(jugadasPosibles))
        print(jugadasPosibles)
        return jugadasPosibles

    def CalcularUtilidad(self):
        count = 0
        for i in range(0, 6):
            for j in range(0, 6):
                if self.tablero[i][j] == self.turno:
                    count = count + 1
        return count

    def evaluarTermino(self):
        if 0 in self.tablero:
            self.completado = True
        else:
            self.completado = False

    def minMax(self):
        raise NotImplementedError

    def renderizarTablero(self, screen):

        CuadradoAzul = pygame.image.load("sprites/CuadradoAzul.png")
        CuadradoAzul = pygame.transform.scale(CuadradoAzul, (100, 100))
        CuadradoRojo = pygame.image.load("sprites/CuadradoRojo.png")
        CuadradoRojo = pygame.transform.scale(CuadradoRojo, (100, 100))
        CuadradoGris = pygame.image.load("sprites/CuadradoGris.png")
        CuadradoGris = pygame.transform.scale(CuadradoGris, (100, 100))
        CuadradoBlanco = pygame.image.load("sprites/CuadradoBlanco.png")
        CuadradoBlanco = pygame.transform.scale(CuadradoBlanco, (100, 100))

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
        x = int(math.trunc(posMouse[0] / 100))
        y = int(math.trunc(posMouse[1] / 100))

        for i in range(0, 6):
            for j in range(0, 6):
                if not (i == x and j == y):
                    if self.tablero[i][j] == 3:
                        self.tablero[i][j] = 0

    def DepImprimirtablero(self):
        for i in range(0, 6):
            print(self.tablero[i])

    def clickear_tablero(self, posMouse):
        jugadas = self.generarJugadasPosibles()
        if pygame.mouse.get_pressed()[0] and self.turno == 1:
            x = int(math.trunc(posMouse[0] / 100))
            y = int(math.trunc(posMouse[1] / 100))
            print(x, y)
            if self.tablero[x][y] == 3:
                self.tablero[x][y] = 1
                for i in range(1, 7):
                    self.voltear(i, (x,y), 1)
                self.cambiar_turno()

        if pygame.mouse.get_pressed()[0] and self.turno == 2:
            x = int(math.trunc(posMouse[0] / 100))
            y = int(math.trunc(posMouse[1] / 100))
            if self.tablero[x][y] == 3:
                self.tablero[x][y] = 2
                for i in range(1, 9):
                    self.voltear(i,(x,y) , 2)
                self.cambiar_turno()

    def voltear(self, direccion, jugada,jugador):
        """ Flips (capturates) the pieces of the given color in the given direction
        (1=North,2=Northeast...) from position. """

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
        print(jugada[0],jugada[1])
        i = jugada[0] + row_inc
        j = jugada[1] + col_inc

        if jugador == 1:
            otro = 2
        else:
            otro = 1

        if i in range(8) and j in range(8) and self.tablero[i][j] == otro:
            # assures there is at least one piece to flip
            places = places + [(i, j)]
            i = i + row_inc
            j = j + col_inc
            while i in range(8) and j in range(8) and self.tablero[i][j] == otro:
                # search for more pieces to flip
                places = places + [(i, j)]
                i = i + row_inc
                j = j + col_inc
            if i in range(8) and j in range(8) and self.tablero[i][j] == jugador:
                # found a piece of the right color to flip the pieces between
                for pos in places:
                    # flips
                    self.tablero[pos[0]][pos[1]] = jugador


"""
0 = Gris no seleccionado
1 = Rojo / Jugador 1
2 = Azul / Jugador 2
3 = Seleccion de mouse
"""


def main():
    size = width, height = 600, 700
    background = 246, 249, 249
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    juego = JuegoOtello(2)

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

        screen.fill(background)

        posMouse = pygame.mouse.get_pos()

        juego.marcarPorMouse(posMouse)
        juego.clickear_tablero(posMouse)
        clock.tick(30)

        juego.renderizarTablero(screen)
        juego.restablecerBlanco(posMouse)
        juego.DepImprimirtablero()
        pygame.display.flip()


main()
