import pygame
import os
import Spritesheet
import random
import copy

class Scroll:
    def __init__(self, surface) -> None:
        
        # Spritesheet das palavras
        self.sprites = "scroll_words"
        self.spritesheet = Spritesheet.Spritesheet(self.sprites)
        
        # Imagem do pergaminho
        self.img = pygame.image.load((os.path.join("Sprites","scroll","scroll.png"))).convert_alpha()
        self.img_rect = self.img.get_rect(topleft = (0,0))
        self.surface = surface

        # Lista contendo tuplas, as quais contém a superície e o retângulo de cada palavra
        self.word_list = []
        # Lista que será preenchida durante a realiação do puzzle
        self.new_word_list = []

        # Imagens das palavras que serão colocadas no pergaminho
        for word in range(10):
            self.word_list.append((self.get_sprite(word), self.get_sprite(word).get_rect(topleft = (10, 200 + 50*word))))

        # Lista das palavras com suas posições randomizadas
        self.word_list_shuffled = []
        self.word_list_shuffled = copy.copy(self.word_list)
        random.shuffle(self.word_list_shuffled)


        # Imagem de fundo
        self.bg_img = pygame.image.load((os.path.join("Sprites","scroll","table_bg.png")))
        self.bg_img_rect = self.bg_img.get_rect(topleft = (0,0))

        # Grava o número da próxima linha a receber uma palavra
        self.line_num = 0

        # Verifica se o pergaminho está completo
        self.complete = False


    def get_sprite(self, num):
        return self.spritesheet.cortar_sprite('{:0>2}'.format(num) + ".png")


    def open_scroll(self, surface):

        # Dá display na imagem de fundo
        surface.blit(self.bg_img,self.bg_img_rect)

        # Dá display na imagem do pergaminho
        surface.blit(self.img, self.img_rect)

        # Dá display em cada palavra do puzzle
        for word in range(10):
            surface.blit(self.word_list[word][0],self.word_list_shuffled[word][1])
        
    
    def write_scroll(self, pos, click):

        line_list = [(538,228),(610,274),(400,316),(430,361),(600,406),(390,452),(270,493),(284,537),(312,581),(380,669)]

        if click:
            for word in self.word_list:
                if self.line_num < 10:
                    if word[1].collidepoint(pos):

                        self.new_word_list.append(word)

                        word[1].topleft = line_list[self.line_num]
                        self.line_num += 1

        if self.line_num == 10:
            self.complete = True


    def check_scroll(self):
        if self.complete:
            for word in range(10):
                if self.word_list_shuffled[word][0] == self.new_word_list[word][0]:
                    return True
                else:
                    return False

    
    def release_sword(self):
        pass