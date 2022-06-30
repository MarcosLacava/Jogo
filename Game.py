from cmath import rect
from msilib import sequence
from Player import Player
import sys, pygame, pygame.freetype
from typing import Sequence
from Mapa import Mapa

pygame.init()

# Game Clock
clock = pygame.time.Clock()

# Fonte padrão do sistema
fonte = pygame.freetype.SysFont(pygame.freetype.get_default_font(), 12) 

preto = 0, 0, 0
branco = 255, 255, 255

# Cria a tela e lista de sprites
size = width, height = 1000, 1000
tela = pygame.display.set_mode(size)
lista_sprites = pygame.sprite.Group()

# Criação do player
player = Player() 
lista_sprites.add(player)

# Criação do Mapa
mapa = Mapa()


'''
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
'''

while True:
    #Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
    
    player.update()

    #Renderização
    tela.fill(branco)
    tela.blits(mapa.quadrados)
    fonte.render_to(tela, [0, 0], str(player.movimento()), branco)

    lista_sprites.draw(tela)

    pygame.display.update()
    clock.tick(60)