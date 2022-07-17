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
import Scroll
import json

from Scroll import Scroll

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
dialogo = None # Todos
estatuas = [] # 2
solucao = [False]*3 # 2
atirando = False # 3
flor_coletada = False # 6

open_scroll = False # Puzzle 07


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


def trocar_sala(nova, posicao=player.pos):
    # Troca o estado do jogo (salas/menus)
    for i in salas.keys():
        salas[i] = False
    salas[nova] = True
    primeiro_loop[nova] = True
    global dialogos
    dialogos = []
    sprites_mapa.empty()
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
            if not puzzles[1]:
                for i, e in enumerate(interagiveis["estatuas"].values()):
                    sprite = mapaAtual.get_sprite(e["tile_num"])

                    mapaAtual.trocar_tile(e["pos"], e["tile_num"], trocar_sprite=False)
                    mapaAtual.trocar_colisao(e["pos"], colisao=True)
                    
                    estatuas.append(Estatua(e["pos"], e["tipo"], sprite))
                    sprites_mapa.add(estatuas[i])

            else:   
                for e in estatuas:
                    sprites_mapa.add(e)

            for c in interagiveis["colisoes"]: # Adiciona as colisões
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
                                player.set_carregando(-1)
                            elif 26 <= tile <= 34 and not solucao[0]: # Deserto
                                if player.carregando == 0:
                                    solucao[0] = 2
                                else:
                                    solucao[0] = 1
                                cords_central = (10, 2)
                                estatuas[player.carregando].descarregar(cords_central)
                                mapaAtual.trocar_tile(cords_central, player.carregando + 23, trocar_sprite=False)
                                mapaAtual.trocar_colisao(cords_central, colisao=True)
                                player.set_carregando(-1)
                                
                                soma = 0
                                for i in solucao:
                                    soma += i
                                if soma == 6:
                                    puzzles[1] = True
                                    
                            elif 44 <= tile <= 52 and not solucao[1]: # Castelo
                                if player.carregando == 1:
                                    solucao[1] = 2
                                else:
                                    solucao[1] = 1
                                cords_central = (10, 6)
                                estatuas[player.carregando].descarregar(cords_central)
                                mapaAtual.trocar_tile(cords_central, player.carregando + 23, trocar_sprite=False)
                                mapaAtual.trocar_colisao(cords_central, colisao=True)
                                player.set_carregando(-1)

                                soma = 0
                                for i in solucao:
                                    soma += i
                                if soma == 6:
                                    puzzles[1] = True
                            elif 53 <= tile <= 61 and not solucao[2]: # Vulcão
                                if player.carregando == 2:
                                    solucao[2] = 2
                                else:
                                    solucao[2] = 1
                                cords_central = (10, 10)
                                estatuas[player.carregando].descarregar(cords_central)
                                mapaAtual.trocar_tile(cords_central, player.carregando + 23, trocar_sprite=False)
                                mapaAtual.trocar_colisao(cords_central, colisao=True)
                                player.set_carregando(-1)

                                soma = 0
                                for i in solucao:
                                    soma += i
                                if soma == 6:
                                    puzzles[1] = True

                        elif 23 <= tile <= 25: # Estátua de Dragão
                                # Levantar a estátua
                                player.set_carregando(tile-23)
                                estatuas[player.carregando].carregar(player.rect)
                                sprites_mapa.remove(estatuas[player.carregando])
                                sprites_mapa.add(estatuas[player.carregando])
                                mapaAtual.trocar_tile(cords, 0, trocar_sprite=False)
                                mapaAtual.trocar_colisao(cords, colisao=False)
                        elif 35 <= tile <= 43: # Dialogável
                            dialogo = Dialogo.Dialogo(["Leva cada dragao a seu lar"])
                            player.interagindo = True

                        elif tile == 2: # Porta
                            # Converte as coordenadas para o formato da key
                            cords_string = str(cords[0]) + " " + str(cords[1]) 
                            destino = interagiveis[cords_string]["destino"]

                            if not puzzles[1]:
                                # Reinicia o puzzle ao sair da sala com ele não solucionado
                                for i, e in enumerate(estatuas):
                                    e = None
                                    del e
                                    solucao[i] = 0
                                estatuas = []
                                    
                            trocar_sala(destino, interagiveis[cords_string]["inicio"])
                            break
                    elif event.key == pygame.K_e and player.interagindo:
                        if not dialogo.passar_linha():
                            dialogo = None
                            player.interagindo = False
                    
        player.update()
        renderização(False)
        sprites_mapa.update()
        sprites_mapa.draw(tela)

        if dialogo != None:
            dialogo.draw(tela)

        pygame.display.update()
        tempo += clock.tick(30)

    while salas["SALA3"]:  
        if primeiro_loop["SALA3"]:
            primeiro_loop["SALA3"] = False
        renderização(False)
        for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e and not player.interagindo and not player.andando:
                        cords = player.proximo()
                        tile = mapaAtual.matriz_mapa[cords[0]][cords[1]]

                        if 16 <= tile <= 17: # Pedestal
                            if not flor.coletada:
                                if flor.idade == 10:                          
                                    flor.coletar()
                                    flor_coletada = True
                                    mapaAtual.trocar_tile(interagiveis["Flor"]["pos"], 28)
                                    puzzles[5] = True # Puzzle 6 resolvido
                                else:
                                    flor.coletar()
                                    flor_coletada = True
                                    mapaAtual.trocar_tile(interagiveis["Flor"]["pos"], 28)
                        
                        elif tile == 15:
                            player.interagindo = True


                        elif tile == 12: # Porta
                            # Converte as coordenadas para o formato da key
                            cords_string = str(cords[0]) + " " + str(cords[1]) 
                            destino = interagiveis[cords_string]["destino"]    

                            trocar_sala(destino, interagiveis[cords_string]["inicio"])

        # Variáveis
    
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
            flor = Flor.Flor(tempo, flor_coletada)
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

                        if 12 <= tile <= 28: # Flor
                            if not flor.coletada:
                                if flor.idade == 10:                          
                                    flor.coletar()
                                    flor_coletada = True
                                    mapaAtual.trocar_tile(interagiveis["Flor"]["pos"], 28)
                                    puzzles[5] = True # Puzzle 6 resolvido
                                else:
                                    flor.coletar()
                                    flor_coletada = True
                                    mapaAtual.trocar_tile(interagiveis["Flor"]["pos"], 28)

                        elif tile == 12: # Porta
                            # Converte as coordenadas para o formato da key
                            cords_string = str(cords[0]) + " " + str(cords[1]) 
                            destino = interagiveis[cords_string]["destino"]    

                            trocar_sala(destino, interagiveis[cords_string]["inicio"])

    while salas["SALA7"]:

        if primeiro_loop["SALA7"]:
            scroll = Scroll(tela)
            primeiro_loop["SALA7"] = False

        
        renderização(False)

        if open_scroll:
            # tela.fill(branco)
            scroll.open_scroll(tela)
            player.interagindo = True

            mx, my = pygame.mouse.get_pos()

            scroll.write_scroll((mx,my), click)
            click = False

            scroll.check_scroll()

        player.update()

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

                        if tile == 18:
                            open_scroll = True
                                                            

                        elif tile == 11: # Porta
                            # Converte as coordenadas para o formato da key
                            cords_string = str(cords[0]) + " " + str(cords[1]) 
                            destino = interagiveis[cords_string]["destino"]    

                            trocar_sala(destino, interagiveis[cords_string]["inicio"])

                    elif (event.key == pygame.K_ESCAPE or event.key == pygame.K_e) and player.interagindo:
                        open_scroll = False
                        player.interagindo = False
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True