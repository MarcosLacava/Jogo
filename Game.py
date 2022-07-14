import os
from pickletools import pyinteger_or_bool
from Player import Player
import sys, pygame, pygame.freetype
from Mapa import Mapa
import copy
import Button
import json
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




# Cria a tela e lista de sprites
monitor_size = [pygame.display.Info().current_w, pygame.display.Info().current_h]
size = width, height = 832, 832
tela = pygame.display.set_mode(size)
pygame.display.set_caption("A DIRETORIA")
lista_sprites = pygame.sprite.Group()


# Criação do Mapa


interagiveis = {(5, 0) : Porta.Porta(cords=(5, 0), destino="SALA2", tile_num=9),
                (5, 12) : Porta.Porta(cords=(5, 12), destino="SALA3", tile_num=9)}

salas = {"MAIN":True,
         "SALA1":False,
         "SALA2":False,
         "SALA3":False,
         "SALA4":False,
         "SALA5":False,
         "SALA6":False,
         "SALA7":False,
         }

with open(os.path.join("Mapas.json")) as m:
    mapas = json.load(m) # Carrega os mapas no .json

mapaAtual = Mapa(copy.deepcopy(mapas["MAIN"]["matriz"]) , mapas["MAIN"]["spritesheet"], interagiveis)

# Criação do player
player = Player((8,6))
player.set_mapa(mapaAtual.gerar_colisoes(), interagiveis)
lista_sprites.add(player)


def trocar_sala(nova):
    for i in salas.keys():
        salas[i] = False
    salas[nova] = True
    global mapaAtual
    mapaAtual = Mapa(copy.deepcopy(mapas[nova]["matriz"]) , mapas[nova]["spritesheet"], interagiveis)
    print(salas)

def renderização():
    # Faz todas as renderizações necessárias
    tela.fill(preto)
    tela.blits(mapaAtual.quadrados)
    fonte.render_to(tela, [0, 0], str(player.movimento()), branco)

    lista_sprites.draw(tela)
    
    pygame.display.update()
    clock.tick(30)
  
def event_loop():
    # Lida com eventos (Botões, Fechamento)
    for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if event.key == pygame.K_e and not player.interagindo:
                        cords = player.proximo()
                        if mapaAtual.matriz_mapa[cords[0]][cords[1]] == 9: # Porta
                            trocar_sala(interagiveis[cords].destino)


# Seção da música
main_menu_theme = os.path.join('Music','alexander-nakarada-space-ambience.ogg')

def music(state, name):
    if state:
        pygame.mixer.music.load(name)
        pygame.mixer.music.play(0, 0, 1000)
        pygame.mixer.music.set_volume(0.5)
    else:
        pygame.mixer.music.fadeout(1000)

music(main_menu, main_menu_theme)


def text_box(surface, text):
        
        # Fonte do text box
        text_box_font = pygame.font.Font((os.path.join("Fonts", "yoster-island.regular.ttf")), 24)

        # Caixa do texto.
        box_rect = pygame.Rect(10, 614, 812, 208)
        box_surf = pygame.draw.rect(surface, (1,1,1,0.5), box_rect)
        box_stroke = pygame.draw.rect(surface, (255,255,255), box_rect, 5)

        # Conteúdo da caixa de texto.
        text_content = text_box_font.render(text, False, (255,255,255))
        text_content_rect = text_content.get_rect(topleft = (30, 634))
        surface.blit(text_content, text_content_rect)

        return box_surf, box_stroke


# Settings (Temporário)
play_button = Button.Button("play_button", (416,416))
quit_button = Button.Button("quit_button", (416,516))

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


        # Condição para o botão de play ser acessado:
        if play_button.blit_button(tela) and click:
            main_menu = False
            music(main_menu, main_menu_theme)
            game = True
            break

        # Condição para o botão de quit ser acessado:
        if quit_button.blit_button(tela) and click:
            pygame.quit()
            sys.exit()
                    
        pygame.display.update()
        clock.tick(30)

    # Game Loop
    while salas['MAIN']:
        renderização()
        event_loop()
        player.update()

    while salas["SALA1"]:
        
        event_loop()
        player.update()
        renderização()

    while salas["SALA2"]:

        event_loop()
        player.update()
        renderização()

    while salas["SALA3"]:  

        event_loop()
        player.update()
        renderização()

    while salas["SALA4"]:

        event_loop()
        player.update()
        renderização()

    while salas["SALA5"]:

        event_loop()
        player.update()
        renderização()

    while salas["SALA6"]:

        event_loop()
        player.update()
        renderização()

    while salas["SALA7"]:

        event_loop()
        player.update()
        renderização()
            
