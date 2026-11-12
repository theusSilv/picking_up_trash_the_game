import pygame

from jogo.config import GRAVIDADE, LARGURA, Y_CHAO
from jogo.recursos import carregar_imagem

DISTANCIA = 130          # quanto ele fica longe do dono
VELOCIDADE_MAX = 760
FOLGA_PES = 3            # o contorno do sprite passa uns pixels abaixo das patas


def espelhar(imagens):
    return [pygame.transform.flip(img, True, False) for img in imagens]


def carregar(nome, quantidade):
    return [carregar_imagem("cachorro", "%s_%d.png" % (nome, i)) for i in range(1, quantidade + 1)]


class Cachorro:
    #Só segue o dono e faz animações:
    
    def __init__(self, dono):
        self.dono = dono

        direita = {
            "parado": carregar("parado", 3),
            "andar": carregar("andar", 6),
            "correr": carregar("correr", 6),
            "sentar": carregar("sentar", 4),
        }
        # os sprites olham para a direita; para a esquerda a gente espelha
        self.imagens = {
            1: direita,
            -1: {nome: espelhar(lista) for nome, lista in direita.items()},
        }

        self.x = dono.x - DISTANCIA
        self.y_chao = Y_CHAO
        self.y = Y_CHAO
        self.velocidade_y = 0.0
        self.no_ar = False
        self.dono_no_ar = False
        self.lado = -1              # -1: fica à esquerda do dono, 1: à direita
        self.olhando = 1
        self.estado = "parado"
        self.tempo_estado = 0.0
        self.tempo_parado = 0.0

        self.sombra = pygame.Surface((70, 16), pygame.SRCALPHA)
        pygame.draw.ellipse(self.sombra, (0, 0, 0, 55), (0, 0, 70, 16))

    def atualizar(self, dt):
        dono = self.dono

        # fica atrás do dono; só troca de lado se o dono andar um tempo para o outro lado
        if dono.direcao != 0 and dono.tempo_andando > 0.35:
            self.lado = -dono.olhando
        alvo = dono.x + self.lado * DISTANCIA
        alvo = max(50, min(LARGURA - 50, alvo))

        distancia = alvo - self.x
        velocidade = 0.0
        if abs(distancia) > 8:
            velocidade = min(abs(distancia) * 5, VELOCIDADE_MAX)
            passo = min(abs(distancia), velocidade * dt)
            self.x += passo if distancia > 0 else -passo
            self.olhando = 1 if distancia > 0 else -1
            self.tempo_parado = 0.0
        else:
            self.tempo_parado += dt
            self.olhando = 1 if dono.x > self.x else -1     # olha para o dono
        if velocidade > 320:
            novo = "correr"
        elif velocidade > 70:
            novo = "andar"
        elif self.tempo_parado > 3:
            novo = "sentar"
        else:
            novo = "parado"
        if novo != self.estado:
            self.estado = novo
            self.tempo_estado = 0.0
        self.tempo_estado += dt

        # só pula quando o dono pula
        if dono.no_ar and not self.dono_no_ar and not self.no_ar:
            self.no_ar = True
            self.velocidade_y = -520
        self.dono_no_ar = dono.no_ar
        if self.no_ar:
            self.velocidade_y += GRAVIDADE * dt
            self.y += self.velocidade_y * dt
            if self.y >= self.y_chao:
                self.y = self.y_chao
                self.velocidade_y = 0.0
                self.no_ar = False

    def imagem_atual(self):
        grupo = self.imagens[self.olhando]
        if self.no_ar:
            return grupo["correr"][2]
        velocidades = {"correr": 14, "andar": 9, "sentar": 3, "parado": 3}
        quadros = grupo[self.estado]
        return quadros[int(self.tempo_estado * velocidades[self.estado]) % len(quadros)]

    def desenhar(self, tela):
        altura = self.y_chao - self.y
        fator = max(0.5, 1 - altura / 200)
        sombra = pygame.transform.smoothscale(self.sombra, (int(70 * fator), int(16 * fator)))
        tela.blit(sombra, sombra.get_rect(center=(self.x, self.y_chao + 1)))

        imagem = self.imagem_atual()
        tela.blit(imagem, imagem.get_rect(midbottom=(self.x, self.y + FOLGA_PES)))
