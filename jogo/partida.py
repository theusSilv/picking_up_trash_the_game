import random

import pygame

from jogo.config import (ALTURA, AMARELO, BRANCO, LARGURA, PONTOS_POR_FLOR,
                         PONTOS_POR_LIXO, PONTOS_POR_MAPA, TEMPO_FASE,
                         VERMELHO, VIDAS_INFINITO)
from jogo.fases import FASES
from jogo.cachorro import Cachorro
from jogo.item import CORACAO, FLOR, LIXO, Item
from jogo.jogador import Jogador

COR_ROTULO = (190, 235, 200)
VERDE_CLARO = (130, 235, 150)


class Aviso:
    # Texto que sobe e some (ex.: "+1")
    def __init__(self, texto, x, y, cor):
        self.texto = texto
        self.x = x
        self.y = y
        self.cor = cor
        self.vida = 0.9

    def atualizar(self, dt):
        self.y -= 50 * dt
        self.vida -= dt

    def desenhar(self, tela, interface):
        interface.texto(tela, interface.fonte_media, self.texto, (self.x, self.y), self.cor, centro=True)


class Partida:
    # Parte comum dos dois modos: itens caindo, jogador e colisões.
    # Cada modo define o que acontece ao pegar (ou perder) um item.
    def __init__(self, jogo, mapa):
        self.jogo = jogo
        self.mapa = mapa
        self.jogador = Jogador(jogo.skin)
        self.cachorro = Cachorro(self.jogador)
        self.itens = []
        self.avisos = []
        self.tempo_total = 0.0
        self.proximo_item = 0.6
        self.pisca = 0.0
        self.terminou = False

        self.lampejo = pygame.Surface((LARGURA, ALTURA))
        self.lampejo.fill((255, 0, 0))

        # valores que mudam conforme o modo (ver atualizar_dificuldade)
        self.vel_min = 260
        self.vel_max = 360
        self.intervalo = 0.7
        self.chance_flor = 0.1
        self.chance_coracao = 0.0
        self.balanca = False
        self.vel_jogador = 640

    def atualizar_dificuldade(self):
        pass

    def pegou_lixo(self, item):
        pass

    def pegou_flor(self, item):
        pass

    def pegou_coracao(self, item):
        pass

    def perdeu_lixo(self, item):
        pass

    def verificar_fim(self):
        pass

    def desenhar_hud(self, tela):
        pass

    def pular(self):
        if self.jogador.pular():
            self.jogo.sons.tocar("pulo")

    def avisar(self, texto, x, y, cor):
        self.avisos.append(Aviso(texto, x, y - 20, cor))

    def sortear_tipo(self):
        sorteio = random.random()
        if sorteio < self.chance_coracao:
            return CORACAO
        if sorteio < self.chance_coracao + self.chance_flor:
            return FLOR
        return LIXO

    def gerar_item(self):
        tipo = self.sortear_tipo()
        velocidade = random.uniform(self.vel_min, self.vel_max)
        if tipo == FLOR:
            imagem = self.jogo.imagem_flor
        elif tipo == CORACAO:
            imagem = self.jogo.imagem_coracao
            velocidade *= 0.85          # o coração cai um pouco mais devagar
        else:
            imagem = random.choice(self.jogo.imagens_lixo)
        self.itens.append(Item(imagem, tipo, velocidade, self.balanca))
        self.proximo_item = self.intervalo * random.uniform(0.7, 1.3)

    def atualizar(self, dt, direcao):
        self.tempo_total += dt
        self.atualizar_dificuldade()
        self.jogador.velocidade = self.vel_jogador
        self.jogador.atualizar(direcao, dt)
        self.cachorro.atualizar(dt)
        self.pisca = max(0.0, self.pisca - dt)

        self.proximo_item -= dt
        if self.proximo_item <= 0:
            self.gerar_item()

        area = self.jogador.area_coleta()
        for item in self.itens[:]:
            item.atualizar(dt)
            if area.collidepoint(item.x, item.y):
                self.itens.remove(item)
                if item.tipo == FLOR:
                    self.pegou_flor(item)
                elif item.tipo == CORACAO:
                    self.pegou_coracao(item)
                else:
                    self.pegou_lixo(item)
            elif item.y > self.jogador.y_chao + 4:
                # chegou no chão sem ser pego
                self.itens.remove(item)
                if item.tipo == LIXO:
                    self.perdeu_lixo(item)

        for aviso in self.avisos[:]:
            aviso.atualizar(dt)
            if aviso.vida <= 0:
                self.avisos.remove(aviso)

        self.verificar_fim()

    def desenhar(self, tela):
        tela.blit(self.mapa.imagem, (0, 0))
        self.cachorro.desenhar(tela)
        for item in self.itens:
            item.desenhar(tela)
        self.jogador.desenhar(tela)
        for aviso in self.avisos:
            aviso.desenhar(tela, self.jogo.interface)
        if self.pisca > 0:
            self.lampejo.set_alpha(int(110 * self.pisca / 0.35))
            tela.blit(self.lampejo, (0, 0))
        self.desenhar_hud(tela)
        self.desenhar_dica(tela)

    def texto_dica(self):
        return "Setas ou A/D: mover   |   ESPAÇO: pular   |   Pegue o lixo e evite as flores"

    def desenhar_dica(self, tela):
        # lembrete dos comandos nos primeiros segundos
        if self.tempo_total > 7:
            return
        alfa = int(235 * min(1.0, (7 - self.tempo_total) / 1.5))
        mensagem = self.texto_dica()
        texto = self.jogo.interface.fonte_pequena.render(mensagem, True, BRANCO)
        texto.set_alpha(alfa)
        caixa = pygame.Surface((texto.get_width() + 30, 38), pygame.SRCALPHA)
        pygame.draw.rect(caixa, (0, 0, 0, int(alfa * 0.65)), caixa.get_rect(), border_radius=12)
        caixa.blit(texto, (15, 8))
        tela.blit(caixa, caixa.get_rect(center=(LARGURA // 2, 104)))


class PartidaFase(Partida):
    # Modo história: pegar a meta de lixos antes dos 60 segundos
    def __init__(self, jogo, indice_fase):
        self.indice = indice_fase
        self.fase = FASES[indice_fase]
        super().__init__(jogo, jogo.mapas[self.fase.mapa])
        self.coletados = 0
        self.venceu = False
        self.atualizar_dificuldade()

    def tempo_restante(self):
        return max(0.0, TEMPO_FASE - self.tempo_total)

    def atualizar_dificuldade(self):
        # dentro da fase a queda e a quantidade de itens aumentam aos poucos
        progresso = min(1.0, self.tempo_total / TEMPO_FASE)
        fase = self.fase
        self.vel_min = fase.vel_minima * (1 + 0.25 * progresso)
        self.vel_max = fase.vel_maxima * (1 + 0.25 * progresso)
        self.intervalo = fase.intervalo / (1 + 0.35 * progresso)
        self.chance_flor = fase.chance_flor
        self.balanca = fase.balanca
        self.vel_jogador = fase.vel_jogador

    def pegou_lixo(self, item):
        self.coletados += 1
        self.jogo.sons.tocar("coleta")
        self.avisar("+1", item.x, item.y, AMARELO)

    def pegou_flor(self, item):
        self.coletados = max(0, self.coletados - 1)
        self.pisca = 0.35
        self.jogo.sons.tocar("erro")
        self.avisar("-1 Não é lixo!", item.x, item.y, VERMELHO)

    def verificar_fim(self):
        if self.coletados >= self.fase.meta:
            self.venceu = True
            self.terminou = True
        elif self.tempo_restante() <= 0:
            self.terminou = True

    def desenhar_hud(self, tela):
        ui = self.jogo.interface
        ui.barra_topo(tela)

        ui.texto(tela, ui.fonte_pequena, "LIXO COLETADO", (16, 8), COR_ROTULO)
        ui.texto(tela, ui.fonte_media, "%d/%d" % (self.coletados, self.fase.meta), (16, 32))
        ui.barra_progresso(tela, 140, 42, 170, 18, self.coletados / self.fase.meta)

        segundos = int(self.tempo_restante() + 0.999)
        cor = BRANCO
        if self.tempo_restante() <= 10:
            cor = VERMELHO if int(self.tempo_restante() * 4) % 2 == 0 else AMARELO
        ui.texto(tela, ui.fonte_pequena, "TEMPO RESTANTE", (LARGURA // 2, 16), COR_ROTULO, centro=True)
        ui.texto(tela, ui.fonte_media, "%02d:%02d" % (segundos // 60, segundos % 60),
                 (LARGURA // 2, 48), cor, centro=True)

        ui.texto_direita(tela, ui.fonte_pequena, "NÍVEL %d/%d" % (self.indice + 1, len(FASES)),
                         LARGURA - 16, 8, COR_ROTULO)
        ui.texto_direita(tela, ui.fonte_media, self.fase.nome, LARGURA - 16, 32)


class PartidaInfinita(Partida):
    # Modo infinito: joga até acabarem as vidas. O mapa muda conforme os pontos.
    def __init__(self, jogo):
        super().__init__(jogo, jogo.mapas[0])
        self.pontos = 0
        self.maior_pontuacao = 0
        self.vidas = VIDAS_INFINITO
        self.indice_mapa = 0
        self.mapas_visitados = 1
        self.transicao = None        # tempo da troca de mapa (None = sem troca)
        self.novo_mapa = 0
        self.atualizar_dificuldade()

    def atualizar_dificuldade(self):
        nivel = self.pontos / 100
        self.vel_min = min(260 + 18 * nivel, 520)
        self.vel_max = min(360 + 24 * nivel, 700)
        self.intervalo = max(0.36, 0.90 - 0.036 * nivel)
        self.chance_flor = min(0.30, 0.10 + 0.012 * nivel)
        self.balanca = self.pontos >= 400
        self.vel_jogador = min(640 + 12 * nivel, 820)
        # corações só aparecem quando falta vida (mais seguido quando só resta uma)
        if self.vidas >= VIDAS_INFINITO:
            self.chance_coracao = 0.0
        elif self.vidas == 1:
            self.chance_coracao = 0.18
        elif self.vidas == 2:
            self.chance_coracao = 0.12
        else:
            self.chance_coracao = 0.09

    def atualizar(self, dt, direcao):
        if self.transicao is not None:
            self.atualizar_transicao(dt)
            return
        super().atualizar(dt, direcao)

    def atualizar_transicao(self, dt):
        # o jogo fica parado por menos de 1 segundo enquanto o mapa troca
        self.transicao += dt
        if self.transicao >= 0.4 and self.mapa is not self.jogo.mapas[self.novo_mapa]:
            self.mapa = self.jogo.mapas[self.novo_mapa]
            self.indice_mapa = self.novo_mapa
            self.itens = []
        if self.transicao >= 0.8:
            self.transicao = None

    def verificar_troca_de_mapa(self):
        if self.transicao is not None:
            return
        indice = (self.maior_pontuacao // PONTOS_POR_MAPA) % len(self.jogo.mapas)
        if indice != self.indice_mapa:
            self.novo_mapa = indice
            self.transicao = 0.0
            self.mapas_visitados += 1
            self.jogo.sons.tocar("mapa")

    def pegou_lixo(self, item):
        self.pontos += PONTOS_POR_LIXO
        self.maior_pontuacao = max(self.maior_pontuacao, self.pontos)
        self.jogo.sons.tocar("coleta")
        self.avisar("+%d" % PONTOS_POR_LIXO, item.x, item.y, AMARELO)
        self.verificar_troca_de_mapa()

    def pegou_flor(self, item):
        self.pontos = max(0, self.pontos - PONTOS_POR_FLOR)
        self.perder_vida()
        self.jogo.sons.tocar("erro")
        self.avisar("-1 vida: não é lixo!", item.x, item.y, VERMELHO)

    def pegou_coracao(self, item):
        self.vidas = min(VIDAS_INFINITO, self.vidas + 1)
        self.jogo.sons.tocar("coracao")
        self.avisar("+1 vida", item.x, item.y, VERDE_CLARO)

    def texto_dica(self):
        return "Setas ou A/D: mover   |   ESPAÇO: pular   |   Pegue lixo e corações, evite as flores"

    def perdeu_lixo(self, item):
        self.perder_vida()
        self.jogo.sons.tocar("vida")
        self.avisar("Lixo no chão!", item.x, self.jogador.y_chao - 30, VERMELHO)

    def perder_vida(self):
        self.vidas -= 1
        self.pisca = 0.35

    def verificar_fim(self):
        if self.vidas <= 0:
            self.terminou = True

    def desenhar(self, tela):
        super().desenhar(tela)
        if self.transicao is not None:
            self.desenhar_transicao(tela)

    def desenhar_transicao(self, tela):
        # escurece até a metade e volta a clarear, mostrando o nome do mapa
        metade = 0.4
        if self.transicao < metade:
            escuro = self.transicao / metade
        else:
            escuro = max(0.0, 1 - (self.transicao - metade) / metade)
        cortina = pygame.Surface((LARGURA, ALTURA))
        cortina.set_alpha(int(255 * escuro))
        tela.blit(cortina, (0, 0))
        if escuro > 0.3:
            ui = self.jogo.interface
            nome = self.jogo.mapas[self.novo_mapa].nome
            ui.texto(tela, ui.fonte_pequena, "NOVO MAPA", (LARGURA // 2, ALTURA // 2 - 40), COR_ROTULO, centro=True)
            ui.texto(tela, ui.fonte_grande, nome, (LARGURA // 2, ALTURA // 2 + 10), BRANCO, centro=True)

    def desenhar_hud(self, tela):
        ui = self.jogo.interface
        ui.barra_topo(tela)

        ui.texto(tela, ui.fonte_pequena, "PONTOS", (16, 8), COR_ROTULO)
        ui.texto(tela, ui.fonte_media, str(self.pontos), (16, 32))
        recorde = max(self.jogo.recorde, self.maior_pontuacao)
        ui.texto(tela, ui.fonte_pequena, "Recorde: %d" % recorde, (170, 40), COR_ROTULO)

        ui.texto(tela, ui.fonte_pequena, "VIDAS", (LARGURA // 2, 16), COR_ROTULO, centro=True)
        largura = VIDAS_INFINITO * 38
        ui.coracoes(tela, LARGURA // 2 - largura // 2, 34, self.vidas, VIDAS_INFINITO)

        ui.texto_direita(tela, ui.fonte_pequena, "MODO INFINITO", LARGURA - 16, 8, COR_ROTULO)
        ui.texto_direita(tela, ui.fonte_media, self.mapa.nome, LARGURA - 16, 32)
