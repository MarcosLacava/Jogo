from email.errors import InvalidDateDefect
import pygame

class Flor(pygame.sprite.Sprite):

    def __init__(self, tempo, coletada) -> None:
        self.maxidade = 17 # Número de estágios de vida da flor (Sprites)
        self.maxtempo = 180000 # Tempo de vida maximo da flor
        self.coletada = coletada # Guarda se a flor ja foi coletada ou nao

        self.fase = (self.maxtempo // self.maxidade) + 50 # Duração de um estágio da flor

        if tempo < self.maxtempo: # Cálcula o estágio atual ao entrar na sala com base no tempo de jogo total
            self.idade = (tempo*self.maxidade)//self.maxtempo
        else:
            self.idade = self.maxidade

        self.limite = ((self.fase + 1) * self.idade) # Tempo máximo total do estágio atual
        if coletada: self.coletar()

    def update(self, tempo) -> None:
        if not self.coletada and tempo >= self.limite and self.idade < self.maxidade:
            return self.trocar_fase() + 11
        return 0

    def coletar(self):
        self.idade = 16
        self.trocar_fase()
        self.coletada = True
    
    def trocar_fase(self):
        self.idade += 1
        self.limite = ((self.fase + 1) * self.idade)
        return self.idade
