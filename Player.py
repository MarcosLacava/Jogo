import this
import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Player_Sprite.png").convert()
        self.rect = self.image.get_rect()

    def mover(self, posicao):
        self.rect.center = posicao 
        #fasdkopjfopas
    def fodr():
        pass