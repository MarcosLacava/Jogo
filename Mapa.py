import pygame
import pygame.display

class Mapa():
    q = pygame.image.load("quadradopreto.png")
    quadrados = [(q, (0,0))]
    colisores = []

    def __init__(self):
        self.q = self.q.convert()
        mapa = [
        [1, 1, 1, 1, 0, 0, 1, 1, 1, 1], 
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
        [1, 0, 1, 0, 0, 0, 0, 0, 0, 1], 
        [1, 0, 0, 0, 0, 0, 1, 0, 0, 1], 
        [0, 0, 0, 0, 0, 1, 0, 0, 0, 0], 
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0], 
        [1, 0, 0, 1, 0, 0, 1, 1, 0, 1], 
        [1, 0, 0, 0, 0, 0, 1, 1, 0, 1], 
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
        [1, 1, 1, 1, 0, 0, 1, 1, 1, 1], 
       ]
        #Cria cada quadrado do mapa
        for i in range(len(mapa)):
            for j in range(len(mapa[i])):
                if mapa[i][j] == 1:
                    r = pygame.Rect([j*100, i*100], [100, 100])
                    self.quadrados.append((self.q, (j*100, i*100)))
                    self.colisores.append(r)