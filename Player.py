import pygame
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

        # Variáveis da posição e movimento:
        self.pos = pos_inicial
        self.dir = (0, 0)
        self.rect.center = (pos_inicial[1]*self.spritesheet.tileLen+self.spritesheet.tileLen/2, pos_inicial[0]*self.spritesheet.tileLen+self.spritesheet.tileLen/2)
        self.mov_count = 0
        self.andando = False
        self.velocidade = 6

        # Variáveis da animação:
        self.frame = 0
        self.frame_inicial = 0
        self.contagem_frame = 0
        self.frame_por_animacao = 6

        # Variáveis dos sistemas:
        self.interagindo = False
        self.carregando = -1
    
    def update(self, *args: Any, **kwargs: Any) -> None:
        self.rect.center += self.movimento()
        if not self.interagindo:      
            self.teclas()  
        return super().update(*args, **kwargs)

    def set_mapa(self, colisao):
        self.colisoes = colisao

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
            if self.contagem_frame == self.frame_por_animacao: 
                self.animar()
                self.contagem_frame = 0

            # Testa se o Player chegou na tile desejada
            if abs(self.rect.topleft[0] - self.pos[1]*self.spritesheet.tileLen) <= self.velocidade and abs(self.rect.topleft[1] - self.pos[0]*self.spritesheet.tileLen) <= self.velocidade:
                self.rect.topleft = (self.pos[1]*self.spritesheet.tileLen, self.pos[0]*self.spritesheet.tileLen)    
                self.andando = False
                if self.carregando >= 0:
                    self.image = self.get_sprite(self.frame_inicial+11)
                else:
                    self.image = self.get_sprite(self.frame_inicial-1)
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
                    if self.carregando >= 0:
                        self.image = self.get_sprite(16)
                    else:
                        self.image = self.get_sprite(4)
                    self.frame_inicial = 4
                    self.andando = True
                else:
                    if self.carregando >= 0:
                        self.image = self.get_sprite(15)
                    else:
                        self.image = self.get_sprite(3)

            elif teclas[pygame.K_s]:
                self.dir = (0,1)
                if self.pos[0] != len(self.colisoes)-1 and self.colisoes[self.pos[0]+1][self.pos[1]] != 1:
                    self.pos = (self.pos[0]+1, self.pos[1])
                    if self.carregando >= 0:
                        self.image = self.get_sprite(13)
                    else:
                        self.image = self.get_sprite(1)
                    self.frame_inicial = 1
                    self.andando = True
                else:
                    if self.carregando >= 0:
                        self.image = self.get_sprite(12)
                    else:
                        self.image = self.get_sprite(0)

            elif teclas[pygame.K_a]:      
                self.dir = (-1,0)
                if self.pos[1] != 0 and self.colisoes[self.pos[0]][self.pos[1]-1] != 1:
                    self.pos = (self.pos[0], self.pos[1]-1)
                    if self.carregando >= 0:
                        self.image = self.get_sprite(22)
                    else:
                        self.image = self.get_sprite(10)
                    self.frame_inicial = 10
                    self.andando = True
                else:
                    if self.carregando >= 0:
                        self.image = self.get_sprite(21)
                    else:
                        self.image = self.get_sprite(9)

            elif teclas[pygame.K_d]:
                self.dir = (1,0)
                if self.pos[1] != len(self.colisoes[0])-1 and self.colisoes[self.pos[0]][self.pos[1]+1] != 1: 
                    self.pos = (self.pos[0], self.pos[1]+1)
                    if self.carregando >= 0:
                        self.image = self.get_sprite(19)
                    else:
                        self.image = self.get_sprite(7)
                    self.frame_inicial = 7
                    self.andando = True
                else:
                    if self.carregando >= 0:
                        self.image = self.get_sprite(18)
                    else:
                        self.image = self.get_sprite(6)

    def set_carregando(self, carregando):
        self.carregando = carregando
        if carregando >= 0:
            self.image = self.get_sprite(12)
        else:
            self.image = self.get_sprite(0)
        self.dir = (0,1)

    def proximo(self):
        # Retorna as coordenadas da tile que o player está olhando
        return (self.pos[0] + self.dir[1], self.pos[1] + self.dir[0])

    def get_sprite(self, num):
        return self.spritesheet.cortar_sprite("sprite_frach" + '{:0>2}'.format(str(num)) + ".png")

    def animar(self):
        self.frame += 1
        if self.frame == 2: 
            self.frame = 0

        if self.carregando >= 0:
            self.image = self.get_sprite(self.frame_inicial + self.frame + 12)
        else:
            self.image = self.get_sprite(self.frame_inicial + self.frame)