import pygame

from jogo.config import ALTURA, LARGURA, PRETO, SKINS, TEMPO_FASE, VERDE_ESCURO, VERMELHO
from jogo.fases import FASES
from jogo.recursos import carregar_imagem


class Tela:
    # Base de todas as telas do jogo
    def __init__(self, jogo):
        self.jogo = jogo

    def evento(self, evento):
        pass

    def atualizar(self, dt):
        pass

    def desenhar(self, tela):
        pass

    def confirmou(self, evento):
        return evento.type == pygame.KEYDOWN and evento.key in (
            pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE)

    def voltou(self, evento):
        return evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE

    def mini_personagem(self, tela, cx, cy, altura):
        imagem = self.jogo.imagem_menu
        largura = int(imagem.get_width() * altura / imagem.get_height())
        imagem = pygame.transform.smoothscale(imagem, (largura, altura))
        tela.blit(imagem, imagem.get_rect(center=(cx, cy)))


class TelaMenu(Tela):
    OPCOES = ["Modo História", "Modo Infinito", "Skins", "Sair"]
    # posição (x, y) de cada botão no painel da imagem do menu
    BOTOES_X = 496
    BOTOES_Y = [342, 398, 455, 511]
    BOTAO_LARGURA = 288
    BOTAO_ALTURA = 47

    def __init__(self, jogo):
        super().__init__(jogo)
        self.selecionada = 0

    def evento(self, evento):
        if evento.type != pygame.KEYDOWN:
            return
        teclas_numeros = [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]
        if evento.key in (pygame.K_UP, pygame.K_w):
            self.selecionada = (self.selecionada - 1) % len(self.OPCOES)
            self.jogo.sons.tocar("clique")
        elif evento.key in (pygame.K_DOWN, pygame.K_s):
            self.selecionada = (self.selecionada + 1) % len(self.OPCOES)
            self.jogo.sons.tocar("clique")
        elif evento.key in teclas_numeros:
            self.selecionada = teclas_numeros.index(evento.key)
            self.escolher()
        elif self.confirmou(evento):
            self.escolher()
        elif evento.key == pygame.K_ESCAPE:
            self.jogo.rodando = False

    def escolher(self):
        self.jogo.sons.tocar("clique")
        if self.selecionada == 0:
            self.jogo.iniciar_fases()
        elif self.selecionada == 1:
            self.jogo.iniciar_infinito()
        elif self.selecionada == 2:
            self.jogo.trocar_tela(TelaSkins(self.jogo))
        else:
            self.jogo.rodando = False

    def desenhar_botao(self, tela, rect, nome, selecionado):
        ui = self.jogo.interface
        if selecionado:
            pygame.draw.rect(tela, (200, 245, 212), rect, border_radius=9)
            pygame.draw.rect(tela, (28, 120, 40), rect, 3, border_radius=9)
            pygame.draw.rect(tela, (235, 235, 70), rect.inflate(-8, -8), 2, border_radius=7)
            cor = (18, 110, 34)
        else:
            pygame.draw.rect(tela, (150, 98, 66), rect, border_radius=9)
            corpo = pygame.Rect(rect.x, rect.y, rect.w, rect.h - 4)
            pygame.draw.rect(tela, (196, 134, 96), corpo, border_radius=9)
            pygame.draw.rect(tela, (214, 158, 118), (rect.x + 6, rect.y + 3, rect.w - 12, 4), border_radius=2)
            pygame.draw.rect(tela, (96, 58, 38), rect, 2, border_radius=9)
            cor = (25, 20, 15)
        ui.texto(tela, ui.fonte_media, nome, rect.center, cor, centro=True, sombra=False)

    def desenhar(self, tela):
        ui = self.jogo.interface
        tela.blit(self.jogo.fundo_menu, (0, 0))
        for i, nome in enumerate(self.OPCOES):
            rect = pygame.Rect(self.BOTOES_X, self.BOTOES_Y[i], self.BOTAO_LARGURA, self.BOTAO_ALTURA)
            self.desenhar_botao(tela, rect, nome, i == self.selecionada)
        ui.texto_direita(tela, ui.fonte_pequena, "Recorde: %d" % self.jogo.recorde, LARGURA - 20, ALTURA - 32)


