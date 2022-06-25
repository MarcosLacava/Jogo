from cmath import rect
from msilib import sequence
from Player import Player
import sys, pygame, pygame.freetype
from typing import Sequence

pygame.init()

#Fonte padrão do sistema
fonte = pygame.freetype.SysFont(pygame.freetype.get_default_font(), 12) 

velocidade = 3
preto = 0, 0, 0
branco = 255, 255, 255

#Cria a tela e lista de sprites
size = width, height = 1000, 1000
tela = pygame.display.set_mode(size)
lista_sprites = pygame.sprite.Group()

#Criação do player
player = Player()
playerrect = player.rect
playerrect.center = (150, 700)
lista_sprites.add(player)

#Criação do mapa
q = pygame.image.load("quadradopreto.png").convert()
quadrados = [(q, (0,0))]
colisores = []
#Matriz map
mapa = [
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
       ]
#Cria cada quadrado do mapa
for i in range(len(mapa)):
    for j in range(len(mapa[i])):
        if mapa[i][j] == 1:
            r = pygame.Rect([j*100, i*100], [100, 100])
            quadrados.append((q, (j*100, i*100)))
            colisores.append(r)


def movimento():
    teclas = pygame.key.get_pressed()
    movimento = pygame.Vector2()

    if teclas[pygame.K_w] and playerrect.top > 0:  
        movimento += (0, -1 * velocidade)
    if teclas[pygame.K_s] and playerrect.bottom < height:    
        movimento += (0, 1 * velocidade)
    if teclas[pygame.K_a] and playerrect.left > 0:      
        movimento += (-1 * velocidade, 0)
        if teclas[pygame.K_s] != teclas[pygame.K_w] and teclas[pygame.K_d] != teclas[pygame.K_a]:
            movimento *= 0.71
    if teclas[pygame.K_d] and playerrect.right < width: 
        movimento += (1 * velocidade, 0)
        if teclas[pygame.K_s] != teclas[pygame.K_w] and teclas[pygame.K_d] != teclas[pygame.K_a]:
            movimento *= 0.71

    return movimento

def detectar_col():
    col = playerrect.collidelist(colisores)
    mover = pygame.Vector2()

    #Caso haja uma colisão
    if col != -1:
        colrect = colisores[col]
        mover = (min(colrect.right - playerrect.left, colrect.left - playerrect.right), min(colrect.top - playerrect.bottom, colrect.bottom - playerrect.top))
        if abs(mover[0]) < abs(mover[1]):
            mover = (mover[0], 0)
        else:
            mover = (0, mover[1])
    return mover

while True:
    #Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    #Movimentação do jogador
    v_movimento = movimento()
    playerrect = playerrect.move(v_movimento)
    #Detecção de Colisão
    v_movimento = detectar_col()
    playerrect = playerrect.move(v_movimento)
    player.mover(playerrect.center)
    
    #Renderização
    tela.fill(branco)
    tela.blits(quadrados)
    fonte.render_to(tela, [0, 0], str(movimento()), branco)

    lista_sprites.draw(tela)

    pygame.display.flip()
    pygame.time.delay(10)