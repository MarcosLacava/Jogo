import pygame
import pygame.display

from Spritesheet import Spritesheet

class Mapa():



    def __init__(self, mapa):
        self.quadrados = []
        self.spritesheet = Spritesheet("main-room")
        self.colisores = []
        self.matriz_mapa = mapa

        # Adiciona tiles de transição baseado no mapa
        for i in range(1, len(mapa)-1):
            for j in range(0, len(mapa[0])):
                if mapa[i][j] == 0 and i != 0 and i != len(mapa):
                    if mapa[i-1][j] == 1:
                        mapa[i][j] = 4 

        # Cria cada tile do mapa
        for i in range(len(mapa)):
            for j in range(len(mapa[i])):
                    r = pygame.Rect([j*self.spritesheet.tileLen, i*self.spritesheet.tileLen], [self.spritesheet.tileLen, self.spritesheet.tileLen])
                    self.quadrados.append((self.spritesheet.cortar_sprite(("sprite_main-room" + '{:0>2}'.format(str(mapa[i][j])) + ".png")), (j*self.spritesheet.tileLen, i*self.spritesheet.tileLen)))
                    self.colisores.append(r)