from cmath import rect
import json
from msilib import sequence
import os
from tkinter import EXCEPTION
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
erro = pygame.image.load(os.path.join("Sprites", "Erro.png")).convert()

def cortar_sprites(nome):
    # Corta a spritesheet no determinado lugar e retorna uma sprite
    try:
        sprites = []
        spritesheet = pygame.image.load(os.path.join("Sprites", "Player.png")).convert_alpha()
        with open(os.path.join("Sprites", "Player.png")) as d:
            metadata = json.load(d)

        for i in range(len(d.self.metadata)):
            d = metadata["frames"][i]["frame"]
            x, y, w, h = d["x"], d["y"], d["w"], d["h"]
            spr = pygame.Surface((w, h))
            spr.set_colorkey((0,0,0))
            spr.blit(spritesheet, (0,0), (x,y,w,h))
            sprites.append(spr)
    except FileNotFoundError:
        print("Erro")
        sprites.append(erro)
        sprites.append(erro)
    return sprites

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
player = Player(matriz_mapa, (3,1), mapaTeste.tileLen, cortar_sprites("Player"))
lista_sprites.add(player)

while True:
    #Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        
    player.update()

    #Renderização
    tela.fill(branco)
    tela.blits(mapaTeste.quadrados)
    fonte.render_to(tela, [0, 0], str(player.movimento()), branco)

    lista_sprites.draw(tela)

    pygame.display.update()
    clock.tick(30)

    