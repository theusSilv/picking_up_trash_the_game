# Picking Up Trash! - Requisitos e Regras de Negócio

## Requisitos Funcionais (RF)

Os requisitos funcionais descrevem as ações que o sistema deve realizar.

- **RF01 – Movimentação do personagem:** O jogo deve permitir que o jogador controle a movimentação do personagem para coletar os lixos espalhados pelo cenário.
- **RF02 – Coleta de lixo:** O jogo deve permitir que o personagem colete os resíduos presentes no ambiente e atualize a quantidade de lixo coletado na tela.
- **RF03 – Controle de tempo:** O jogo deve possuir um cronômetro que indique o tempo restante para completar o objetivo de coleta de cada fase.
- **RF04 – Progressão de níveis:** O jogo deve permitir que o jogador avance para novos níveis ao cumprir a meta de coleta de lixo estabelecida em cada fase.
- **RF05 – Modo infinito:** O jogo deve oferecer um modo sem fim de fases, no qual o mapa muda conforme a pontuação do jogador aumenta.
- **RF06 – Efeitos sonoros:** O jogo deve emitir sons ao coletar lixo, ao errar, ao vencer, ao perder e ao trocar de mapa, e permitir silenciar o áudio.
- **RF07 – Recuperação de vidas:** No modo infinito, o jogo deve permitir que o jogador recupere vidas ao coletar corações que caem no cenário.
- **RF08 – Pulo do personagem:** O jogo deve permitir que o personagem pule, tanto parado quanto em movimento, para alcançar os itens mais cedo.
- **RF09 – Menu principal e skins:** O jogo deve ter um menu principal com os modos de jogo e permitir que o jogador escolha a aparência (skin) do personagem, guardando a escolha.
- **RF10 – Companheiro:** O jogo deve exibir um cachorro que acompanha o personagem durante a partida, sem interagir com os itens que caem.

## Requisitos Não Funcionais (RNF)

Os requisitos não funcionais definem características de qualidade e funcionamento do sistema.

- **RNF01 – Desempenho:** O jogo deve executar os movimentos do personagem e as ações de coleta de forma fluida, sem travamentos que prejudiquem a experiência do jogador.
- **RNF02 – Usabilidade:** O jogo deve apresentar comandos simples e objetivos, permitindo que o jogador compreenda facilmente como movimentar o personagem e coletar os resíduos.
- **RNF03 – Interface gráfica:** O jogo deve exibir de forma clara as informações de quantidade de lixo coletado, tempo restante e nível atual.
- **RNF04 – Compatibilidade:** O jogo deve funcionar corretamente no ambiente ou dispositivo para o qual foi desenvolvido, sem comprometer suas funcionalidades principais.
- **RNF05 – Distribuição:** O jogo deve poder ser executado no Windows por meio de um arquivo executável, sem exigir a instalação do Python.

## Regras de Negócio (RN)

As regras de negócio descrevem as normas que o jogo deve seguir.

- **RN01 – Categorização do lixo:** Todo item que cai no cenário deve ser identificado como lixo ou como item que não é lixo (a flor). Cada lixo pertence a uma categoria de material (plástico, metal, vidro, papel ou orgânico). No modo história, ao coletar um lixo o jogo soma 1 ponto ao contador da fase, e ao coletar uma flor retira 1 ponto.
- **RN02 – Dificuldade progressiva:** A velocidade e a quantidade de itens que caem devem aumentar a cada nível e também ao longo do tempo. O lixo que cair no chão sem ser coletado deve desaparecer da tela.
- **RN03 – Aprovação e desbloqueio de fases:** Para desbloquear a fase seguinte, o jogador deve atingir a meta de lixos da fase (20, 30 e 40) dentro do limite de 1 minuto. Se o tempo acabar antes de a meta ser atingida, o jogador deve repetir a mesma fase.
- **RN04 – Feedback imediato ao erro:** Sempre que o jogador coletar um item que não é lixo, o jogo deve exibir um aviso visual rápido ("Não é lixo!") e retirar pontos.
- **RN05 – Pontuação e vidas no modo infinito:** Cada lixo coletado vale 10 pontos. O jogador começa com 5 vidas e perde 1 vida quando coleta uma flor (e também perde 5 pontos) ou quando um lixo cai no chão sem ser coletado. O jogo termina quando as vidas acabam.
- **RN06 – Recuperação de vidas:** No modo infinito, quando o jogador está com menos de 5 vidas, passam a cair corações (com mais frequência quando resta apenas 1 vida). Cada coração coletado devolve 1 vida, até o máximo de 5. O coração que cair no chão desaparece e não tira vida.
- **RN07 – Troca de mapas no modo infinito:** A cada 200 pontos o mapa muda, seguindo a ordem Derby, Marco Zero e Casa da Cultura, e voltando ao primeiro depois do último. A dificuldade continua aumentando com a pontuação.
- **RN08 – Recorde:** O jogo deve guardar a maior pontuação do modo infinito no computador do jogador e mostrá-la no menu e durante a partida.
