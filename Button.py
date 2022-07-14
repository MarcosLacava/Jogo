import pygame
import os

class Button:
    def __init__(self, name, pos) -> None:

        self.surf = pygame.image.load((os.path.join("Sprites","buttons", name + ".png")))
        self.rect = self.surf.get_rect(center = (pos))
        self.name = name

    def blit_button(self, surf):

        surf.blit(self.surf, self.rect)
        mx, my = pygame.mouse.get_pos()

        if self.rect.collidepoint((mx,my)):
            self.surf = pygame.image.load((os.path.join("Sprites","buttons", self.name + "-hover.png")))
            return True
        else:
            self.surf = pygame.image.load((os.path.join("Sprites","buttons", self.name + ".png")))
        
        return False