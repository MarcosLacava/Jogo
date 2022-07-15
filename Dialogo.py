import pygame
import os

class Dialogo:
    def __init__(self, texto, tela) -> None:
        self.texto = texto
        self.pronto = False
        # Fonte do text box
        text_box_font = pygame.font.Font((os.path.join("Fonts", "yoster-island.regular.ttf")), 24)

        # Caixa do texto.
        box_rect = pygame.Rect(10, 614, 812, 208)
        box_surf = pygame.draw.rect(tela, (1,1,1,0.5), box_rect)
        box_stroke = pygame.draw.rect(tela, (255,255,255), box_rect, 5)

        # Conteúdo da caixa de texto.
        text_content = text_box_font.render(texto, False, (255,255,255))
        text_content_rect = text_content.get_rect(topleft = (30, 634))
        tela.blit(text_content, text_content_rect)

        #return box_surf, box_stroke
    
    def fechar():
        pass

    def pular():
        pass

class Dialogavel:
    def __init__(self, texto) -> None:
        self.texto = texto
        self.aberto = False

    def interagir(self, tela):
        if self.aberto:
            if self.dialogo.pronto:
                self.dialogo.fechar()
            else:
                self.dialogo.pular()     
        else:
            self.dialogo = Dialogo(self.texto, tela)