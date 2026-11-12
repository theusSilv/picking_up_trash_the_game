import sys
import traceback

try:
    import pygame  # noqa: F401
except ImportError:
    sys.exit("Este jogo precisa do pygame. Instale com: pip install pygame")

from jogo.jogo import Jogo


def main():
    try:
        Jogo().rodar()
    except Exception:
        # Salva o erro num arquivo, porque no executável não aparece terminal
        erro = traceback.format_exc()
        try:
            with open("erro.txt", "w", encoding="utf-8") as arq:
                arq.write(erro)
        except OSError:
            pass
        print(erro)
        raise


if __name__ == "__main__":
    main()
