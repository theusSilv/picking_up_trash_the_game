import os
import sys

import pygame


def caminho(*partes):
    # Quando o jogo roda como executável, os arquivos ficam em sys._MEIPASS
    if hasattr(sys, "_MEIPASS"):
        base = sys._MEIPASS
    else:
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, *partes)


def carregar_imagem(*partes, transparente=True):
    imagem = pygame.image.load(caminho("assets", "imagens", *partes))
    if transparente:
        return imagem.convert_alpha()
    return imagem.convert()


def caminho_som(nome):
    return caminho("assets", "sons", nome + ".wav")