class TelaSkins(Tela):
    # Escolha da aparência do personagem
    def __init__(self, jogo):
        super().__init__(jogo)
        self.nomes = [nome for nome, _ in SKINS]
        self.indice = self.nomes.index(jogo.skin)
        self.imagens = [carregar_imagem("personagem", nome, "parado_1.png") for nome in self.nomes]

    def evento(self, evento):
        if evento.type != pygame.KEYDOWN:
            return
        if evento.key in (pygame.K_LEFT, pygame.K_a):
            self.indice = (self.indice - 1) % len(self.nomes)
            self.jogo.sons.tocar("clique")
        elif evento.key in (pygame.K_RIGHT, pygame.K_d):
            self.indice = (self.indice + 1) % len(self.nomes)
            self.jogo.sons.tocar("clique")
        elif self.confirmou(evento):
            self.jogo.sons.tocar("clique")
            self.jogo.definir_skin(self.nomes[self.indice])
            self.jogo.ir_para_menu()
        elif evento.key == pygame.K_ESCAPE:
            self.jogo.ir_para_menu()

    def desenhar(self, tela):
        ui = self.jogo.interface
        tela.blit(self.jogo.mapas[0].imagem, (0, 0))
        r = ui.painel(tela, 780, 440)
        c = r.centerx
        ui.texto(tela, ui.fonte_grande, "Skins", (c, r.y + 50), VERDE_ESCURO, centro=True, sombra=False)

        for i, imagem in enumerate(self.imagens):
            x = c + (i - (len(self.imagens) - 1) / 2) * 180
            if i == self.indice:
                caixa = pygame.Rect(0, 0, 150, 230)
                caixa.center = (x, r.y + 215)
                pygame.draw.rect(tela, (225, 245, 230), caixa, border_radius=12)
                pygame.draw.rect(tela, VERDE_ESCURO, caixa, 3, border_radius=12)
            tela.blit(imagem, imagem.get_rect(midbottom=(x, r.y + 310)))
            nome = SKINS[i][1]
            cor = VERDE_ESCURO if i == self.indice else PRETO
            ui.texto(tela, ui.fonte_pequena, nome, (x, r.y + 345), cor, centro=True, sombra=False)
            if self.nomes[i] == self.jogo.skin:
                ui.texto(tela, ui.fonte_pequena, "em uso", (x, r.y + 368), VERDE_ESCURO, centro=True, sombra=False)

        ui.texto(tela, ui.fonte_pequena, "Setas para escolher   |   ENTER para usar   |   ESC para voltar",
                 (c, r.bottom - 30), PRETO, centro=True, sombra=False)


class TelaIntroFase(Tela):
    def __init__(self, jogo, indice):
        super().__init__(jogo)
        self.indice = indice
        self.fase = FASES[indice]

    def evento(self, evento):
        if self.confirmou(evento):
            self.jogo.sons.tocar("clique")
            partida = self.jogo.criar_partida_fase(self.indice)
            self.jogo.trocar_tela(TelaJogo(self.jogo, partida))
        elif self.voltou(evento):
            self.jogo.ir_para_menu()

    def desenhar(self, tela):
        ui = self.jogo.interface
        tela.blit(self.jogo.mapas[self.fase.mapa].imagem, (0, 0))
        r = ui.painel(tela, 720, 340)
        c = r.centerx
        ui.texto(tela, ui.fonte_grande, "Nível %d" % (self.indice + 1), (c, r.y + 55), VERDE_ESCURO, centro=True, sombra=False)
        ui.texto(tela, ui.fonte_media, self.fase.nome, (c, r.y + 110), PRETO, centro=True, sombra=False)
        ui.texto(tela, ui.fonte_pequena, "Meta: pegar %d lixos em %d segundos" % (self.fase.meta, TEMPO_FASE),
                 (c, r.y + 160), PRETO, centro=True, sombra=False)
        ui.texto(tela, ui.fonte_pequena, self.fase.dica, (c, r.y + 195), PRETO, centro=True, sombra=False)
        ui.texto(tela, ui.fonte_pequena, "Controles: setas ou A/D para mover e ESPAÇO para pular",
                 (c, r.y + 232), PRETO, centro=True, sombra=False)
        ui.texto(tela, ui.fonte_media, "ENTER para começar", (c, r.bottom - 40), VERDE_ESCURO, centro=True, sombra=False)


