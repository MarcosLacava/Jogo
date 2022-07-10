import pygame
import pygame.display

from Spritesheet import Spritesheet

class Mapa():



    def __init__(self, mapa):
        self.quadrados = []
        self.spritesheet = Spritesheet("main-room")
        self.colisores = []
        self.matriz_mapa = mapa
        self.largura = 13

        # Adiciona tiles de transição baseado na matriz do mapa
        for i in range(0, self.largura):
            for j in range(0, self.largura):
                if mapa[i][j] == 0:
                    if mapa[i-1][j] == 1:
                        if mapa[i][j-1] == 1:
                            mapa[i][j] = 3    
                        elif mapa[i][j+1] == 1:
                            mapa[i][j] = 5
                        else:
                            mapa[i][j] = 4 

                    elif mapa[i][j-1] == 1:
                        if mapa[i+1][j] == 1:
                            mapa[i][j] = 9
                        else:
                            mapa[i][j] = 10

                    elif mapa[i][j+1] == 1:
                        if mapa[i+1][j] == 1:
                            mapa[i][j] = 7
                        else:
                            mapa[i][j] = 6
                    
                    elif mapa[i+1][j] == 1:
                        mapa[i][j] = 8

        # Troca paredes das extremidades por tiles de fundo
        for i in range (self.largura):
            mapa[0]            [i] = 2
            mapa[i]            [0] = 2
            mapa[self.largura-1][i] = 2
            mapa[i][self.largura-1] = 2
                    
        # Cria cada tile do mapa
        for i in range(len(mapa)):
            for j in range(len(mapa[i])):
                    r = pygame.Rect([j*self.spritesheet.tileLen, i*self.spritesheet.tileLen], [self.spritesheet.tileLen, self.spritesheet.tileLen])
                    self.quadrados.append((self.spritesheet.cortar_sprite(("sprite_main-room" + '{:0>2}'.format(str(mapa[i][j])) + ".png")), (j*self.spritesheet.tileLen, i*self.spritesheet.tileLen)))
                    self.colisores.append(r)