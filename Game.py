from inspect import FullArgSpec
import os
from tkinter import EventType
from Player import Player
import sys, pygame, pygame.freetype
from Mapa import Mapa

pygame.init()

# Estados do jogo:
main_menu = True
pause_menu = False
game = False

# Cores
preto = 0, 0, 0
branco = 255, 255, 255

# Game Clock
clock = pygame.time.Clock()

# Fonte padrão do sistema
fonte = pygame.freetype.SysFont(pygame.freetype.get_default_font(), 24) 

# Função para desenhar texto na tela.
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, color, preto)
    textobj[1].topleft = (x, y)
    surface.blit(textobj[0],textobj[1])


# Cria a tela e lista de sprites
monitor_size = [pygame.display.Info().current_w, pygame.display.Info().current_h]
size = width, height = 832, 832
tela = pygame.display.set_mode(size, pygame.RESIZABLE)
lista_sprites = pygame.sprite.Group()

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

click = False

# Main Loop
while True:
    # Menu Loop
    while main_menu:
        tela.fill((1,1,1))
        draw_text('A DIRETORIA', fonte, branco, tela, 100, 100)

        mx, my = pygame.mouse.get_pos()
        
        button_1 = pygame.Rect(100, 200, 200, 50)
        button_2 = pygame.Rect(100, 400, 200, 50)

        if button_1.collidepoint((mx, my)):
            if click:
                main_menu = False
                game = True
                break
        if button_2.collidepoint((mx, my)):
            if click:
                pass

        pygame.draw.rect(tela, (255,0,0), button_1)
        pygame.draw.rect(tela, (255,0,0), button_2)

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
                    print(click)
                    
        pygame.display.update()
        clock.tick(30)

    # Game Loop
    while game:
        #Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

            if event.type == pygame.VIDEORESIZE:
                if not fullscreen:
                    tela = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
        
            if  event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    fullscreen = not fullscreen
                    if fullscreen:
                        tela = pygame.display.set_mode(monitor_size, pygame.FULLSCREEN)
                    else:
                        tela = pygame.display.set_mode((size), pygame.RESIZABLE)

        player.update()

        #Renderização
        tela.fill(preto)
        tela.blits(mapaTeste.quadrados)
        fonte.render_to(tela, [0, 0], str(player.movimento()), branco)

        lista_sprites.draw(tela)

        pygame.display.update()
        clock.tick(30)