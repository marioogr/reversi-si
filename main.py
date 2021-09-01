import sys, pygame, math

pygame.init()

#Jugador 1 = 1, Agente = 2

class JuegoOtello:
    def __init__(self, tablero, turno):
        self.tablero = tablero
        self.completado = False
        self.turno = turno

    def setTablero (self, tablero):
        self.tablero = tablero


    def busqueda(self, fila, columna, juagdor):
        
        if juagdor == 1:
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
        if (i >= 0 and j >= 0 and i < 8 and j < 8 and self.tablero[i][j] == otro):
            i += x
            j += y
            while (i >= 0 and j >= 0 and i < 8 and j < 8 and self.tablero[i][j] == otro):
                i += x
                j += y
            if (i >= 0 and j >= 0 and i < 8 and j < 8 and self.tablero[i][j] == 0):
                return (i, j)


    def generarJugadasPosibles(self, jugador):
        """
        Retorna un arreglo de coordenadas de las jugadas posibles 

        """
       
        jugadasPosibles=[]
        for i in range(6):
            for j in range(6):
                if self.tablero[i][j]==jugador:
                    jugadasPosibles=jugadasPosibles+self.busqueda(i,j,jugador)
        jugadasPosibles=list(set(jugadasPosibles))
        print(jugadasPosibles)
        return jugadasPosibles
        
    

    def CalcularUtilidad(self, jugador):
        count = 0
        for i in range(0,6):
            for j in range(0,6):
                if self.tablero[i][j] == jugador:
                    count = count + 1
        return count

    def evaluarTermino(self):
        if 0 in self.tablero:
            self.completado = True
        else: self.completado = False

    def minMax(self):
        raise NotImplementedError
        
class Tablero:
    def __init__(self):
        self.tablero = [
            [0,0,0,0,0,0],
            [0,0,0,0,0,0],
            [0,0,2,2,0,0],
            [0,0,2,1,0,0],
            [0,0,0,0,0,0],
            [0,0,0,0,0,0],
        ]

    def actualizarTablero(self, x, y, valor):
        self.tablero[x][y] = valor

    def renderizarTablero(self, screen):

        CuadradoAzul = pygame.image.load("sprites/CuadradoAzul.png")
        CuadradoAzul = pygame.transform.scale(CuadradoAzul, (100, 100))
        CuadradoRojo = pygame.image.load("sprites/CuadradoRojo.png")
        CuadradoRojo = pygame.transform.scale(CuadradoRojo, (100, 100))
        CuadradoGris = pygame.image.load("sprites/CuadradoGris.png")
        CuadradoGris = pygame.transform.scale(CuadradoGris, (100, 100))
        CuadradoBlanco = pygame.image.load("sprites/CuadradoBlanco.png")
        CuadradoBlanco = pygame.transform.scale(CuadradoBlanco, (100, 100))

        for i in range(0,6):
            for j in range(0,6):
                if self.tablero[i][j] == 0:
                    screen.blit(CuadradoGris, (i*100, j*100))
                if self.tablero[i][j] == 1:
                    screen.blit(CuadradoRojo, (i*100, j*100))
                if self.tablero[i][j] == 2:
                    screen.blit(CuadradoAzul, (i*100, j*100))
                if self.tablero[i][j] == 3:
                    screen.blit(CuadradoBlanco, (i*100, j*100))

    def marcarPorMouse(self, posMouse, jugadasPosibles):
        x = int(math.trunc(posMouse[0]/100))
        y = int(math.trunc(posMouse[1]/100))

        for i in range(0,6):
            for j in range(0,6):
                if i == x and j == y:
                    if self.tablero[i][j] == 0:
                        if (x, y) in jugadasPosibles:
                            self.actualizarTablero(x, y, 3)

    def restablecerBlanco(self, posMouse):
        x = int(math.trunc(posMouse[0]/100))
        y = int(math.trunc(posMouse[1]/100))

        for i in range(0,6):
            for j in range(0,6):
                if not (i == x and j == y):
                    if self.tablero[i][j] == 3:
                        self.tablero[i][j] = 0

    def DepImprimirtablero(self):
        for i in range(0,6):
            print(self.tablero[i])

def renderizarTablero(tablero: Tablero, screen):
    CuadradoAzul = pygame.image.load("sprites/CuadradoAzul.png")
    CuadradoAzul = pygame.transform.scale(CuadradoAzul, (100, 100))
    CuadradoRojo = pygame.image.load("sprites/CuadradoRojo.png")
    CuadradoRojo = pygame.transform.scale(CuadradoRojo, (100, 100))
    CuadradoGris = pygame.image.load("sprites/CuadradoGris.png")
    CuadradoGris = pygame.transform.scale(CuadradoGris, (100, 100))
    CuadradoBlanco = pygame.image.load("sprites/CuadradoBlanco.png")
    CuadradoBlanco = pygame.transform.scale(CuadradoBlanco, (100, 100))

    for i in range(0,6):
        for j in range(0,6):
            if tablero.tablero[i][j] == 0:
                screen.blit(CuadradoGris, (i*100, j*100))
            if tablero.tablero[i][j] == 1:
                screen.blit(CuadradoRojo, (i*100, j*100))
            if tablero.tablero[i][j] == 2:
                screen.blit(CuadradoAzul, (i*100, j*100))
            if tablero.tablero[i][j] == 3:
                screen.blit(CuadradoBlanco, (i*100, j*100))
            

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
    
    tablero = Tablero()
    clock = pygame.time.Clock()
    
    juego = JuegoOtello(tablero.tablero, 1)

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

        screen.fill(background)

        posMouse = pygame.mouse.get_pos()

        juego.setTablero(tablero.tablero)
        
        jugadasPosibles = juego.generarJugadasPosibles(1)
        
        tablero.marcarPorMouse(posMouse, jugadasPosibles)

        clock.tick(30)

        tablero.renderizarTablero(screen)
        tablero.DepImprimirtablero()
        pygame.display.flip()

main()