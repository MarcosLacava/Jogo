import pygame
import os
import Spritesheet

class Scroll:
    def __init__(self, surface) -> None:
        
        # Spritesheet das palavras
        self.sprites = "scroll_words"
        self.spritesheet = Spritesheet.Spritesheet(self.sprites)
        
        # Imagem do pergaminho
        self.img = pygame.image.load((os.path.join("Sprites","scroll","scroll.png"))).convert_alpha()
        self.img_rect = self.img.get_rect(topleft = (0,0))
        self.surface = surface
        self.word_list = []
        self.rect_list = []

        # Imagens das palavras que serão colocadas no pergaminho
        for word in range(10):
            self.word_list.append(self.get_sprite(word))
            self.rect_list.append(self.word_list[word].get_rect(topleft = (10, 150 + 50*word)))

        
    def get_sprite(self, num):
        return self.spritesheet.cortar_sprite('{:0>2}'.format(num) + ".png")


    def open_scroll(self, surface):

        surface.blit(self.img, self.img_rect)
        word = 0
        surface.blit(self.word_list[word],self.rect_list[word])
       # for word in range(10):
        
    
    def write_scroll(self):
        mx, my = pygame.mouse.get_pos()
        click = False


