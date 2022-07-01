import pygame
import pygame.display

class Mapa():
    parede = pygame.image.load("tile_brick_wall0.png")
    chao = pygame.image.load("tile_main_floor0.png")
    rodape = pygame.image.load("tile_main_floor_footer0.png")
    detalhe = pygame.image.load("tile_brick_wall_detail0.png")
    tileLen = parede.get_bounding_rect().width
    
    def __init__(self, mapa):
        self.quadrados = [(self.parede, (0,0))]
        self.colisores = []

        # Cria cada tile do mapa
        for i in range(len(mapa)):
            for j in range(len(mapa[i])):
                if mapa[i][j] == 0:
                    r = pygame.Rect([j*self.tileLen, i*self.tileLen], [self.tileLen, self.tileLen])
                    self.quadrados.append((self.chao, (j*self.tileLen, i*self.tileLen)))
                    self.colisores.append(r)
                elif mapa[i][j] == 1:
                    r = pygame.Rect([j*self.tileLen, i*self.tileLen], [self.tileLen, self.tileLen])
                    self.quadrados.append((self.parede, (j*self.tileLen, i*self.tileLen)))
                    self.colisores.append(r)
                elif mapa[i][j] == 2:
                    r = pygame.Rect([j*self.tileLen, i*self.tileLen], [self.tileLen, self.tileLen])
                    self.quadrados.append((self.rodape, (j*self.tileLen, i*self.tileLen)))
                    self.colisores.append(r)
                elif mapa[i][j] == 3:
                    r = pygame.Rect([j*self.tileLen, i*self.tileLen], [self.tileLen, self.tileLen])
                    self.quadrados.append((self.detalhe, (j*self.tileLen, i*self.tileLen)))
                    self.colisores.append(r)