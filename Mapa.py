from encodings import CodecRegistryError
from operator import truediv
from os import remove
from re import I
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
        self.matriz_colisao = copy.deepcopy(self.matriz_mapa)

        for keys in interagiveis.keys(): # Adiciona cada interagível da lista no mapa
            if "tile_num" in interagiveis[keys]: # Verifica se o interagivel precisa de uma tile no mapa
                try: # Testa para ver se as coordenadas estão no nome
                    cordI, cordJ = keys.split()
                    cordI, cordJ = int(cordI), int(cordJ)

                except ValueError: # Caso contrário, assume que o valor está no dicionário
                    tile = interagiveis[keys]["tile_num"]
                    cordI, cordJ = interagiveis[keys]["pos"]

                tile = interagiveis[keys]["tile_num"]

                self.matriz_mapa[cordI][cordJ] = tile
                self.matriz_colisao[cordI][cordJ] = 1

        # Cria cada tile do mapa
        for i in range(len(self.matriz_mapa)):
            for j in range(len(self.matriz_mapa[i])):
                    sprite = self.get_sprite(str(self.matriz_mapa[i][j]))
                    r = sprite.get_rect(topleft=(j*self.spritesheet.tileLen, i*self.spritesheet.tileLen))
                    self.quadrados.append((sprite, r)) # Adiciona a tile na lista de tiles para dar Blit

    def trocar_tile(self, cords, nova, trocar_sprite = True):
        i, j = cords
        if trocar_sprite:
            sprite = self.get_sprite(nova)
            r = sprite.get_rect(topleft=(j*self.spritesheet.tileLen, i*self.spritesheet.tileLen))
            self.quadrados[i*13 + j] = (sprite, r)
        self.matriz_mapa[i][j] = nova

    def trocar_colisao(self, cords, colisao):
        i, j = cords
        self.matriz_colisao[i][j] = int(colisao)

    def get_sprite(self, num):
        return self.spritesheet.cortar_sprite("sprite_" + self.sprites + '{:0>2}'.format(num) + ".png")

    def gerar_colisoes(self):
        # Retorna uma matriz com 0 para tiles passáveis, 1 para tiles com colisão  
        for i in range(len(self.matriz_colisao)):
            for j in range(len(self.matriz_colisao)):
                if self.matriz_colisao[i][j] != 1 and self.matriz_colisao != 2:
                    self.matriz_colisao[i][j] = 0
                else:
                    self.matriz_colisao[i][j] = 1

        # Torna as extremidades colisão, independentemente do tipo de tile
        for i in range (self.largura):
            self.matriz_colisao[0]             [i] = 1
            self.matriz_colisao[i]             [0] = 1
            self.matriz_colisao[self.largura-1][i] = 1
            self.matriz_colisao[i][self.largura-1] = 1
        
        return self.matriz_colisao
