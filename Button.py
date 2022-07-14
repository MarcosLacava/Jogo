import pygame
import os

class Button:
    def __init__(self, name, pos) -> None:

        self.surf_default = pygame.image.load((os.path.join("Sprites","buttons", name + ".png")))
        self.rect_default = self.surf_default.get_rect(center = (pos))

        self.surf_hover = pygame.image.load((os.path.join("Sprites","buttons", name + "-hover.png")))
        self.rect_hover = self.surf_hover.get_rect(center = (pos))

        self.name = name

    def blit_button(self, surf):

        surf.blit(self.surf_default, self.rect_default)
        mx, my = pygame.mouse.get_pos()

        if self.rect_default.collidepoint((mx,my)):
            surf.blit(self.surf_hover, self.rect_hover)
            return True
        return False