# Picking Up Trash!

Jogo 2D feito com pygame sobre a ODS 11 (Cidades e Comunidades Sustentáveis).
O personagem precisa pegar o lixo que cai antes que ele suje a cidade, mas não pode pegar as flores.

## Modos de jogo

- **Modo história:** três fases (Derby, Marco Zero e Casa da Cultura). Em cada uma é preciso pegar uma meta de lixos (20, 30 e 40) em 1 minuto.
- **Modo infinito:** o jogo não acaba até as 5 vidas terminarem. A cada 200 pontos o mapa muda e a dificuldade aumenta. Quando falta vida, caem corações: pegue-os para recuperar uma vida.

- **Cachorro:** um cachorro acompanha o personagem durante o jogo. Ele só faz companhia: não pega nem esbarra nos itens.
- **Skins:** no menu, a opção Skins deixa escolher a cor do moletom do personagem (a escolha fica salva).

## Controles

| Tecla | Ação |
|---|---|
| Setas ou A / D | mover o personagem |
| ESPAÇO, seta para cima ou W | pular |
| Setas ou W / S | escolher opção no menu |
| ENTER ou ESPAÇO | confirmar |
| P | pausar |
| M | ligar/desligar o som |
| - e + | volume |
| F3 | mostrar o FPS |
| ESC | voltar ao menu |

## Como rodar

1. Instale o Python 3.
2. Instale o pygame: `pip install -r requirements.txt`
3. Execute: `python main.py`

## Como gerar o executável (Windows)

Dê dois cliques no arquivo `build.bat` ou rode no terminal:

```
python -m pip install -r requirements.txt pyinstaller
python -m PyInstaller --noconfirm --clean --onefile --windowed --name PickingUpTrash --add-data "assets;assets" main.py
```

O jogo vai ficar em `dist/PickingUpTrash.exe`. Se algum antivírus reclamar, é comum com executáveis feitos pelo PyInstaller.
Se o jogo fechar sozinho, procure o arquivo `erro.txt` na mesma pasta do executável.

## Organização das pastas

```
main.py            ponto de partida do jogo
jogo/              código do jogo
  config.py        constantes (tamanho da tela, cores, regras)
  jogo.py          classe Jogo (laço principal e troca de telas)
  telas.py         telas: menu, introdução, partida, resultados
  partida.py       regras das partidas (PartidaFase e PartidaInfinita)
  jogador.py       personagem
  cachorro.py      cachorro que acompanha o personagem
  item.py          itens que caem (lixo e flor)
  fases.py         configuração das fases
  mapas.py         mapas (imagens de fundo)
  interface.py     textos, painéis e barra do topo
  sons.py          efeitos sonoros e música
  dados.py         recorde e skin escolhida (salvos no computador)
  recursos.py      carrega arquivos (funciona também no executável)
assets/            imagens e sons
ferramentas/       gerar_sons.py (cria os sons 8 bits) e gerar_skins.py (cores do personagem)
docs/              requisitos e regras de negócio
```
