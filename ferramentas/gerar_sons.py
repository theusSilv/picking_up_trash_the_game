#Gera os sons do jogo estilo 8 bits na pasta assets/sons.
import math
import os
import struct
import wave

PASTA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "sons")
TAXA = 22050


def onda(tipo, fase):
    # fase vai de 0 a 1
    if tipo == "quadrada":
        return 1.0 if fase < 0.5 else -1.0
    if tipo == "triangular":
        return 4 * abs(fase - 0.5) - 1
    if tipo == "serra":
        return 2 * fase - 1
    return math.sin(2 * math.pi * fase)


def nota(freq, duracao, tipo="quadrada", volume=0.4, freq_final=None, taxa=TAXA):
    total = int(taxa * duracao)
    amostras = []
    fase = 0.0
    for i in range(total):
        f = freq if freq_final is None else freq + (freq_final - freq) * i / total
        fase = (fase + f / taxa) % 1.0
        ataque = min(1.0, i / (0.005 * taxa))
        queda = (1 - i / total) ** 0.7
        amostras.append(onda(tipo, fase) * volume * ataque * queda)
    return amostras


def juntar(*partes):
    resultado = []
    for p in partes:
        resultado.extend(p)
    return resultado


def salvar(nome, amostras, taxa=TAXA):
    os.makedirs(PASTA, exist_ok=True)
    caminho = os.path.join(PASTA, nome + ".wav")
    with wave.open(caminho, "wb") as arq:
        arq.setnchannels(1)
        arq.setsampwidth(2)
        arq.setframerate(taxa)
        dados = b""
        for a in amostras:
            a = max(-1.0, min(1.0, a))
            dados += struct.pack("<h", int(a * 32767))
        arq.writeframes(dados)
    print("gerado:", caminho)


def musica():
    taxa = 11025
    bpm = 130
    tempo = 60 / bpm
    # um acorde por compasso: (baixo, nota1, nota2, nota3)
    acordes = [
        (130.81, 329.63, 392.00, 523.25),   # C
        (110.00, 261.63, 329.63, 440.00),   # Am
        (87.31, 220.00, 261.63, 349.23),    # F
        (98.00, 246.94, 293.66, 392.00),    # G
    ]
    compassos = acordes * 2
    padrao = [0, 1, 2, 1, 0, 2, 1, 2]
    total = int(taxa * tempo * 4 * len(compassos))
    saida = [0.0] * total

    def misturar(inicio, amostras):
        pos = int(inicio * taxa)
        for i, a in enumerate(amostras):
            if pos + i < total:
                saida[pos + i] += a

    for c, (baixo, n1, n2, n3) in enumerate(compassos):
        comeco = c * tempo * 4
        notas = [n1, n2, n3]
        for beat in (0, 2):
            misturar(comeco + beat * tempo, nota(baixo, tempo * 1.8, "triangular", 0.35, taxa=taxa))
        for k, idx in enumerate(padrao):
            misturar(comeco + k * tempo / 2, nota(notas[idx], tempo / 2 * 0.9, "quadrada", 0.12, taxa=taxa))
    salvar("musica", saida, taxa)


def main():
    salvar("coleta", juntar(nota(880, 0.06, volume=0.3), nota(1320, 0.1, volume=0.3)))
    salvar("erro", nota(220, 0.28, "serra", 0.35, freq_final=110))
    salvar("vida", juntar(nota(330, 0.12, volume=0.3), nota(165, 0.22, volume=0.3)))
    salvar("coracao", juntar(nota(523, 0.07, volume=0.3), nota(659, 0.07, volume=0.3),
                             nota(784, 0.07, volume=0.3), nota(1047, 0.2, volume=0.3)))
    salvar("pulo", nota(300, 0.16, volume=0.3, freq_final=700))
    salvar("clique", nota(660, 0.05, volume=0.25))
    salvar("mapa", nota(400, 0.4, "triangular", 0.45, freq_final=1000))
    salvar("vitoria", juntar(nota(523, 0.12), nota(659, 0.12), nota(784, 0.12), nota(1047, 0.35)))
    salvar("derrota", juntar(nota(392, 0.18, "triangular", 0.5), nota(330, 0.18, "triangular", 0.5),
                             nota(262, 0.18, "triangular", 0.5), nota(196, 0.45, "triangular", 0.5)))
    salvar("fim_de_jogo", juntar(nota(440, 0.2, "triangular", 0.5), nota(349, 0.2, "triangular", 0.5),
                                 nota(262, 0.2, "triangular", 0.5), nota(196, 0.55, "triangular", 0.5)))
    musica()


if __name__ == "__main__":
    main()
