from audioop import cross
from operator import truediv
import os
from pickletools import pyinteger_or_bool
from turtle import pos
from xmlrpc.client import FastParser
from Player import Player
import sys, pygame, pygame.freetype
from Estatua import Estatua
import Dialogo
from Mapa import Mapa
import copy
import Button
import Flor
import Gun
import json

pygame.init()

# Estados do jogo:
main_menu = True
pause_menu = False
game = False

# Cores
preto = 1, 1, 1
branco = 255, 255, 255

# Game Clock
tempo = 0
clock = pygame.time.Clock()

# Fontes
title_font = pygame.freetype.SysFont(pygame.freetype.get_default_font(), 64)
fonte = pygame.freetype.SysFont(pygame.freetype.get_default_font(), 24)

# Estados do jogo
salas = {"MAIN":True,
         "SALA1":False,
         "SALA2":False,
         "SALA3":False,
         "SALA4":False,
         "SALA5":False,
         "SALA6":False,
         "SALA7":False,
         }
primeiro_loop = copy.deepcopy(salas)
puzzles = [False]*7

# Lógica dos puzzles
dialogos = [] # Todos
estatuas = [] # 2

# Cria a tela
monitor_size = [pygame.display.Info().current_w, pygame.display.Info().current_h]
size = width, height = 832, 832
tela = pygame.display.set_mode(size)
pygame.display.set_caption("A DIRETORIA")

# Criação do Mapa
with open(os.path.join("Mapas.json")) as m:
    mapas = json.load(m) # Carrega os mapas no .json

interagiveis = mapas["MAIN"]["interagiveis"]
mapaAtual = Mapa(copy.deepcopy(mapas["MAIN"]["matriz"]) , mapas["MAIN"]["spritesheet"], interagiveis)

# Criação do player
player = Player((8,6))
player.set_mapa(mapaAtual.gerar_colisoes())

# Sprites
sprites_player = pygame.sprite.Group()
sprites_player.add(player)
sprites_mapa = pygame.sprite.Group()


def trocar_sala(nova, posicao=(0,0)):
    # Troca o estado do jogo (salas/menus)
    for i in salas.keys():
        salas[i] = False
    salas[nova] = True
    primeiro_loop[nova] = True
    dialogos = []

    fade = pygame.Surface(size) # Objeto do fade
    fade.fill(preto)

    for i in range(255): # Fade out
        fade.set_alpha(i)
        renderização(update=False)
        tela.blit(fade, (0,0))
        pygame.display.update()
        clock.tick(255)

    global mapaAtual
    global interagiveis
    interagiveis = mapas[nova]["interagiveis"]
    mapaAtual = Mapa(copy.deepcopy(mapas[nova]["matriz"]) , mapas[nova]["spritesheet"], interagiveis)
    player.set_mapa(mapaAtual.gerar_colisoes())
    player.set_pos(posicao)

    for i in range(255, 0, -1): # Fade in
        fade.set_alpha(i)
        renderização(update=False)
        tela.blit(fade, (0,0))
        pygame.display.update()
        clock.tick(255)

