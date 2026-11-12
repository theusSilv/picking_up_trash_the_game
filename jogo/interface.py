import pygame

from jogo.config import (ALTURA, BRANCO, LARGURA, VERDE_ESCURO, VERMELHO)


class Interface:
    # Fontes 
    def __init__(self):
        self.fonte_pequena = pygame.font.SysFont("arial", 20, bold=True)
        self.fonte_media = pygame.font.SysFont("arial", 28, bold=True)
        self.fonte_grande = pygame.font.SysFont("arial", 52, bold=True)
        self.fonte_titulo = pygame.font.SysFont("arial", 64, bold=True)

        self.veu = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
        self.veu.fill((0, 0, 0, 140))
        self.fundo_hud = self.criar_fundo_hud()
        self.paineis = {}

    def texto(self, tela, fonte, mensagem, pos, cor=BRANCO, centro=False, sombra=True):
        imagem = fonte.render(mensagem, True, cor)
        rect = imagem.get_rect()
        if centro:
            rect.center = pos
        else:
            rect.topleft = pos
        if sombra:
            contorno = fonte.render(mensagem, True, (0, 0, 0))
            tela.blit(contorno, (rect.x + 2, rect.y + 2))
        tela.blit(imagem, rect)
        return rect

    def texto_direita(self, tela, fonte, mensagem, x_direita, y, cor=BRANCO):
        largura = fonte.size(mensagem)[0]
        self.texto(tela, fonte, mensagem, (x_direita - largura, y), cor)

    def painel(self, tela, largura, altura):
        # escurece a tela e desenha uma caixa clara no meio
        tela.blit(self.veu, (0, 0))
        chave = (largura, altura)
        if chave not in self.paineis:
            self.paineis[chave] = self.criar_painel(largura, altura)
        imagem = self.paineis[chave]
        rect = imagem.get_rect(center=(LARGURA // 2, ALTURA // 2))
        tela.blit(imagem, rect)
        return rect

    def criar_painel(self, largura, altura):
        imagem = pygame.Surface((largura, altura), pygame.SRCALPHA)
        rect = imagem.get_rect()
        pygame.draw.rect(imagem, (250, 250, 242), rect, border_radius=22)
        pygame.draw.rect(imagem, VERDE_ESCURO, rect, 6, border_radius=22)
        pygame.draw.rect(imagem, (120, 200, 140), rect.inflate(-20, -20), 2, border_radius=16)
        return imagem

    def criar_fundo_hud(self):
        fundo = pygame.Surface((LARGURA, 74), pygame.SRCALPHA)
        for y in range(74):
            pygame.draw.line(fundo, (8, 34, 26, int(205 - 75 * y / 74)), (0, y), (LARGURA, y))
        pygame.draw.line(fundo, (120, 220, 150, 190), (0, 72), (LARGURA, 72), 2)
        return fundo

    def barra_topo(self, tela):
        tela.blit(self.fundo_hud, (0, 0))

    def barra_progresso(self, tela, x, y, largura, altura, fracao):
        fracao = max(0.0, min(1.0, fracao))
        pygame.draw.rect(tela, (50, 50, 60), (x, y, largura, altura), border_radius=9)
        if fracao > 0:
            pygame.draw.rect(tela, (60, 180, 90), (x, y, int(largura * fracao), altura), border_radius=9)
        pygame.draw.rect(tela, BRANCO, (x, y, largura, altura), 2, border_radius=9)

    def coracoes(self, tela, x, y, vidas, total):
        for i in range(total):
            cor = VERMELHO if i < vidas else (90, 90, 100)
            cx = x + i * 38
            pygame.draw.circle(tela, cor, (cx + 8, y + 8), 8)
            pygame.draw.circle(tela, cor, (cx + 22, y + 8), 8)
            pygame.draw.polygon(tela, cor, [(cx, y + 11), (cx + 30, y + 11), (cx + 15, y + 28)])