class TelaJogo(Tela):
    # Tela em que a partida acontece (serve para os dois modos)
    def __init__(self, jogo, partida):
        super().__init__(jogo)
        self.partida = partida
        self.pausado = False

    def evento(self, evento):
        if evento.type != pygame.KEYDOWN:
            return
        if evento.key == pygame.K_p:
            self.pausado = not self.pausado
        elif evento.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_w):
            if not self.pausado:
                self.partida.pular()
        elif evento.key == pygame.K_ESCAPE:
            self.jogo.ir_para_menu()

    def atualizar(self, dt):
        if self.pausado:
            return
        teclas = pygame.key.get_pressed()
        direcao = 0
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            direcao += 1
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            direcao -= 1
        self.partida.atualizar(dt, direcao)
        if self.partida.terminou:
            self.jogo.fim_da_partida(self.partida)

    def desenhar(self, tela):
        self.partida.desenhar(tela)
        if self.pausado:
            ui = self.jogo.interface
            r = ui.painel(tela, 480, 200)
            ui.texto(tela, ui.fonte_grande, "Pausado", (r.centerx, r.y + 70), VERDE_ESCURO, centro=True, sombra=False)
            ui.texto(tela, ui.fonte_pequena, "P para continuar   |   ESC para o menu",
                     (r.centerx, r.y + 140), PRETO, centro=True, sombra=False)


class TelaResultadoFase(Tela):
    def __init__(self, jogo, partida):
        super().__init__(jogo)
        self.partida = partida

    def evento(self, evento):
        if self.confirmou(evento):
            self.jogo.sons.tocar("clique")
            if not self.partida.venceu:
                self.jogo.trocar_tela(TelaIntroFase(self.jogo, self.partida.indice))
            elif self.partida.indice + 1 < len(FASES):
                self.jogo.trocar_tela(TelaIntroFase(self.jogo, self.partida.indice + 1))
            else:
                self.jogo.trocar_tela(TelaFinal(self.jogo))
        elif self.voltou(evento):
            self.jogo.ir_para_menu()

    def desenhar(self, tela):
        ui = self.jogo.interface
        p = self.partida
        p.desenhar(tela)
        r = ui.painel(tela, 720, 300)
        c = r.centerx
        if p.venceu:
            sobra = int(p.tempo_restante())
            ui.texto(tela, ui.fonte_grande, "Nível concluído!", (c, r.y + 55), VERDE_ESCURO, centro=True, sombra=False)
            ui.texto(tela, ui.fonte_media, "Você coletou %d lixos com %ds de sobra." % (p.coletados, sobra),
                     (c, r.y + 120), PRETO, centro=True, sombra=False)
            ui.texto(tela, ui.fonte_pequena, "Cada resíduo no lugar certo deixa a cidade mais limpa e sustentável.",
                     (c, r.y + 168), PRETO, centro=True, sombra=False)
            ultimo = p.indice + 1 >= len(FASES)
            mensagem = "ENTER para ver o final" if ultimo else "ENTER para o próximo nível"
            ui.texto(tela, ui.fonte_media, mensagem, (c, r.bottom - 45), VERDE_ESCURO, centro=True, sombra=False)
        else:
            ui.texto(tela, ui.fonte_grande, "O tempo acabou!", (c, r.y + 55), VERMELHO, centro=True, sombra=False)
            ui.texto(tela, ui.fonte_media, "Você pegou %d de %d lixos." % (p.coletados, p.fase.meta),
                     (c, r.y + 120), PRETO, centro=True, sombra=False)
            ui.texto(tela, ui.fonte_pequena, "Tente de novo: a cidade conta com você!",
                     (c, r.y + 168), PRETO, centro=True, sombra=False)
            ui.texto(tela, ui.fonte_media, "ENTER para tentar novamente", (c, r.bottom - 45), VERDE_ESCURO, centro=True, sombra=False)


