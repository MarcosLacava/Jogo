from email.errors import InvalidDateDefect
import pygame

class Flor(pygame.sprite.Sprite):

    def __init__(self, tempo, pos) -> None:
        self.maxidade = 17 # Número de estágios de vida da flor (Sprites)
        self.maxtempo = 180000 # Tempo de vida maximo da flor
        self.fase = (self.maxtempo // self.maxidade) + 50 # Duração de um estágio da flor
        print(self.fase)

        if tempo < self.maxtempo: # Cálcula o estágio atual ao entrar na sala com base no tempo de jogo total
            self.idade = (tempo*self.maxidade)//self.maxtempo
        else:
            self.idade = self.maxidade

        self.limite = ((self.fase + 1) * self.idade) # Tempo máximo total do estágio atual

    def update(self, tempo) -> None:
        if tempo >= self.limite and self.idade < self.maxidade:
            print(self.limite)
            return self.trocar_fase() + 10
        return 0

    def trocar_fase(self):
        self.idade += 1
        self.limite = ((self.fase + 1) * self.idade)
        return self.idade
