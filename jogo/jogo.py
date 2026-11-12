import pygame

from jogo import dados
from jogo.config import ALTURA, FPS, LARGURA, SKINS, TITULO
from jogo.interface import Interface
from jogo.mapas import carregar_mapas
from jogo.partida import PartidaFase, PartidaInfinita
from jogo.recursos import carregar_imagem
from jogo.sons import Sons
from jogo.telas import TelaFimInfinito, TelaJogo, TelaMenu, TelaIntroFase, TelaResultadoFase


def criar_janela():
    # Janela que se ajusta ao tamanho da tela (pygame 2). Se não der, usa a simples.
    flags = getattr(pygame, "SCALED", 0) | getattr(pygame, "RESIZABLE", 0)
    try:
        return pygame.display.set_mode((LARGURA, ALTURA), flags, vsync=1)
    except Exception:
        pass
    try:
        return pygame.display.set_mode((LARGURA, ALTURA), flags)
    except Exception:
        return pygame.display.set_mode((LARGURA, ALTURA))


class Jogo:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITULO)
        self.janela = criar_janela()
        self.relogio = pygame.time.Clock()

        self.interface = Interface()
        self.sons = Sons()
        self.mapas = carregar_mapas()
        self.imagens_lixo = [carregar_imagem("itens", "lixo_%02d.png" % i) for i in range(16)]
        self.imagem_flor = carregar_imagem("itens", "flor.png")
        self.imagem_coracao = carregar_imagem("itens", "coracao.png")
        self.fundo_menu = carregar_imagem("fundos", "menu.jpg", transparente=False)

        salvo = dados.carregar()
        self.recorde = int(salvo.get("recorde", 0))
        self.skin = salvo.get("skin", "vermelho")
        if self.skin not in [nome for nome, _ in SKINS]:
            self.skin = "vermelho"
        self.imagem_menu = self.carregar_imagem_menu()

        self.mostrar_fps = False
        self.rodando = True
        self.tela = TelaMenu(self)
        self.sons.iniciar_musica()

    def carregar_imagem_menu(self):
        return carregar_imagem("personagem", self.skin, "parado_1.png")

    def definir_skin(self, nome):
        self.skin = nome
        self.imagem_menu = self.carregar_imagem_menu()
        self.salvar_dados()

    def salvar_dados(self):
        dados.salvar({"recorde": self.recorde, "skin": self.skin})

    # troca de telas
    def trocar_tela(self, tela):
        self.tela = tela

    def ir_para_menu(self):
        self.trocar_tela(TelaMenu(self))

    def iniciar_fases(self):
        self.trocar_tela(TelaIntroFase(self, 0))

    def criar_partida_fase(self, indice):
        return PartidaFase(self, indice)

    def iniciar_infinito(self):
        self.trocar_tela(TelaJogo(self, PartidaInfinita(self)))

    def fim_da_partida(self, partida):
        if isinstance(partida, PartidaFase):
            self.sons.tocar("vitoria" if partida.venceu else "derrota")
            self.trocar_tela(TelaResultadoFase(self, partida))
        else:
            self.sons.tocar("fim_de_jogo")
            self.trocar_tela(TelaFimInfinito(self, partida))

    # teclas que valem em qualquer tela
    def tecla_global(self, tecla):
        if tecla == pygame.K_F3:
            self.mostrar_fps = not self.mostrar_fps
        elif tecla == pygame.K_m:
            self.sons.alternar_mudo()
        elif tecla in (pygame.K_MINUS, pygame.K_KP_MINUS):
            self.sons.mudar_volume(-0.1)
        elif tecla in (pygame.K_EQUALS, pygame.K_PLUS, pygame.K_KP_PLUS):
            self.sons.mudar_volume(0.1)
        else:
            return False
        return True

    def rodar(self):
        while self.rodando:
            dt = min(self.relogio.tick(FPS) / 1000.0, 0.05)

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.rodando = False
                elif evento.type == pygame.KEYDOWN and self.tecla_global(evento.key):
                    continue
                else:
                    self.tela.evento(evento)

            self.tela.atualizar(dt)
            self.tela.desenhar(self.janela)

            if self.mostrar_fps:
                self.interface.texto(self.janela, self.interface.fonte_pequena,
                                     "%d FPS" % self.relogio.get_fps(), (10, ALTURA - 28))
            pygame.display.flip()

        pygame.quit()