class TelaFinal(Tela):
    def evento(self, evento):
        if self.confirmou(evento) or self.voltou(evento):
            self.jogo.sons.tocar("clique")
            self.jogo.ir_para_menu()

    def desenhar(self, tela):
        ui = self.jogo.interface
        tela.blit(self.jogo.mapas[2].imagem, (0, 0))
        r = ui.painel(tela, 780, 420)
        c = r.centerx
        ui.texto(tela, ui.fonte_grande, "Parabéns, herói da cidade!", (c, r.y + 60), VERDE_ESCURO, centro=True, sombra=False)
        linhas = [
            "Você limpou o Derby, o Marco Zero e a Casa da Cultura.",
            "A ODS 11 busca cidades inclusivas, seguras, resilientes e sustentáveis,",
            "com atenção especial à gestão de resíduos e à qualidade do ambiente urbano.",
            "Separar, reciclar e descartar corretamente: todo mundo pode ajudar!",
        ]
        for i, linha in enumerate(linhas):
            ui.texto(tela, ui.fonte_pequena, linha, (c, r.y + 135 + i * 34), PRETO, centro=True, sombra=False)
        self.mini_personagem(tela, c, r.y + 305, 95)
        ui.texto(tela, ui.fonte_media, "ENTER para voltar ao menu", (c, r.bottom - 35), VERDE_ESCURO, centro=True, sombra=False)


class TelaFimInfinito(Tela):
    def __init__(self, jogo, partida):
        super().__init__(jogo)
        self.partida = partida
        self.novo_recorde = partida.pontos > jogo.recorde
        if self.novo_recorde:
            jogo.recorde = partida.pontos
            jogo.salvar_dados()

    def evento(self, evento):
        if self.confirmou(evento):
            self.jogo.sons.tocar("clique")
            self.jogo.iniciar_infinito()
        elif self.voltou(evento):
            self.jogo.ir_para_menu()

    def desenhar(self, tela):
        ui = self.jogo.interface
        p = self.partida
        p.desenhar(tela)
        r = ui.painel(tela, 720, 340)
        c = r.centerx
        ui.texto(tela, ui.fonte_grande, "Fim de jogo", (c, r.y + 55), VERMELHO, centro=True, sombra=False)
        ui.texto(tela, ui.fonte_media, "Pontos: %d" % p.pontos, (c, r.y + 120), PRETO, centro=True, sombra=False)
        if self.novo_recorde:
            ui.texto(tela, ui.fonte_media, "Novo recorde!", (c, r.y + 160), VERDE_ESCURO, centro=True, sombra=False)
        else:
            ui.texto(tela, ui.fonte_pequena, "Recorde: %d" % self.jogo.recorde, (c, r.y + 160), PRETO, centro=True, sombra=False)
        ui.texto(tela, ui.fonte_pequena, "Mapas visitados: %d" % p.mapas_visitados, (c, r.y + 200), PRETO, centro=True, sombra=False)
        ui.texto(tela, ui.fonte_media, "ENTER para jogar de novo", (c, r.bottom - 70), VERDE_ESCURO, centro=True, sombra=False)
        ui.texto(tela, ui.fonte_pequena, "ESC para voltar ao menu", (c, r.bottom - 30), PRETO, centro=True, sombra=False)
