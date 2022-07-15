import pygame
import os

class Gun:
    def __init__(self) -> None:
        mx, my = pygame.mouse.get_pos()
        self.crosshair = pygame.image.load((os.path.join("Sprites","crosshair","sprite_crosshair-empty.png"))).convert_alpha
        self.crosshair_rect = self.crosshair.get_rect(center = (mx,my))


    def loaded(self, tela):
        tela.blit(self.crosshair, self.crosshair_rect)