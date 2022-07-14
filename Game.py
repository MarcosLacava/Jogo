import os
from pickletools import pyinteger_or_bool
from Player import Player
import sys, pygame, pygame.freetype
from Mapa import Mapa
import copy
import Text

import Porta

pygame.init()

# Estados do jogo:
main_menu = True
pause_menu = False
game = False

# Cores
preto = 1, 1, 1
branco = 255, 255, 255

# Game Clock
clock = pygame.time.Clock()

# Fontes
title_font = pygame.freetype.SysFont(pygame.freetype.get_default_font(), 64)
fonte = pygame.freetype.SysFont(pygame.freetype.get_default_font(), 24)


# Função para desenhar texto na tela
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, color)
    textobj[1].topleft = (x, y)
    surface.blit(textobj[0],textobj[1])
    if game:
        font = fonte
        color = preto

        

# Musicas
main_menu_theme = os.path.join('Music','alexander-nakarada-space-ambience.ogg')

def music(state, name):
    if state:
        pygame.mixer.music.load(name)
        pygame.mixer.music.play(0, 0, 1000)
        pygame.mixer.music.set_volume(0.5)
    else:
        pygame.mixer.music.fadeout(1000)

# Cria a tela e lista de sprites
monitor_size = [pygame.display.Info().current_w, pygame.display.Info().current_h]
size = width, height = 832, 832
tela = pygame.display.set_mode(size)
pygame.display.set_caption("A DIRETORIA")
lista_sprites = pygame.sprite.Group()

dialogo = Text.Text("Marcos é fodaasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasd", title_font, (branco), tela, 25, 581)

# Criação do Mapa
matriz_mapa = [
        [2, 2 , 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
        [2, 1 , 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2], 
        [2, 3 , 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 2], 
        [2, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 2], 
        [2, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 2],
        [2, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 2], 
        [2, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 2], 
        [2, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 2], 
        [2, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 2], 
        [2, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 2], 
        [2, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 2], 
        [2, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 2], 
        [2, 2 , 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
       ]

interagiveis = {(5, 0) : Porta.Porta(cords=(5, 0), destino="SALA2", tile_num=9),
                (5, 12) : Porta.Porta(cords=(5, 12), destino="SALA3", tile_num=9)}


salas = {"DIRETORIA":True,
         "SALA1":False,
         "SALA2":False,
         "SALA3":False,
         "SALA4":False,
         "SALA5":False,
         "SALA6":False,
         "SALA7":False,
         }

mapaTeste = Mapa(copy.deepcopy(matriz_mapa), "main-room", interagiveis)

# Criação do player
player = Player((8,6))
player.set_mapa(mapaTeste.gerar_colisoes(), interagiveis)
lista_sprites.add(player)


click = False
music(main_menu, main_menu_theme)

def trocar_sala(nova):
    for i in salas:
        i = False
    salas[nova] = True
    print(salas[nova])
    
def renderização():
    # Faz todas as renderizações necessárias
    tela.fill(preto)
    tela.blits(mapaTeste.quadrados)
    fonte.render_to(tela, [0, 0], str(player.movimento()), branco)

    lista_sprites.draw(tela)

    pygame.display.update()
    clock.tick(30)
  
# Main Loop
while True:
    # Menu Loop
    while main_menu:
        # Event loop do menu principal
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


        # Imagens utilizadas na interface do menu principal e seus retângulos
        bg = pygame.image.load((os.path.join('Sprites','menu','bg_main-menu.png'))).convert()
        tela.blit(bg,(0,0))

        play_button = pygame.image.load((os.path.join('Sprites','menu','play_button.png'))).convert_alpha()
        play_button_rect = play_button.get_rect(center = (416,416))
        tela.blit(play_button, play_button_rect)

        quit_button = pygame.image.load((os.path.join('Sprites','menu','quit_button.png'))).convert_alpha()
        quit_button_rect = quit_button.get_rect(center = (416, 516))
        tela.blit(quit_button, quit_button_rect)

        # Capturar a posição x e y do mouse
        mx, my = pygame.mouse.get_pos()

        # Condição para o botão de play ser acessado:
        if play_button_rect.collidepoint((mx, my)):
            play_button = pygame.image.load((os.path.join('Sprites','menu','play_button-hover.png'))).convert_alpha()
            tela.blit(play_button, play_button_rect)
            if click:
                main_menu = False
                music(main_menu, main_menu_theme)
                game = True
                break

        # Condição para o botão de quit ser acessado:
        if quit_button_rect.collidepoint((mx, my)):
            quit_button = pygame.image.load((os.path.join('Sprites','menu','quit_button-hover.png'))).convert_alpha()
            tela.blit(quit_button, quit_button_rect)
            if click:
                pygame.quit()
                sys.exit()
                    
        pygame.display.update()
        clock.tick(30)

    # Game Loop
    while salas['DIRETORIA']:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_e and not player.interagindo:
                    cords = player.proximo()
                    if mapaTeste.matriz_mapa[cords[0]][cords[1]] == 9: # Porta
                        trocar_sala(interagiveis[cords].destino)

        player.update()
        renderização()
            
