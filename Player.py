import os
import pygame
import json
from typing import Any
from Spritesheet import Spritesheet

class Player(pygame.sprite.Sprite):
    
    playerrect = pygame.Rect
    velocidade = 1

    def __init__(self, mapa, pos_inicial):
        pygame.sprite.Sprite.__init__(self)
        # Inicialização do Player
        self.spritesheet = Spritesheet("Player")
        self.image = self.spritesheet.cortar_sprite("frach_sprite00.png")
        self.rect = self.image.get_rect()
        self.pos = pos_inicial
        self.dir = (0, 0)
        self.rect.center = (pos_inicial[1]*self.spritesheet.tileLen+self.spritesheet.tileLen/2, pos_inicial[0]*self.spritesheet.tileLen+self.spritesheet.tileLen/2)
        self.mapa = mapa
        self.mov_count = 0
        self.anim_frame = 0
        
    def mover(self, posicao):
        # Move o sprite do Player
        self.rect.center = posicao 

    def movimento(self):
        # Realiza o movimento do Player no mapa em tiles
        movimento = pygame.Vector2()
        # Animação

        # Move o Player até a proxima tile
        if self.dir != (0,0):
            movimento += (self.dir[0]*self.velocidade, self.dir[1]*self.velocidade)
            
            # Testa se o Player chegou na tile desejada
            if abs(self.rect.topleft[0] - self.pos[1]*self.spritesheet.tileLen) <= self.velocidade and abs(self.rect.topleft[1] - self.pos[0]*self.spritesheet.tileLen) <= self.velocidade:
                self.rect.topleft = (self.pos[1]*self.spritesheet.tileLen, self.pos[0]*self.spritesheet.tileLen)    
                self.dir = (0,0)
                self.teclas()       
        else:
            self.teclas()
        return movimento

    def teclas(self):
        # Pega o input e move quando possível
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_w] and self.pos[0] != 0 and self.mapa[self.pos[0]-1][self.pos[1]] != 1:
            self.dir = (0,-1)
            self.pos = (self.pos[0]-1, self.pos[1])
            self.image = self.spritesheet.cortar_sprite("frach_sprite05.png")
        elif teclas[pygame.K_s] and self.pos[0] != len(self.mapa)-1 and self.mapa[self.pos[0]+1][self.pos[1]] != 1:    
            self.dir = (0,1)
            self.pos = (self.pos[0]+1, self.pos[1])
            self.image = self.spritesheet.cortar_sprite("frach_sprite01.png")
        elif teclas[pygame.K_a] and self.pos[1] != 0 and self.mapa[self.pos[0]][self.pos[1]-1] != 1:      
            self.dir = (-1,0)
            self.pos = (self.pos[0], self.pos[1]-1)
            self.image = self.spritesheet.cortar_sprite("frach_sprite09.png")
        elif teclas[pygame.K_d] and self.pos[1] != len(self.mapa[0])-1 and self.mapa[self.pos[0]][self.pos[1]+1] != 1: 
            self.dir = (1,0)
            self.pos = (self.pos[0], self.pos[1]+1)
            self.image = self.spritesheet.cortar_sprite("frach_sprite07.png")

    def update(self, *args: Any, **kwargs: Any) -> None:
        self.rect.center += self.movimento()
        self.anim_frame 
        return super().update(*args, **kwargs)

    