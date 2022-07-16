from email.errors import MultipartConversionError
from typing import Any
import pygame

from Player import Player


class Estatua(pygame.sprite.Sprite):

    def __init__(self, pos, tipo, sprite) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.tileLen = 64
        self.image = sprite
        self.rect = self.image.get_rect()
        self.carregada = False
        self.set_pos(pos)
        self.tipo = tipo

    def update(self, *args: Any, **kwargs: Any) -> None:
        if self.carregada:
            x, y = self.player_rect.center
            self.rect.center = (x, y - self.tileLen)

        return super().update(*args, **kwargs)

    def set_pos(self, nova_pos):
        self.set_pos(nova_pos)
        self.carregada = False

    def carregar(self, playerrect):
        self.player_rect = playerrect
        self.carregada = True

    def descarregar(self, cords):
        self.carregada = False
        self.set_pos(cords)

    def set_pos(self, nova_pos):
        self.rect.center = nova_pos[1] * self.tileLen + self.tileLen // 2, nova_pos[0] * self.tileLen + self.tileLen // 2