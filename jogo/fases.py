# Fases do modo história. Cada fase usa um mapa (indice na lista de mapas).

class Fase:
    def __init__(self, nome, mapa, meta, vel_minima, vel_maxima, intervalo,
                 chance_flor, balanca, vel_jogador, dica):
        self.nome = nome
        self.mapa = mapa
        self.meta = meta                  # lixos para passar de fase
        self.vel_minima = vel_minima      # velocidade de queda (pixels por segundo)
        self.vel_maxima = vel_maxima
        self.intervalo = intervalo        # segundos entre um item e outro
        self.chance_flor = chance_flor    # chance de cair uma flor (não é lixo)
        self.balanca = balanca            # itens balançando de lado
        self.vel_jogador = vel_jogador
        self.dica = dica


FASES = [
    Fase("Derby", 0, 20, 260, 360, 0.84, 0.10, False, 640,
         "Pegue o lixo antes que ele suje o parque!"),
    Fase("Marco Zero", 1, 30, 320, 450, 0.66, 0.20, False, 740,
         "O centro está movimentado: mais lixo, mais rápido!"),
    Fase("Casa da Cultura", 2, 40, 400, 590, 0.48, 0.28, True, 820,
         "Frenesi total! Os itens balançam e aceleram com o tempo."),
]
