import pygame
import json
import os

class Spritesheet:
    def __init__(self, nome) -> None:
        self.spritesheet = pygame.image.load(os.path.join("Sprites", nome + ".png")).convert()
        # Guarda os dados do .json na self.metadata
        with open(os.path.join("Sprites", nome + ".json")) as d:
            self.metadata = json.load(d)
        self.tileLen = self.metadata["frames"][list(self.metadata["frames"])[0]]["frame"]["w"]


    def cortar_sprite(self, nome):
    # Corta a spritesheet no determinado lugar e retorna uma sprite
        meta_spr = self.metadata["frames"][nome]["frame"]
        x, y, w, h = meta_spr["x"], meta_spr["y"], meta_spr["w"], meta_spr["h"]
        spr = pygame.Surface((w, h))    
        spr.set_colorkey((0,0,0))
        spr.blit(self.spritesheet, (0,0), (x,y,w,h))
        return spr