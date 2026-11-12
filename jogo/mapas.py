from jogo.recursos import carregar_imagem


class Mapa:
    def __init__(self, nome, arquivo):
        self.nome = nome
        self.imagem = carregar_imagem("fundos", arquivo, transparente=False)


def carregar_mapas():
    return [
        Mapa("Derby", "fase1.jpg"),
        Mapa("Marco Zero", "fase2.jpg"),
        Mapa("Casa da Cultura", "fase3.jpg"),
    ]
