from encodings import CodecRegistryError
import pygame
import pygame.display
import copy

from Spritesheet import Spritesheet

class Mapa():

    def __init__(self, matriz, sprites, interagiveis):
        self.quadrados = []
        self.sprites = sprites
        self.spritesheet = Spritesheet(sprites)
        self.matriz_mapa = matriz
        self.largura = 13

        for k in interagiveis.keys(): # Adiciona cada interagível da lista no mapa
            try: # Testa para ver se as coordenadas estão no nome
                cordX, cordY = k.split()
                cordX, cordY = int(cordX), int(cordY)

            except ValueError: # Caso contrário, assume que o valor está no dicionário
                tile = interagiveis[k]["tile_num"]
                cordX, cordY = interagiveis[k]["pos"]

            tile = interagiveis[k]["tile_num"]
            
            if tile == -1:
                self.matriz_mapa[cordX][cordY] = 0
            else:
                self.matriz_mapa[cordX][cordY] = tile

        # Cria cada tile do mapa
        for i in range(len(self.matriz_mapa)):
            for j in range(len(self.matriz_mapa[i])):
                    r = pygame.Rect([j*self.spritesheet.tileLen, i*self.spritesheet.tileLen], [self.spritesheet.tileLen, self.spritesheet.tileLen])
                    self.quadrados.append((self.spritesheet.cortar_sprite(("sprite_" + sprites + '{:0>2}'.format(str(self.matriz_mapa[i][j])) + ".png")), (j*self.spritesheet.tileLen, i*self.spritesheet.tileLen)))

    def trocar_tile(self, pos, nova):
        self.quadrados[pos[0]*13 + pos[1]] = (self.spritesheet.cortar_sprite(("sprite_" + self.sprites + '{:0>2}'.format(nova) + ".png")), (pos[1]*self.spritesheet.tileLen, pos[0]*self.spritesheet.tileLen))

    def gerar_colisoes(self):
        # Retorna uma matriz com 0 para tiles passáveis, 1 para tiles com colisão
        matriz_colisao = copy.deepcopy(self.matriz_mapa)
        for i in range(len(matriz_colisao)):
            for j in range(len(matriz_colisao)):
                if matriz_colisao[i][j] == 1 or matriz_colisao[i][j] == 2:
                    matriz_colisao[i][j] = 1
                else:
                    matriz_colisao[i][j] = 0

        # Torna as extremidades colisão, independentemente do tipo de tile
        for i in range (self.largura):
            matriz_colisao[0]             [i] = 1
            matriz_colisao[i]             [0] = 1
            matriz_colisao[self.largura-1][i] = 1
            matriz_colisao[i][self.largura-1] = 1
        
        return matriz_colisao


    def mouse_collide(self):
        pass