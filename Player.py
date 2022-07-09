import os
import pygame
import json
from typing import Any
from Spritesheet import Spritesheet

class Player(pygame.sprite.Sprite):
    
    playerrect = pygame.Rect
    velocidade = 3

    def __init__(self, mapa, pos_inicial):
        pygame.sprite.Sprite.__init__(self)
        # Variáveis da Sprite:
        self.spritesheet = Spritesheet("Player")
        self.image = self.spritesheet.cortar_sprite("sprite_frach00.png")
        self.rect = self.image.get_rect()

        # Variáveis da posição e movimento:
        self.pos = pos_inicial
        self.dir = (0, 0)
        self.rect.center = (pos_inicial[1]*self.spritesheet.tileLen+self.spritesheet.tileLen/2, pos_inicial[0]*self.spritesheet.tileLen+self.spritesheet.tileLen/2)
        self.mapa = mapa
        self.mov_count = 0

        #Variáveis da animação:
        self.frame = 0
        self.frame_inicial = 0
        self.contagem_frame = 0
        self.frame_por_animacao = 6

        #Variáveis dos sistemas:
        self.interagindo = False
    
    def update(self, *args: Any, **kwargs: Any) -> None:
        self.rect.center += self.movimento()      
        return super().update(*args, **kwargs)

    def mover(self, posicao):
        # Move o sprite do Player
        self.rect.center = posicao 

    def movimento(self):
        # Realiza o movimento do Player no mapa em tiles
        movimento = pygame.Vector2()

        # Move o Player até a proxima tile
        if self.dir != (0,0):
            movimento += (self.dir[0]*self.velocidade, self.dir[1]*self.velocidade) 

            # Animação 
            self.contagem_frame += 1
            if self.contagem_frame == self.frame_por_animacao: self.animar(); self.contagem_frame = 0

            # Testa se o Player chegou na tile desejada
            if abs(self.rect.topleft[0] - self.pos[1]*self.spritesheet.tileLen) <= self.velocidade and abs(self.rect.topleft[1] - self.pos[0]*self.spritesheet.tileLen) <= self.velocidade:
                self.rect.topleft = (self.pos[1]*self.spritesheet.tileLen, self.pos[0]*self.spritesheet.tileLen)    
                self.dir = (0,0)
                self.image = self.spritesheet.cortar_sprite("sprite_frach" + '{:0>2}'.format(str(self.frame_inicial-1)) + ".png")
                self.teclas()    
        else:
            self.teclas()
        return movimento

    def teclas(self):
        # Pega o input e indica a direção do movimento quando possível
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_w] and self.pos[0] != 0 and self.mapa[self.pos[0]-1][self.pos[1]] != 1:
            self.dir = (0,-1)
            self.pos = (self.pos[0]-1, self.pos[1])
            self.image = self.spritesheet.cortar_sprite("sprite_frach04.png")
            self.frame_inicial = 4
        elif teclas[pygame.K_s] and self.pos[0] != len(self.mapa)-1 and self.mapa[self.pos[0]+1][self.pos[1]] != 1:    
            self.dir = (0,1)
            self.pos = (self.pos[0]+1, self.pos[1])
            self.image = self.spritesheet.cortar_sprite("sprite_frach01.png")
            self.frame_inicial = 1
        elif teclas[pygame.K_a] and self.pos[1] != 0 and self.mapa[self.pos[0]][self.pos[1]-1] != 1:      
            self.dir = (-1,0)
            self.pos = (self.pos[0], self.pos[1]-1)
            self.image = self.spritesheet.cortar_sprite("sprite_frach10.png")
            self.frame_inicial = 10
        elif teclas[pygame.K_d] and self.pos[1] != len(self.mapa[0])-1 and self.mapa[self.pos[0]][self.pos[1]+1] != 1: 
            self.dir = (1,0)
            self.pos = (self.pos[0], self.pos[1]+1)
            self.image = self.spritesheet.cortar_sprite("sprite_frach07.png")
            self.frame_inicial = 7

        if teclas[pygame.K_e] and not self.interagindo:
            self.interagir()

    def interagir():
        pass

    def animar(self):
        self.frame += 1
        if self.frame == 2: self.frame = 0
        self.image = self.spritesheet.cortar_sprite("sprite_frach" + '{:0>2}'.format(str(self.frame_inicial + self.frame)) + ".png")