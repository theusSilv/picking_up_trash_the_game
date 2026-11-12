import math
import random

import pygame

from jogo.config import LARGURA


# Tipos de item
LIXO = "lixo"
FLOR = "flor"          # não é lixo
CORACAO = "coracao"    # dá uma vida no modo infinito


class Item:
    # Algo que cai do alto da tela
    def __init__(self, imagem, tipo, velocidade, balanca):
        self.imagem = imagem
        self.tipo = tipo
        self.velocidade = velocidade
        self.x_base = random.randint(60, LARGURA - 60)
        self.x = float(self.x_base)
        self.y = -60.0
        self.tempo = 0.0
        self.fase_balanco = random.uniform(0, math.tau)
        self.inclinacao_max = random.uniform(5, 14)
        self.angulo = 0.0
        if balanca:
            self.amplitude = random.uniform(30, 90)
        else:
            self.amplitude = 0
        self.frequencia = random.uniform(2.0, 4.0)

    def atualizar(self, dt):
        self.tempo += dt
        self.y += self.velocidade * dt
        self.angulo = self.inclinacao_max * math.sin(self.fase_balanco + self.tempo * 2.4)
        if self.amplitude:
            x = self.x_base + math.sin(self.fase_balanco + self.tempo * self.frequencia) * self.amplitude
            self.x = max(40, min(LARGURA - 40, x))

    def desenhar(self, tela):
        imagem = self.imagem
        if abs(self.angulo) > 1.5:
            imagem = pygame.transform.rotate(imagem, self.angulo)
        tela.blit(imagem, imagem.get_rect(center=(self.x, self.y)))
