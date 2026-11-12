import json
import os

# Recorde e skin escolhida ficam salvos na pasta do usuário
ARQUIVO = os.path.join(os.path.expanduser("~"), ".picking_up_trash.json")


def carregar():
    try:
        with open(ARQUIVO, encoding="utf-8") as arq:
            dados = json.load(arq)
        if isinstance(dados, dict):
            return dados
    except (OSError, ValueError):
        pass
    return {}


def salvar(dados):
    try:
        with open(ARQUIVO, "w", encoding="utf-8") as arq:
            json.dump(dados, arq)
    except OSError:
        pass
