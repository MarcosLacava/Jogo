from cmath import rect
from msilib import sequence
import sys, pygame
from turtle import pos
from telnetlib import GA
from typing import Any

class Player(pygame.sprite.Sprite):
    playerrect = pygame.Rect
    velocidade = 7

    def __init__(self, mapa, pos_inicial, tileLen):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("sprite_FRACH00.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.pos = pos_inicial
        self.dir = (0, 0)
        self.tileLen = tileLen
        self.rect.center = (pos_inicial[1]*tileLen+tileLen/2, pos_inicial[0]*tileLen+tileLen/2)
        self.mapa = mapa
        self.mov_count = 0
        
    def mover(self, posicao):
        self.rect.center = posicao 

    def movimento(self):
        
        movimento = pygame.Vector2()

        if self.dir != (0,0):
            movimento += (self.dir[0] * self.tileLen/30, self.dir[1]*self.tileLen/(30/self.velocidade))
            self.mov_count += 1
            if self.mov_count >= 30/self.velocidade:
                self.dir = (0,0)
                self.mov_count = 0
                self.input()
        else:
            self.input()
        return movimento

    def input(self):
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_w] and self.pos[0] != 0 and self.mapa[self.pos[0]-1][self.pos[1]] == 0:
            self.dir = (0,-1)
            self.pos = (self.pos[0]-1, self.pos[1])
        elif teclas[pygame.K_s] and self.pos[0] != len(self.mapa) and self.mapa[self.pos[0]+1][self.pos[1]] == 0:    
            self.dir = (0,1)
            self.pos = (self.pos[0]+1, self.pos[1])
        elif teclas[pygame.K_a] and self.pos[0] != 0 and self.mapa[self.pos[0]-1][self.pos[1]] == 0:      
            movimento += (-1 * self.velocidade, 0)
        elif teclas[pygame.K_d] and self.pos[0] != 0 and self.mapa[self.pos[0]-1][self.pos[1]] == 0: 
            movimento += (1 * self.velocidade, 0)

    def update(self, *args: Any, **kwargs: Any) -> None:
        self.rect.center += self.movimento()
        return super().update(*args, **kwargs)
