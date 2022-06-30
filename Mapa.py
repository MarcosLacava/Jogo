import pygame
import pygame.display

class Mapa():
    q = pygame.image.load("quadradopreto.png")
    tileLen = q.get_bounding_rect().width
    
    def __init__(self, mapa):
        self.quadrados = [(self.q, (0,0))]
        self.colisores = []

        self.q = self.q.convert()
        # Cria cada tile do mapa
        for i in range(len(mapa)):
            for j in range(len(mapa[i])):
                if mapa[i][j] == 1:
                    r = pygame.Rect([j*self.tileLen, i*self.tileLen], [self.tileLen, self.tileLen])
                    self.quadrados.append((self.q, (j*self.tileLen, i*self.tileLen)))
                    self.colisores.append(r)