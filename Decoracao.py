from email.mime import image
import pygame

class Decoracao(pygame.sprite.Sprite):

    def __init__(self, imagem):
        pygame.sprite.Sprite.__init__(self)
        self.image = imagem
        self.rect = imagem.get_rect()