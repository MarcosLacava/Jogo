import pygame
import pygame.freetype
import os

class Text():

    def text_box(self, surface, text):
        
        # Fonte do text box
        text_box_font = pygame.font.Font((os.path.join("Fonts", "yoster-island.regular.ttf")), 24)

        # Caixa do texto.
        box_rect = pygame.Rect(10, 614, 812, 208)
        box_surf = pygame.draw.rect(surface, (1,1,1,0.5), box_rect)
        box_stroke = pygame.draw.rect(surface, (255,255,255), box_rect, 5)

        # Conteúdo da caixa de texto.
        text_content = text_box_font.render(text, False, (255,255,255))
        text_content_rect = text_content.get_rect(topleft = (30, 634))
        surface.blit(text_content, text_content_rect)

        return box_surf, box_stroke
        
        