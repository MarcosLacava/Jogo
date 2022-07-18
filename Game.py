import sys, os, pygame, pygame.freetype
from tkinter import dialog
import copy, json
import Decoracao, Estatua, Flor, Scroll
import Button, Dialogo, Mapa, Player, Spritesheet

pygame.init()

# Cria a tela
monitor_size = [pygame.display.Info().current_w, pygame.display.Info().current_h]
size = width, height = 832, 832
tela = pygame.display.set_mode(size)
pygame.display.set_caption("A DIRETORIA")

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
salas = {"MAIN": False,
         "SALA1":False,
         "SALA2":False,
         "SALA3":False,
         "SALA4":False,
         "SALA5":False,
         "SALA6":False,
         "SALA7":False,
         "END"  :False,
         "MENU" :True,
         }
primeiro_loop = copy.deepcopy(salas)

puzzles = [True, False, False, False, True, False, False] # Guarda se um puzzle está completo ou não
                                                          # Os não implementados começam como true

# Lógica dos puzzles
dialogo = None # Todos
estatuas = [] # 2
solucao = [False]*3 # 2
atirando = False # 3
spritesheet_retratos = Spritesheet.Spritesheet("retratos") # 3
ordem_correta_salas = ["SALA6", "SALA2", "SALA3", "SALA7"] # 4
ordem_atual_salas = [] # 4
ordem_completa = False
flor_coletada = False # 6
open_scroll = False # 7

# Lógica dos botões
frames_reset = 30 # Frames que deve segurar o botão para reiniciar o puzzle
frames_reset_atual = 0 # Frames segurados 

# Criação do Mapa
with open(os.path.join("Mapas.json")) as m:
    mapas = json.load(m) # Carrega os mapas no .json

interagiveis = mapas["MAIN"]["interagiveis"]
mapaAtual = Mapa.Mapa(copy.deepcopy(mapas["MAIN"]["matriz"]) , mapas["MAIN"]["spritesheet"], interagiveis)
tileLen = 64

# Criação do player
posicao_inicial = (6,6)
player = Player.Player(posicao_inicial)
player.set_mapa(mapaAtual.gerar_colisoes())

# Sprites
sprites_player = pygame.sprite.Group()
sprites_player.add(player)
sprites_mapa = pygame.sprite.Group()
crosshair_sprite = pygame.image.load(os.path.join("Sprites", "crosshair", "sprite_crosshair.png"))
alvo_sprite = pygame.image.load(os.path.join("Sprites", "crosshair", "sprite_alvo.png"))


def trocar_sala(nova, posicao_player=False, fade_in=True, fade_out=True):
    # Troca o estado do jogo (salas/menus)
    som(door_sound)

    global mapaAtual
    global posicao_inicial
    global interagiveis
    global dialogo


    for i in salas.keys():
        salas[i] = False
    salas[nova] = True
    primeiro_loop[nova] = True
    sprites_mapa.empty()
    fade = pygame.Surface(size) # Objeto do fade
    fade.fill(preto)

    if fade_out:
        for i in range(255): # Fade out
            fade.set_alpha(i)
            tela.fill(preto)
            tela.blits(mapaAtual.quadrados)

            sprites_player.draw(tela)
            tela.blit(fade, (0,0))
            pygame.display.update()
            clock.tick(255)

    dialogo = None
    posicao_inicial = mapas[nova]["posicao_inicial"]
    interagiveis = mapas[nova]["interagiveis"]
    mapaAtual = Mapa.Mapa(copy.deepcopy(mapas[nova]["matriz"]) , mapas[nova]["spritesheet"], interagiveis)
    player.set_mapa(mapaAtual.gerar_colisoes())
    if posicao_player:
        player.set_pos(posicao_player)
    else:
        player.set_pos(posicao_inicial)

    if fade_in:
        for i in range(255, 0, -1): # Fade in
            fade.set_alpha(i)
            tela.fill(preto)
            tela.blits(mapaAtual.quadrados)
            sprites_player.draw(tela)
            tela.blit(fade, (0,0))
            pygame.display.update()
            clock.tick(255)              

# Seção da música
main_menu_theme = os.path.join('Music','alexander-nakarada-space-ambience.ogg')

