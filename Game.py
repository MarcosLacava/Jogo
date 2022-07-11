import os
from Player import Player
import sys, pygame, pygame.freetype
from Mapa import Mapa
import copy

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

# Fontes
title_font = pygame.freetype.SysFont(pygame.freetype.get_default_font(), 64)
fonte = pygame.freetype.SysFont(pygame.freetype.get_default_font(), 24) 

# Função para desenhar texto na tela
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, color, preto)
    textobj[1].topleft = (x, y)
    surface.blit(textobj[0],textobj[1])

# Musica
if main_menu:
    music = pygame.mixer.music.load(os.path.join('Music','NGGYU.ogg'))
    pygame.mixer.music.play(0, 0.0, 1)
    pygame.mixer.music.set_volume(0.3)
else:
    pygame.mixer.music.stop()


# Cria a tela e lista de sprites
monitor_size = [pygame.display.Info().current_w, pygame.display.Info().current_h]
size = width, height = 832, 832
tela = pygame.display.set_mode(size)
pygame.display.set_caption("A DIRETORIA")
lista_sprites = pygame.sprite.Group()

#Criação do Mapa
matriz_mapa = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
       ]

mapaTeste = Mapa(copy.deepcopy(matriz_mapa))

# Criação do player
player = Player(matriz_mapa, (3,1))
lista_sprites.add(player)

click = False

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
    while game:
        #Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

            # if event.type == pygame.VIDEORESIZE:
            #     if not fullscreen:
            #         tela = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
        
            # if  event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_f:
            #         fullscreen = not fullscreen
            #         if fullscreen:
            #             tela = pygame.display.set_mode(monitor_size, pygame.FULLSCREEN)
            #         else:
            #             tela = pygame.display.set_mode((size), pygame.RESIZABLE)

        player.update()

        #Renderização
        tela.fill(preto)
        tela.blits(mapaTeste.quadrados)
        fonte.render_to(tela, [0, 0], str(player.movimento()), branco)

        lista_sprites.draw(tela)

        pygame.display.update()
        clock.tick(30)