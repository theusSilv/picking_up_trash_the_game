import pygame

from jogo.recursos import caminho_som

NOMES = ["coleta", "erro", "vida", "coracao", "pulo", "clique", "mapa", "vitoria", "derrota", "fim_de_jogo"]


class Sons:
    def __init__(self):
        self.efeitos = {}
        self.funcionando = False
        self.mudo = False
        self.volume = 0.6

        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            for nome in NOMES:
                self.efeitos[nome] = pygame.mixer.Sound(caminho_som(nome))
            self.funcionando = True
        except (pygame.error, FileNotFoundError):
            # sem placa de som ou arquivo faltando: o jogo segue sem áudio
            self.funcionando = False
        self.aplicar_volume()

    def aplicar_volume(self):
        if not self.funcionando:
            return
        volume = 0 if self.mudo else self.volume
        for som in self.efeitos.values():
            som.set_volume(volume)
        pygame.mixer.music.set_volume(volume * 0.5)

    def tocar(self, nome):
        if self.funcionando and nome in self.efeitos:
            self.efeitos[nome].play()

    def iniciar_musica(self):
        if not self.funcionando:
            return
        try:
            pygame.mixer.music.load(caminho_som("musica"))
            pygame.mixer.music.play(-1)
            self.aplicar_volume()
        except (pygame.error, FileNotFoundError):
            pass

    def alternar_mudo(self):
        self.mudo = not self.mudo
        self.aplicar_volume()

    def mudar_volume(self, valor):
        self.volume = max(0.0, min(1.0, self.volume + valor))
        self.aplicar_volume()
