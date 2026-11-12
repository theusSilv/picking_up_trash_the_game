import math

import pygame

from jogo.config import GRAVIDADE, LARGURA, PULO_VELOCIDADE, Y_CHAO
from jogo.recursos import carregar_imagem

FOLGA_PES = 3     # o contorno do sprite passa uns pixels abaixo dos pés


def espelhar(imagens):
    return [pygame.transform.flip(img, True, False) for img in imagens]


class Jogador:
    def __init__(self, skin="vermelho"):
        # os sprites originais olham para a direita; para a esquerda a gente espelha
        parado = [carregar_imagem("personagem", skin, "parado_%d.png" % i) for i in (1, 2, 3)]
        correr = [carregar_imagem("personagem", skin, "correr_%d.png" % i) for i in range(1, 10)]
        pulo = [carregar_imagem("personagem", skin, nome + ".png")
                for nome in ("pulo_subida", "pulo_topo", "pulo_descida")]
        pouso = [carregar_imagem("personagem", skin, "pouso.png")]

        self.imagens = {
            1: {"parado": parado, "correr": correr, "pulo": pulo, "pouso": pouso},
            -1: {"parado": espelhar(parado), "correr": espelhar(correr),
                 "pulo": espelhar(pulo), "pouso": espelhar(pouso)},
        }

        self.x = LARGURA / 2
        self.y_chao = Y_CHAO
        self.y = Y_CHAO             # posição dos pés (muda durante o pulo)
        self.velocidade = 640
        self.velocidade_y = 0.0
        self.no_ar = False
        self.direcao = 0            # -1 esquerda, 0 parado, 1 direita
        self.olhando = 1            # para que lado ele está virado
        self.tempo = 0.0            # tempo total (animação de parado)
        self.tempo_andando = 0.0
        self.tempo_pouso = 0.0

        # sombra no chão
        self.sombra = pygame.Surface((110, 26), pygame.SRCALPHA)
        pygame.draw.ellipse(self.sombra, (0, 0, 0, 40), (0, 0, 110, 26))
        pygame.draw.ellipse(self.sombra, (0, 0, 0, 60), (15, 5, 80, 16))

    def pular(self):
        # devolve True se o pulo começou (não pula de novo no ar)
        if self.no_ar:
            return False
        self.no_ar = True
        self.velocidade_y = -PULO_VELOCIDADE
        return True

    def atualizar(self, direcao, dt):
        self.tempo += dt
        self.direcao = direcao

        # movimento para os lados (também vale no ar)
        if direcao != 0:
            self.olhando = direcao
            self.tempo_andando += dt
            self.x += direcao * self.velocidade * dt
            self.x = max(60, min(LARGURA - 60, self.x))
        else:
            self.tempo_andando = 0.0

        # pulo
        if self.no_ar:
            self.velocidade_y += GRAVIDADE * dt
            self.y += self.velocidade_y * dt
            if self.y >= self.y_chao:
                self.y = self.y_chao
                self.velocidade_y = 0.0
                self.no_ar = False
                self.tempo_pouso = 0.12
        elif self.tempo_pouso > 0:
            self.tempo_pouso -= dt

    def imagem_atual(self):
        grupo = self.imagens[self.olhando]
        if self.no_ar:
            if self.velocidade_y < -250:
                return grupo["pulo"][0]
            if self.velocidade_y < 250:
                return grupo["pulo"][1]
            return grupo["pulo"][2]
        if self.direcao != 0:
            return grupo["correr"][int(self.tempo_andando * 14) % len(grupo["correr"])]
        if self.tempo_pouso > 0:
            return grupo["pouso"][0]
        # parado: respirando devagar (quadros 1, 2, 3, 2)
        ciclo = [0, 1, 2, 1]
        return grupo["parado"][ciclo[int(self.tempo * 4) % 4]]

    def area_coleta(self):
        # cabeça e tronco do personagem
        return pygame.Rect(self.x - 56, self.y - 167, 112, 115)

    def desenhar(self, tela):
        # sombra fica no chão e diminui quando ele está no alto
        altura = self.y_chao - self.y
        fator = max(0.5, 1 - altura / 300)
        sombra = pygame.transform.smoothscale(self.sombra, (int(110 * fator), int(26 * fator)))
        tela.blit(sombra, sombra.get_rect(center=(self.x, self.y_chao + 1)))

        imagem = self.imagem_atual()
        pulinho = 0
        if self.direcao != 0 and not self.no_ar:
            pulinho = abs(math.sin(self.tempo_andando * 14 * math.pi / 2)) * 3
        tela.blit(imagem, imagem.get_rect(midbottom=(self.x, self.y + FOLGA_PES - pulinho)))
