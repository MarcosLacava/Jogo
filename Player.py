from cmath import rect
from msilib import sequence
import sys, pygame, Game
from telnetlib import GA
from typing import Any

class Player(pygame.sprite.Sprite):
    playerrect = pygame.Rect
    andando = False
    velocidade = 3

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Player_Sprite.png").convert()
        self.rect = self.image.get_rect()
        self.rect.center = (150, 700)
        
    def mover(self, posicao):
        self.rect.center = posicao 

    def movimento(self):
        teclas = pygame.key.get_pressed()
        movimento = pygame.Vector2()

        if teclas[pygame.K_w]:
            andando = True
            movimento += (0, -1 * self.velocidade)
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
