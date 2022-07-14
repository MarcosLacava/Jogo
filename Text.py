import pygame
import pygame.freetype
import os

class Text():

    def __init__(self, text, color, surface, x, y):
        # Fontes
        self.title_font = pygame.freetype.SysFont(pygame.freetype.get_default_font(), 64)
        self.text_box_font = pygame.font.Font((os.path.join("Fonts", "yoster-island.regular.ttf")), 24)
        
        self.text = text
        self.color = color
        self.surface = surface
        self.pos = int(x), int(y)


    def text_box(self):

        box_rect = pygame.Rect(10, 614, 812, 208)
        box_surf = pygame.draw.rect(self.surface, (1,1,1,0.5), box_rect)
        box_stroke = pygame.draw.rect(self.surface, (255,255,255), box_rect, 5)

        text_content = self.text_box_font.render(self.text, False, self.color)
        text_content_rect = text_content.get_rect(topleft = (self.pos))
        self.surface.blit(text_content, text_content_rect)

        return box_surf, box_stroke
        
        