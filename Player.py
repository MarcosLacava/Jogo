from cmath import rect
from msilib import sequence
import sys, pygame
from turtle import pos
from telnetlib import GA
from typing import Any

class Player(pygame.sprite.Sprite):
    playerrect = pygame.Rect
    velocidade = 3

    def __init__(self, mapa, pos_inicial, tileLen):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("sprite_FRACH00.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.pos = pos_inicial
        self.dir = (0, 0)
        self.tileLen = tileLen
        self.rect.center = (pos_inicial[1]*tileLen+tileLen/2, pos_inicial[0]*tileLen+tileLen/2)
        self.mapa = mapa
        
    def mover(self, posicao):
        self.rect.center = posicao 

    def movimento(self):
        teclas = pygame.key.get_pressed()
        movimento = pygame.Vector2()

        if self.dir != (0,0):
            movimento += (self.dir[0] * self.velocidade, self.dir[1] * self.velocidade)
            if not(abs(self.rect.x - self.pos[1]*self.tileLen) >= 0.1*self.velocidade != abs(self.rect.y + self.pos[0]*self.tileLen) >= 0.1*self.velocidade):
                self.dir = (0,0)
                print("aa")
        else:
            if teclas[pygame.K_w] and self.dir == (0,0) and self.pos[0] != 0 and self.mapa[self.pos[0]+1][self.pos[1]] == 0:
                self.dir = (0,-1)
                self.pos = (self.pos[0]+1, self.pos[1])
            elif teclas[pygame.K_s]:    
                movimento += (0, 1 * self.velocidade)
            elif teclas[pygame.K_a]:      
                movimento += (-1 * self.velocidade, 0)
            elif teclas[pygame.K_d]: 
                movimento += (1 * self.velocidade, 0)

        return movimento
    
    def update(self, *args: Any, **kwargs: Any) -> None:
        self.rect.center += self.movimento()
        return super().update(*args, **kwargs)
