import pygame
import os

class Dialogo:
    def __init__(self, texto) -> None:
        self.textos = texto
        self.pronto = False
        self.linha = 0

        # Animação de digitar
        self.digitando = False
        self.digito = 0
        self.digitos_totais = len(texto[0])
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
        # Desenha o diálogo de acordo com a animação
        self.digito += 1 # Incrementa o dígito da animação

        pygame.draw.rect(tela, self.cor_borda, self.box_rect)
        pygame.draw.rect(tela, self.cor, self.box_rect, self.largura_borda)

        # Desenha o texto até o dígito da animação
        text_content = self.text_box_font.render(self.textos[self.linha][0 : self.digito], False, (255,255,255))
        text_content_rect = text_content.get_rect(topleft = (30, 634)) 

        tela.blit(text_content, text_content_rect)
    def fechar():
        pass

    def passar_linha(self):
        # Verifica se a animação acabou, senão termina ela
        if self.digito < len(self.textos[self.linha]):
            self.digito = len(self.textos[self.linha])
            return True

        # Passa para a próxima string na lista do texto
        self.linha += 1
        if self.linha >= len(self.textos):
            return False

        # Lógica da animação
        self.digitando = True
        self.digito = 0
        self.digitos_totais = len(self.textos[self.linha])

        return True