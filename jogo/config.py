# Configurações gerais do jogo

TITULO = "Picking Up Trash!"
LARGURA = 1280
ALTURA = 720
FPS = 60

# Modo história
TEMPO_FASE = 60          # segundos por fase

# Posição dos pés do personagem (fica dentro da faixa de chão dos mapas)
Y_CHAO = ALTURA - 36

# Pulo do personagem
PULO_VELOCIDADE = 900    # pixels por segundo (para cima)
GRAVIDADE = 2600         # pixels por segundo ao quadrado

# Modo infinito
VIDAS_INFINITO = 5
PONTOS_POR_LIXO = 10
PONTOS_POR_FLOR = 5      # pontos perdidos ao pegar uma flor
PONTOS_POR_MAPA = 200    # a cada tantos pontos o mapa muda

# Skins do personagem: (pasta, nome na tela)
SKINS = [
    ("vermelho", "Vermelho"),
    ("azul", "Azul"),
    ("verde", "Verde"),
    ("amarelo", "Amarelo"),
]

# Cores
BRANCO = (255, 255, 255)
PRETO = (20, 20, 30)
VERDE = (60, 180, 90)
VERDE_ESCURO = (30, 120, 60)
VERMELHO = (220, 60, 60)
AMARELO = (255, 215, 70)
