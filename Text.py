import pygame
import pygame.freetype

class Text():

    def __init__(self, text, font, color, surface, x, y):
        # Fontes
        self.title_font = pygame.freetype.SysFont(pygame.freetype.get_default_font(), 64)
        self.fonte = pygame.freetype.SysFont(pygame.freetype.get_default_font(), 24)
        
        self.text = text
        self.font = font
        self.color = color
        self.surface = surface
        self.pos = int(x), int(y)


    def text_box(self):

        box_rect = pygame.Rect(10, 556, 812, 266)
        box_surf = pygame.draw.rect(self.surface, (1,1,1,0.5), box_rect)
        box_stroke = pygame.draw.rect(self.surface, (255,255,255), box_rect, 5)

        self.text_content = self.font.render(self.text, self.color)
        self.text_content[1].topleft = self.pos
        self.surface.blit(self.text_content[0],self.text_content[1])

        # tela.blit(box_surf, box_rect)
        # tela.blit(box_stroke, box_rect)
        return box_surf, box_stroke
        
        