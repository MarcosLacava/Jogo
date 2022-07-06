import os
from Player import Player
import sys, pygame, pygame.freetype
from Mapa import Mapa

pygame.init()

# Game Clock
clock = pygame.time.Clock()

# Fonte padrão do sistema
fonte = pygame.freetype.SysFont(pygame.freetype.get_default_font(), 12) 

preto = 0, 0, 0
branco = 255, 255, 255

# Cria a tela e lista de sprites
size = width, height = 1280, 720
tela = pygame.display.set_mode(size, pygame.RESIZABLE), pygame.FULLSCREEN
lista_sprites = pygame.sprite.Group()
erro = pygame.image.load(os.path.join("Sprites", "Erro.png")).convert()



#Criação do Mapa
matriz_mapa = [
        [1, 1, 1, 1, 0, 0, 1, 1, 1, 1], 
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
        [1, 0, 1, 0, 0, 0, 0, 0, 0, 1], 
        [1, 0, 0, 0, 0, 0, 1, 0, 0, 1], 
        [0, 0, 0, 0, 0, 1, 0, 0, 0, 0], 
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0], 
        [1, 0, 0, 1, 0, 0, 1, 1, 0, 1], 
        [1, 0, 0, 0, 0, 0, 1, 1, 0, 1], 
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
        [1, 1, 1, 1, 0, 0, 1, 1, 1, 1], 
        [0, 0, 0, 0, 0, 1, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [1, 0, 0, 0, 0, 0, 1, 1, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 0, 1], 
        [1, 1, 1, 0, 0, 0, 0, 0, 0, 1], 
        [1, 1, 1, 1, 0, 0, 1, 1, 1, 1], 
       ]

mapaTeste = Mapa(matriz_mapa.copy())

# Criação do player
player = Player(matriz_mapa, (3,1))
lista_sprites.add(player)

while True:
    #Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.type == pygame.K_F11: pygame.display.toggle_fullscreen()
        
    player.update()

    #Renderização
    tela.fill(branco)
    tela.blits(mapaTeste.quadrados)
    fonte.render_to(tela, [0, 0], str(player.movimento()), branco)

    lista_sprites.draw(tela)

    pygame.display.update()
    clock.tick(30)

    