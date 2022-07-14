import os
import pygame
import json
from typing import Any
from Spritesheet import Spritesheet

class Player(pygame.sprite.Sprite):

    def __init__(self, pos_inicial):
        pygame.sprite.Sprite.__init__(self)
        # Variáveis da Sprite:
        self.spritesheet = Spritesheet("Player")
        self.image = self.spritesheet.cortar_sprite("sprite_frach00.png")
        self.rect = self.image.get_rect()
        self.tileLen = 64
        self.playerrect = pygame.Rect

        # Variáveis da posição e movimento:
        self.pos = pos_inicial
        self.dir = (0, 0)
        self.rect.center = (pos_inicial[1]*self.spritesheet.tileLen+self.spritesheet.tileLen/2, pos_inicial[0]*self.spritesheet.tileLen+self.spritesheet.tileLen/2)
        self.mov_count = 0
        self.andando = False
        self.velocidade = 6

        #Variáveis da animação:
        self.frame = 0
        self.frame_inicial = 0
        self.contagem_frame = 0
        self.frame_por_animacao = 6

        #Variáveis dos sistemas:
        self.interagindo = False
    
    def update(self, *args: Any, **kwargs: Any) -> None:
        self.rect.center += self.movimento()      
        self.teclas()  
        return super().update(*args, **kwargs)

    def set_mapa(self, colisao, interagiveis):
        self.colisoes = colisao
        self.interagiveis = interagiveis
        #self.mapa_interacoes = interacao

    def set_pos(self, nova_pos):
        # Reposiciona o player no centro da tile indicada
        # Necessário para mudanças abruptas de movimento (ex: nova posição depois de interagir com a porta) 
        self.rect.center = nova_pos[1] * self.tileLen + self.tileLen // 2, nova_pos[0] * self.tileLen + self.tileLen // 2
        self.pos = nova_pos

    def get_interagindo(self):
        return self.interagindo

    def movimento(self):
        # Realiza o movimento do Player no mapa em tiles
        movimento = pygame.Vector2()

        # Move o Player até a proxima tile
        if self.andando:
            movimento += (self.dir[0]*self.velocidade, self.dir[1]*self.velocidade) 

            # Animação 
            self.contagem_frame += 1
            if self.contagem_frame == self.frame_por_animacao: self.animar(); self.contagem_frame = 0

            # Testa se o Player chegou na tile desejada
            if abs(self.rect.topleft[0] - self.pos[1]*self.spritesheet.tileLen) <= self.velocidade and abs(self.rect.topleft[1] - self.pos[0]*self.spritesheet.tileLen) <= self.velocidade:
                self.rect.topleft = (self.pos[1]*self.spritesheet.tileLen, self.pos[0]*self.spritesheet.tileLen)    
                self.andando = False
                self.image = self.spritesheet.cortar_sprite("sprite_frach" + '{:0>2}'.format(str(self.frame_inicial-1)) + ".png")   
                self.teclas()
        return movimento

    def teclas(self):
        # Pega o input e indica a direção do movimento quando possível

        teclas = pygame.key.get_pressed()
        if not self.andando:
            if teclas[pygame.K_w]:
                self.dir = (0,-1)
                if self.pos[0] != 0 and self.colisoes[self.pos[0]-1][self.pos[1]] != 1:
                    self.pos = (self.pos[0]-1, self.pos[1])        
                    self.image = self.spritesheet.cortar_sprite("sprite_frach04.png")
                    self.frame_inicial = 4
                    self.andando = True
                else:
                    self.image = self.spritesheet.cortar_sprite("sprite_frach03.png")

            elif teclas[pygame.K_s]:
                self.dir = (0,1)
                if self.pos[0] != len(self.colisoes)-1 and self.colisoes[self.pos[0]+1][self.pos[1]] != 1:
                    self.pos = (self.pos[0]+1, self.pos[1])
                    self.image = self.spritesheet.cortar_sprite("sprite_frach01.png")
                    self.frame_inicial = 1
                    self.andando = True
                else:
                    self.image = self.spritesheet.cortar_sprite("sprite_frach00.png")

            elif teclas[pygame.K_a]:      
                self.dir = (-1,0)
                if self.pos[1] != 0 and self.colisoes[self.pos[0]][self.pos[1]-1] != 1:
                    self.pos = (self.pos[0], self.pos[1]-1)
                    self.image = self.spritesheet.cortar_sprite("sprite_frach10.png")
                    self.frame_inicial = 10
                    self.andando = True
                else:
                    self.image = self.spritesheet.cortar_sprite("sprite_frach09.png")

            elif teclas[pygame.K_d]:
                self.dir = (1,0)
                if self.pos[1] != len(self.colisoes[0])-1 and self.colisoes[self.pos[0]][self.pos[1]+1] != 1: 
                    self.pos = (self.pos[0], self.pos[1]+1)
                    self.image = self.spritesheet.cortar_sprite("sprite_frach07.png")
                    self.frame_inicial = 7
                    self.andando = True
                else:
                    self.image = self.spritesheet.cortar_sprite("sprite_frach06.png")

    def proximo(self):
        # Retorna as coordenadas da tile que o player está olhando
        return (self.pos[0] + self.dir[1], self.pos[1] + self.dir[0])

    def animar(self):
        self.frame += 1
        if self.frame == 2: self.frame = 0
        self.image = self.spritesheet.cortar_sprite("sprite_frach" + '{:0>2}'.format(str(self.frame_inicial + self.frame)) + ".png")