def renderização(update=True):
    # Faz todas as renderizações necessárias
    tela.fill(preto)
    tela.blits(mapaAtual.quadrados)

    sprites_player.draw(tela)
    if update:
        pygame.display.update()
        global tempo
        tempo += clock.tick(30)
  
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
                    # Converte as coordenadas para o formato da key
                    cords_string = str(cords[0]) + " " + str(cords[1]) 
                    destino = interagiveis[cords_string]["destino"]    
                    trocar_sala(destino, interagiveis[cords_string]["inicio"])

                if salas["SALA3"]:
                    if mapaAtual.matriz_mapa[cords[0]][cords[1]] == 15:
                        # Coloca a imagem da mira da arma na 
                        global mira
                        mira = True

                if salas["SALA6"]:
                    if 12 <= mapaAtual.matriz_mapa[cords[0]][cords[1]] <= 28: # Flor
                        if flor.idade == 10 and not flor.coletada:                          
                            flor.coletar()
                            mapaAtual.trocar_tile(interagiveis["Flor"]["pos"], 28)
                            puzzles[6] = True # Puzzle 6 resolvido

                        

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


        # Imagem de fundo do menu
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
        renderização(False)
        fonte.render_to(tela, [0, 0], str(player.movimento()), branco)
        fonte.render_to(tela, [0, 32], str(tempo), branco)
        pygame.display.update()
        tempo += clock.tick(30)

        event_loop()
        player.update()

    while salas["SALA1"]:
        
        event_loop()
        player.update()
        renderização()

    while salas["SALA2"]:
        
        if primeiro_loop["SALA2"]: 
            # Cria os objetos no primeiro loop do estado
            for i, e in enumerate(interagiveis["estatuas"].values()):
                sprite = mapaAtual.get_sprite(e["tile_num"])

                mapaAtual.trocar_tile(e["pos"], e["tile_num"], trocar_sprite=False)
                mapaAtual.trocar_colisao(e["pos"], colisao=True)
                
                estatuas.append(Estatua(e["pos"], e["tipo"], sprite))
                sprites_mapa.add(estatuas[i])

            for c in interagiveis["colisoes"]:
                mapaAtual.trocar_colisao(c, colisao=True)

            primeiro_loop["SALA2"] = False
            
        for event in pygame.event.get(): # Event Loop
                if event.type == pygame.QUIT: 
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e and not player.interagindo and not player.andando:
                        cords = player.proximo()
                        tile = mapaAtual.matriz_mapa[cords[0]][cords[1]]

                        if player.carregando >= 0:
                            if tile == 0:       
                                # Depositar estátua no chão
                                estatuas[player.carregando].descarregar(cords)
                                mapaAtual.trocar_tile(cords, player.carregando + 23, trocar_sprite=False)
                                mapaAtual.trocar_colisao(cords, colisao=True)
                                player.carregando = -1
                        elif 23 <= tile <= 25: # Estátua de Dragão
                                # Levantar a estátua
                                player.carregando = tile-23
                                estatuas[player.carregando].carregar(player.rect)
                                sprites_mapa.remove(estatuas[player.carregando])
                                sprites_mapa.add(estatuas[player.carregando])
                                mapaAtual.trocar_tile(cords, 0, trocar_sprite=False)
                                mapaAtual.trocar_colisao(cords, colisao=False)
                        elif 35 <= tile <= 44: # Dialogável
                            Dialogo.Dialogo("Leva cada dragão a seu lar", tela)

                        elif tile == 2: # Porta
                            # Converte as coordenadas para o formato da key
                            cords_string = str(cords[0]) + " " + str(cords[1]) 
                            destino = interagiveis[cords_string]["destino"]    

                            trocar_sala(destino, interagiveis[cords_string]["inicio"])
                    
        player.update()
        renderização(False)
        sprites_mapa.update()
        sprites_mapa.draw(tela)

        pygame.display.update()
        tempo += clock.tick(30)

    while salas["SALA3"]:  
        
        renderização(False)
        event_loop()

        # Variáveis
        gun = Gun.Gun()
    
        player.update()

        pygame.display.update()
        tempo += clock.tick(30)
    

    while salas["SALA4"]:

        event_loop()
        player.update()
        renderização()

    while salas["SALA5"]:

        event_loop()
        player.update()
        renderização()

    while salas["SALA6"]:
        if primeiro_loop["SALA6"]:
            flor = Flor.Flor(tempo, puzzles[6])
            primeiro_loop["SALA6"] = False

        player.update()
        renderização(False)

        nova_tile = flor.update(tempo)

        if nova_tile > 0:
            mapaAtual.trocar_tile(interagiveis["Flor"]["pos"], nova_tile)
        
        fonte.render_to(tela, [0, 0], str(tempo), branco)

        pygame.display.update()
        tempo += clock.tick(30)

        for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e and not player.interagindo and not player.andando:
                        cords = player.proximo()
                        tile = mapaAtual.matriz_mapa[cords[0]][cords[1]]

                        if player.carregando:
                            if tile == 0:
                                mapaAtual.trocar_tile(cords, player.carregando)
                                player.carregando = 0
                        elif 23 <= tile <= 25: # Estátua de Dragão
                                mapaAtual.trocar_tile(cords, 0, remover_colisao=True)
                                player.carregando = tile

                        elif tile == 2: # Porta
                            # Converte as coordenadas para o formato da key
                            cords_string = str(cords[0]) + " " + str(cords[1]) 
                            destino = interagiveis[cords_string]["destino"]    

                            trocar_sala(destino, interagiveis[cords_string]["inicio"])
    while salas["SALA7"]:
        event_loop()
        player.update()
        renderização()
            