def music(state, name):
    if state:
        pygame.mixer.music.load(name)
        pygame.mixer.music.play(0, 0, 1000)
        pygame.mixer.music.set_volume(0.5)
    else:
        pygame.mixer.music.fadeout(1000)

music(salas["MENU"], main_menu_theme)

# Efeitos sonoros
door_sound = os.path.join("Sounds","door.ogg")
dragon_sound = os.path.join("Sounds","dragon.ogg")
flower_sound = os.path.join("Sounds","flower.ogg")
gun_sound = os.path.join("Sounds","gun.ogg")
sword_sound = os.path.join("Sounds","sword.ogg")
angel_sound = os.path.join("Sounds","angel.ogg")

def som(name):
    pygame.mixer.Sound(name).play()


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

def image_box(sprite):
    # Desenha uma sprite com bordas no meio da tela
    rect = sprite.get_rect(center=(416,416))
    borda = rect.copy().inflate(10, 10)
    pygame.draw.rect(tela, preto, borda)
    tela.blit(sprite, rect)

# Settings (Temporário)
play_button = Button.Button("play_button", (416,416))
quit_button = Button.Button("quit_button", (416,516))

# Main Loop
while True:
    # Menu Loop
    while salas["MENU"]:
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
            trocar_sala("MAIN",fade_out=False)
            music(salas["MENU"], main_menu_theme)
            break

        # Condição para o botão de quit ser acessado:
        if quit_button.blit_button(tela) and click:
            pygame.quit()
            sys.exit()
                    
        pygame.display.update()
        clock.tick(30)

    # Game Loop 
    while salas["END"]:
        # Fim do jogo
        pygame.quit()
        sys.exit()

    while salas['MAIN']:
        if primeiro_loop["MAIN"]:
            mesa = Decoracao.Decoracao(mapaAtual.get_sprite(interagiveis["Mesa"]["tile_num"]))
            sprites_mapa.add(mesa)

            cY, cX = interagiveis["Mesa"]["pos"]
            mesa.rect.topleft = cY*tileLen, cX*tileLen
            for x in range(3):
                    # Cria colisão para cada uma das 3 tiles da mesa
                    cords = cY, cX+x
                    mapaAtual.trocar_tile(cords, interagiveis["Mesa"]["tile_num"])
                    mapaAtual.trocar_colisao(cords, colisao=True)

            primeiro_loop["MAIN"] = False      

        tela.fill(preto)
        tela.blits(mapaAtual.quadrados)

        sprites_mapa.draw(tela)
        sprites_player.draw(tela)
        fonte.render_to(tela, [0, 0], str(player.movimento()), branco)
        fonte.render_to(tela, [0, 32], str(tempo), branco)

        if dialogo != None:
            dialogo.draw(tela)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_e and not player.interagindo and not player.andando:
                    cords = player.proximo()
                    tile = mapaAtual.matriz_mapa[cords[0]][cords[1]]

                    if tile == 20:
                        end = True
                        for p in puzzles: # Verifica se o jogo foi completado
                            if not p:
                                end = False
                        if end:
                            trocar_sala("END", fade_in=False)
                        else:
                            player.interagindo = True
                            lista_dialogo = ["Va em cada sala e resolva seus desafios", "So assim você sera liberado"]
                            dialogo = Dialogo.Dialogo(lista_dialogo)
                        
                    elif 12 <= tile <= 18: # Porta
                        # Converte as coordenadas para o formato da key
                        cords_string = str(cords[0]) + " " + str(cords[1]) 
                        destino = interagiveis[cords_string]["destino"]    

                        if destino != "SALA4":
                            ordem_atual_salas.append(destino) # Adiciona a nova sala à lista de salas entradas
                        if ordem_atual_salas == ordem_correta_salas:
                            # Completa o puzzle 4
                            ordem_completa = True

                        trocar_sala(destino)
                        

                elif event.key == pygame.K_e and player.interagindo:
                        if not dialogo.passar_linha():
                            dialogo = None
                            player.interagindo = False
        player.update()

        pygame.display.update()
        tempo += clock.tick(30)

    while salas["SALA2"]:
        
        if primeiro_loop["SALA2"]: 
            # Cria os objetos no primeiro loop do estado
            if not puzzles[1]:
                for y, e in enumerate(interagiveis["estatuas"].values()):
                    # Cria as estátuas
                    sprite = mapaAtual.get_sprite(e["tile_num"])
                    
                    # Troca as tiles no mapa (Visível e colisão)
                    mapaAtual.trocar_tile(e["pos"], e["tile_num"], trocar_sprite=False)
                    mapaAtual.trocar_colisao(e["pos"], colisao=True)
                    
                    estatuas.append(Estatua.Estatua(e["pos"], e["tipo"], sprite))
                    estatuas[y].set_pos(e["pos"])
                    sprites_mapa.add(estatuas[y])

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
                                for y in solucao:
                                    soma += y
                                if soma == 6:
                                    som(dragon_sound)
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
                                for y in solucao:
                                    soma += y
                                if soma == 6:
                                    som(dragon_sound)
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
                                for y in solucao:
                                    soma += y
                                if soma == 6:
                                    puzzles[1] = True

                        elif 23 <= tile <= 25: # Estátua de Dragão
                                # Levantar a estátua
                                player.set_carregando(tile - 23)
                                estatuas[player.carregando].carregar(player.rect)
                                sprites_mapa.remove(estatuas[player.carregando])
                                sprites_mapa.add(estatuas[player.carregando])
                                mapaAtual.trocar_tile(cords, 0, trocar_sprite=False)
                                mapaAtual.trocar_colisao(cords, colisao=False)
                        elif 35 <= tile <= 43: # Dialogável
                            if puzzles[1]:
                                # Diálogo do puzzle completo
                                lista_dialogo = ["Cada dragao em seu lar"]
                            else:
                                # Dialogo do puzzle a ser feito
                                lista_dialogo = ["Ha tres dragoes, um de cada lugar", 
                                "Os do deserto sempre falam a verdade",
                                "Os que residem no vulcao sao mentirosos",
                                "Os dragoes do castelo tanto mentem quanto falam verdades",
                                "O vermelho diz: O verde é do castelo",
                                "O azul diz: o vermelho é do deserto",
                                "O verde diz: eu sou do castelo",
                                "Leve cada dragao a seu lar"]
                            dialogo = Dialogo.Dialogo(lista_dialogo)
                            player.interagindo = True

                        elif tile == 2: # Porta
                            # Converte as coordenadas para o formato da key
                            cords_string = str(cords[0]) + " " + str(cords[1]) 
                            destino = interagiveis[cords_string]["destino"]

                            if not puzzles[1]:
                                # Reinicia o puzzle ao sair da sala com ele não solucionado
                                for y, e in enumerate(estatuas):
                                    e = None
                                    del e
                                    solucao[y] = 0
                                estatuas = []
                                    
                            trocar_sala(destino, interagiveis[cords_string]["inicio"])
                            break
                    elif event.key == pygame.K_e and player.interagindo:
                        if not dialogo.passar_linha():
                            dialogo = None
                            player.interagindo = False
                    
        player.update()
        tela.fill(preto)
        tela.blits(mapaAtual.quadrados)

        sprites_player.draw(tela)
        sprites_mapa.update()
        sprites_mapa.draw(tela)

        if dialogo != None:
            dialogo.draw(tela)

        if not puzzles[1] and pygame.key.get_pressed()[pygame.K_f]:
            # Botao de reset do puzzle
            frames_reset_atual += 1

            progresso = pygame.Rect(100,700,21*frames_reset_atual, 30)
            pygame.draw.rect(tela, preto, progresso)

            if frames_reset_atual >= frames_reset:
                frames_reset_atual = 0
                
                fade = pygame.Surface(size) # Objeto do fade
                fade.fill(preto)

                player.set_pos(posicao_inicial) # Teleporta o player para o começo da sala
                player.set_carregando(-1)
                player.interagindo = False
                primeiro_loop["SALA2"] = True
                dialogo = None

                # Reinicia as variáveis do puzzle
                for y in range(3):
                    sprites_mapa.remove(estatuas[0])
                    del estatuas[0]
                estatuas = []
                solucao.clear()
                solucao = [0]*3

                mapaAtual = Mapa.Mapa(copy.deepcopy(mapas["SALA2"]["matriz"]) , mapas["SALA2"]["spritesheet"], interagiveis)
                player.set_mapa(mapaAtual.gerar_colisoes())
                
                for y in range(255, 0, -1): # Fade in
                    fade.set_alpha(y)
                    tela.fill(preto)
                    tela.blits(mapaAtual.quadrados)

                    sprites_player.draw(tela)
                    tela.blit(fade, (0,0))
                    pygame.display.update()
                    clock.tick(300)
        else:
            frames_reset_atual = 0

        pygame.display.update()
        tempo += clock.tick(30)

    while salas["SALA3"]:  
        if primeiro_loop["SALA3"]:
            sprite = None # Sprite a ser desenha na tela (retrato)
            retrato = False # Controla quando deve desenha o retrato na tela 
            atirando = False # Controla quando o player está no modo atirar
            crosshair_rect = crosshair_sprite.get_rect() # Rect do crosshair
            rect_pedestais = [] # Guarda os rects dos pedestais para colidir com o cursor do mouse
            indicadores = [] # Lista de indicadores de tiro

            ordem_correta = [0,3,1,5,4,2,6]
            ordem_feita = [] # Ordem dos alvos marcados pelo player

            for p in interagiveis["pedestais"].keys():
                # Cria cada pedestal (retratos)
                x, y = p.split()
                x, y = int(x), int(y)
                mapaAtual.trocar_colisao((x, y), colisao=True)

                if puzzles[2]:
                    # Troca os pedestais por cactos caso o puzzle tenha sido completado antes
                    mapaAtual.trocar_tile((x, y), 20) 
                else:
                    mapaAtual.trocar_tile((x, y), interagiveis["pedestais"][p]["tile_num"])

                x, y = x * tileLen, y * tileLen
                w, h = tileLen, tileLen
                r = pygame.Rect(y, x, w, h)
                rect_pedestais.append(r)
            rect_pedestais.append(player.rect) # Adiciona o rect do player à lista, pois ele também age como pedestal

            primeiro_loop["SALA3"] = False

        mx, my = pygame.mouse.get_pos()
        tela.fill(preto)
        tela.blits(mapaAtual.quadrados)

        sprites_player.draw(tela)

        for event in pygame.event.get(): # Event loop
                if event.type == pygame.QUIT: 
                    pygame.quit()
                    sys.exit()
                if atirando and event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1: # Marcar alvo
                        som(gun_sound)
                        t = -1
                        for y, x in enumerate(rect_pedestais):
                            # Verifica se o mouse está em cima de um pedestal
                            if x.collidepoint(mx, my): 
                                t = y
                                break

                        if t >= 0 and t not in ordem_feita:
                            # Caso marque um alvo válido novo, marca e cria a sprite do alvo sobre o pedestal
                            p = rect_pedestais[t]
                            r = pygame.Rect(p.x, p.y, crosshair_rect.w, crosshair_rect.h)
                            r.center = p.center
                            indicadores.append((alvo_sprite, r))
                            ordem_feita.append(t)

                        if ordem_feita == ordem_correta:
                            # Conclui o puzzle
                            player.interagindo = False
                            atirando = False
                            pygame.mouse.set_visible(True)
                            indicadores = []

                            puzzles[2] = True
                            for p in interagiveis["pedestais"].keys():
                                # Troca os pedestais por cactos
                                x, y = p.split()
                                x, y = int(x), int(y)
                                mapaAtual.trocar_tile((x, y), 20) 

                            fade = pygame.Surface(size) # Objeto do fade
                            fade.fill(preto)

                            for y in range(255, 0, -1): # Fade in
                                fade.set_alpha(y)
                                tela.fill(preto)
                                tela.blits(mapaAtual.quadrados)

                                sprites_player.draw(tela)
                                tela.blit(fade, (0,0))
                                pygame.display.update()
                                clock.tick(85)
                                

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e and not player.interagindo and not player.andando:
                        cords = player.proximo()
                        tile = mapaAtual.matriz_mapa[cords[0]][cords[1]]
                    
                        if 16 <= tile <= 17: # Pedestal
                                # Abre o retrato
                                cords_string = str(cords[0]) + " " + str(cords[1]) 
                                sprite = spritesheet_retratos.cortar_sprite("retratos_" + interagiveis["pedestais"][cords_string]["pedestal"] + ".png")
                                player.interagindo = True
                                retrato = True

                        elif tile == 15 and not puzzles[2]: # Arma
                            # Pega a arma
                            player.interagindo = True
                            atirando = True
                            pygame.mouse.set_visible(False)
                            
                        elif tile == 22: # Mesa do Texto
                            lista_dialogo = ["A começar pela Gula, nunca saciada,",
                             "que segue predando a terra escassa",
                             "Nao muito distante, no grande cofre de pedra,",
                             "Sobre a Avareza cunhou o seu projetil",
                             "A Luxuria o trai com um outro qualquer,",
                             "Ali desvendado, o terceiro disparo selou a sentença",
                             "Ao seu braco direito, fiel companheiro,",
                             "Nao esperava o que a Inveja faria,",
                             "o som do estampido findou parceria",
                             "O bom filho a casa retorna,",
                             "Atado por sangue, do laço com a Ira ele se desfez",
                             "E sobre esse mesmo teto, a Preguiça doente, ",
                             "para frente e para tras na cadeira balança",
                             "Finalmente caida a ultima memoria,",
                             "no fundo do inferno chegou o pecador",
                             "E apesar dos pesares, ",
                             "o vil Pistoleiro ainda carregava um tiro no tambor."

                            ]
                            dialogo = Dialogo.Dialogo(lista_dialogo)
                            player.interagindo = True

                        elif tile == 11: # Porta
                            # Converte as coordenadas para o formato da key
                            cords_string = str(cords[0]) + " " + str(cords[1]) 
                            destino = interagiveis[cords_string]["destino"]    

                            trocar_sala(destino, interagiveis[cords_string]["inicio"])
                    elif event.key == pygame.K_e and player.interagindo:
                        # Guarda a arma
                        if atirando:
                            player.interagindo = False
                            atirando = False
                            pygame.mouse.set_visible(True)
                        if retrato:
                        # Fecha o retrato
                            player.interagindo = False
                            retrato = False

                        if dialogo != None:
                            # Fecha o diálogo
                            if not dialogo.passar_linha():
                                dialogo = None
                                player.interagindo = False

        if atirando:
            # Lógica da arma (marcar alvos)
            crosshair_rect.center = (mx, my)
            tela.blit(crosshair_sprite, crosshair_rect)

        if indicadores != None:
            for y in indicadores:
                tela.blit(y[0], y[1])

        if retrato:
            # Desenha a imagem do retrato
            image_box(sprite)

        player.update()
        if dialogo != None:
            dialogo.draw(tela)

        if not puzzles[2] and pygame.key.get_pressed()[pygame.K_f]:
            # Botao de reset do puzzle
            frames_reset_atual += 1

            progresso = pygame.Rect(100,700,21*frames_reset_atual, 30)
            pygame.draw.rect(tela, preto, progresso)

            if frames_reset_atual >= frames_reset:
                frames_reset_atual = 0
                
                fade = pygame.Surface(size) # Objeto do fade
                fade.fill(preto)

                player.set_pos(posicao_inicial) # Teleporta o player para o começo da sala
                player.set_carregando(-1)
                player.interagindo = False
                primeiro_loop["SALA3"] = True
                dialogo = None
                
                # Reincia as varáveis do puzzle
                indicadores = []
                ordem_feita = []
                atirando = False
                
                for y in range(255, 0, -1): # Fade in
                    fade.set_alpha(y)
                    tela.fill(preto)
                    tela.blits(mapaAtual.quadrados)

                    sprites_player.draw(tela)
                    tela.blit(fade, (0,0))
                    pygame.display.update()
                    clock.tick(300)
        else:
            frames_reset_atual = 0

        pygame.display.update()
        tempo += clock.tick(30)
    
    while salas["SALA4"]:
        if primeiro_loop["SALA4"]:
            if ordem_completa:
                mapaAtual.trocar_tile([6,6], 13)
            primeiro_loop["SALA4"] = False
        
        player.update()
        tela.fill(preto)
        tela.blits(mapaAtual.quadrados)

        sprites_player.draw(tela)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_e and not player.interagindo:
                    cords = player.proximo()
                    tile = mapaAtual.matriz_mapa[cords[0]][cords[1]]
                    
                    if tile == 13: # Finalizar puzzle
                        som(angel_sound)
                        puzzles[3] = True
                        lista_dialogo = ["..."]

                        dialogo = Dialogo.Dialogo(lista_dialogo) # Cria o dialogo do anjo
                        player.interagindo = True

                    elif tile == 12: # Dialogável
                        lista_dialogo = ["A ordem do viajante importa", "Primeiro na floresta...", 
                                                   "Depois pela caverna...", "Passando pelo deserto...", "Chegando no castelo", 
                                                   "Para acabar na masmorra"]

                        dialogo = Dialogo.Dialogo(lista_dialogo) # Cria o dialogo do anjo
                        player.interagindo = True

                    elif tile == 11: # Porta
                        # Converte as coordenadas para o formato da key
                        cords_string = str(cords[0]) + " " + str(cords[1]) 
                        destino = interagiveis[cords_string]["destino"]    
                        trocar_sala(destino, interagiveis[cords_string]["inicio"])

                elif event.key == pygame.K_e and player.interagindo:
                        if not dialogo.passar_linha():
                            dialogo = None
                            player.interagindo = False
                
        
        if dialogo != None:
            dialogo.draw(tela)

        if not puzzles[3] and pygame.key.get_pressed()[pygame.K_f]:
            # Botao de reset do puzzle
            frames_reset_atual += 1

            progresso = pygame.Rect(100,700,21*frames_reset_atual, 30)
            pygame.draw.rect(tela, preto, progresso)

            if frames_reset_atual >= frames_reset:
                frames_reset_atual = 0
                
                fade = pygame.Surface(size) # Objeto do fade
                fade.fill(preto)

                player.set_pos(posicao_inicial) # Teleporta o player para o começo da sala
                player.set_carregando(-1)
                player.interagindo = False
                primeiro_loop["SALA3"] = True
                dialogo = None
                
                # Reincia as varáveis do puzzle
                ordem_atual_salas = []
                ordem_completa = False
                
                for y in range(255, 0, -1): # Fade in
                    fade.set_alpha(y)
                    tela.fill(preto)
                    tela.blits(mapaAtual.quadrados)

                    sprites_player.draw(tela)
                    tela.blit(fade, (0,0))
                    pygame.display.update()
                    clock.tick(300)
        else:
            frames_reset_atual = 0
                    
        pygame.display.update()
        tempo += clock.tick(30)

    while salas["SALA6"]:
        if primeiro_loop["SALA6"]:
            flor = Flor.Flor(tempo, flor_coletada) # Cria a flor
            primeiro_loop["SALA6"] = False

        player.update()
        tela.fill(preto)
        tela.blits(mapaAtual.quadrados)

        sprites_player.draw(tela)
        nova_tile = flor.update(tempo) # Adiciona o tempo á flor

        if nova_tile > 0:
            # Muda a tile a flor quando seu estágio é alterado
            mapaAtual.trocar_tile(interagiveis["Flor"]["pos"], nova_tile)

        if not puzzles[5] and pygame.key.get_pressed()[pygame.K_f]:
            # Botao de reset do puzzle
            frames_reset_atual += 1

            progresso = pygame.Rect(100,700,21*frames_reset_atual, 30)
            pygame.draw.rect(tela, preto, progresso)

            if frames_reset_atual >= frames_reset:
                frames_reset_atual = 0
                
                fade = pygame.Surface(size) # Objeto do fade
                fade.fill(preto)

                player.set_pos(posicao_inicial) # Teleporta o player para o começo da sala
                player.set_carregando(-1)
                player.interagindo = False
                primeiro_loop["SALA6"] = True
                dialogo = None
                
                # Reincia as varáveis do puzzle
                flor_coletada = False
                tempo = 0
                
                for y in range(255, 0, -1): # Fade in
                    fade.set_alpha(y)
                    tela.fill(preto)
                    tela.blits(mapaAtual.quadrados)

                    sprites_player.draw(tela)
                    tela.blit(fade, (0,0))
                    pygame.display.update()
                    clock.tick(300)
        else:
            frames_reset_atual = 0

        if dialogo != None:
            dialogo.draw(tela)

        pygame.display.update()
        tempo += clock.tick(30)

        for event in pygame.event.get(): # Event Loop
                if event.type == pygame.QUIT: 
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e and not player.interagindo and not player.andando:
                        cords = player.proximo()
                        tile = mapaAtual.matriz_mapa[cords[0]][cords[1]]
                        
                        if tile == 29: # Mesa
                            lista_dialogo = ["A paciencia e uma virtude..."]
                            dialogo = Dialogo.Dialogo(lista_dialogo)
                            player.interagindo = True

                        elif 12 <= tile <= 28: # Flor
                            if not flor.coletada:
                                som(flower_sound)
                                if flor.idade == 10:    
                                    # Caso colete no tempo certo (Completa o puzzle)     
                                    flor.coletar()
                                    flor_coletada = True
                                    mapaAtual.trocar_tile(interagiveis["Flor"]["pos"], 28)
                                    puzzles[5] = True # Puzzle 6 resolvido
                                else:
                                    # Caso colete no tempo errado (Falha o puzzle)
                                    flor.coletar()
                                    flor_coletada = True
                                    mapaAtual.trocar_tile(interagiveis["Flor"]["pos"], 28)

                        elif tile == 11: # Porta
                            # Converte as coordenadas para o formato da key
                            cords_string = str(cords[0]) + " " + str(cords[1]) 
                            destino = interagiveis[cords_string]["destino"]    

                            trocar_sala(destino, interagiveis[cords_string]["inicio"])
                    elif event.key == pygame.K_e and player.interagindo:
                        if not dialogo.passar_linha():
                            dialogo = None
                            player.interagindo = False

    while salas["SALA7"]:

        if primeiro_loop["SALA7"]:
            scroll = Scroll.Scroll(tela)
            if puzzles[6]:
                mapaAtual.trocar_tile(interagiveis["Mesa"]["pos"], 19)
                mapaAtual.trocar_tile(interagiveis["Espada"]["pos"], 21)

            primeiro_loop["SALA7"] = False

        tela.fill(preto)
        tela.blits(mapaAtual.quadrados)

        sprites_player.draw(tela)

        if open_scroll:
            # tela.fill(branco)
            scroll.open_scroll(tela)
            player.interagindo = True

            mx, my = pygame.mouse.get_pos()

            scroll.write_scroll((mx,my), click)
            click = False

            if scroll.check_scroll():
                mapaAtual.trocar_tile(interagiveis["Mesa"]["pos"], 19)

        player.update()

        if not puzzles[6] and pygame.key.get_pressed()[pygame.K_f]:
            # Botao de reset do puzzle
            frames_reset_atual += 1

            progresso = pygame.Rect(100,700,21*frames_reset_atual, 30)
            pygame.draw.rect(tela, preto, progresso)

            if frames_reset_atual >= frames_reset:
                frames_reset_atual = 0
                
                fade = pygame.Surface(size) # Objeto do fade
                fade.fill(preto)

                player.set_pos(posicao_inicial) # Teleporta o player para o começo da sala
                player.set_carregando(-1)
                player.interagindo = False
                primeiro_loop["SALA7"] = True
                dialogo = None
                
                # Reincia as varáveis do puzzle
                mapaAtual.trocar_tile(interagiveis["Mesa"]["pos"], 18)
                scroll = None
                open_scroll = False
                
                for y in range(255, 0, -1): # Fade in
                    fade.set_alpha(y)
                    tela.fill(preto)
                    tela.blits(mapaAtual.quadrados)

                    sprites_player.draw(tela)
                    tela.blit(fade, (0,0))
                    pygame.display.update()
                    clock.tick(300)
        else:
            frames_reset_atual = 0

        if dialogo != None:
            dialogo.draw(tela)

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

                        if tile == 18: # Abre o pergaminho
                            open_scroll = True
                                                            
                        if tile == 20: # Retira a espada do pedestal, se o puzzle foi concluido com sucesso
                            if scroll.check_scroll():
                                mapaAtual.trocar_tile(interagiveis["Espada"]["pos"], 21)
                                som(sword_sound)
                                puzzles[6] = True
                            else:
                                lista_dialogo = ["Este nao foi o juramento do cavaleiro"]
                                dialogo = Dialogo.Dialogo(lista_dialogo)
                                player.interagindo = True

                        if tile == 11: # Porta
                            # Converte as coordenadas para o formato da key
                            cords_string = str(cords[0]) + " " + str(cords[1]) 
                            destino = interagiveis[cords_string]["destino"]    

                            trocar_sala(destino, interagiveis[cords_string]["inicio"])

                    elif event.key == pygame.K_e and player.interagindo and dialogo != None:
                        if not dialogo.passar_linha():
                            dialogo = None
                            player.interagindo = False

                    elif (event.key == pygame.K_ESCAPE or event.key == pygame.K_e) and player.interagindo:
                        open_scroll = False
                        player.interagindo = False
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True