#Mudar a cor da roupa do personagem principal

import os

import numpy as np
from PIL import Image

PASTA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "imagens", "personagem")

# quanto o tom do moletom gira em relação ao vermelho (escala de 0 a 255)
SKINS = {"azul": 150, "verde": 88, "amarelo": 36}


def recolorir(imagem, deslocamento):
    alfa = np.array(imagem)[..., 3]
    hsv = np.array(imagem.convert("RGB").convert("HSV")).astype(int)
    tom, saturacao, brilho = hsv[..., 0], hsv[..., 1], hsv[..., 2]
    moletom = ((tom >= 243) | (tom <= 6)) & (saturacao >= 60) & (brilho >= 40) & (alfa > 0)
    hsv[..., 0] = np.where(moletom, (tom + deslocamento) % 256, tom)
    rgb = Image.fromarray(hsv.astype(np.uint8), "HSV").convert("RGB")
    return Image.fromarray(np.dstack([np.array(rgb), alfa]), "RGBA")


def main():
    origem = os.path.join(PASTA, "vermelho")
    for nome, deslocamento in SKINS.items():
        destino = os.path.join(PASTA, nome)
        os.makedirs(destino, exist_ok=True)
        for arquivo in os.listdir(origem):
            imagem = Image.open(os.path.join(origem, arquivo)).convert("RGBA")
            recolorir(imagem, deslocamento).save(os.path.join(destino, arquivo))
        print("skin gerada:", nome)


if __name__ == "__main__":
    main()
