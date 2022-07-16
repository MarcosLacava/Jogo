import pygame
import os

class Dialogo:
    def __init__(self, texto) -> None:
        self.textos = texto
        self.pronto = False
        self.linha = 0
        # Fonte do text box
        self.text_box_font = pygame.font.Font((os.path.join("Fonts", "yoster-island.regular.ttf")), 24)
        # Cores
        self.cor_borda = (1,1,1,0.5)
        self.cor = (255,255,255)
        # Caixa do texto.
        self.box_rect = pygame.Rect(10, 614, 812, 208)
        self.largura_borda = 5

        # self.box_surf = pygame.draw.rect(tela, self.cor_borda, self.box_rect)
        # self.box_stroke = pygame.draw.rect(tela, self.cor, self.box_rect, self.largura_borda)

        # Conteúdo da caixa de texto.
        

        #return box_surf, box_stroke
    def draw(self, tela):
        # Desenha todo o diálogo

        pygame.draw.rect(tela, self.cor_borda, self.box_rect)
        pygame.draw.rect(tela, self.cor, self.box_rect, self.largura_borda)

        text_content = self.text_box_font.render(self.textos[self.linha], False, (255,255,255))
        text_content_rect = text_content.get_rect(topleft = (30, 634)) 

        tela.blit(text_content, text_content_rect)
    def fechar():
        pass

    def passar_linha(self):
        self.linha += 1
        if self.linha >= len(self.textos):
            return False
        return True

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