import pygame
from personagens import *
import random
from time import sleep


def mostrar_vida(personagem, posicaox, posicaoy, dif_head_x, dif_head_y):
    """+Função+
    - Destinada a mostrar um pequeno indicador de vida/mana de um personagem, mostrando na tela, uma barra vermelha
    indicando a vida, e uma barra azul, indicando a mana restante

    personagem = mostra qual o personagem que terá a vida exibida
    posicaox = posição X na qual o indicador estará
    posicaoy = posição Y na qual o indicador estará
    dif_head_x = Diferença na posição X para que a cabeça do personagem fique alinhado ao circulo azul
    dif_head_y = Diferença na posição Y para que a cabeça do personagem fique alinhado ao circulo azul"""

    # Globais
    global janela

    # Fontes
    vida_fonte = pygame.font.Font('alagard.ttf', 28)
    mana_fonte = pygame.font.Font('alagard.ttf', 22)

    # Carregar Vida
    vida_texto = vida_fonte.render(f'{personagem.vida_atual:.0f}/{personagem.vida_max:.0f}', False, (0, 0, 0)) \
        .convert_alpha()
    mana_texto = mana_fonte.render(f'{personagem.mana_atual:.0f}/{personagem.mana_max:.0f}', False, (0, 0, 120)) \
        .convert_alpha()

    # Tamanho Cabeças
    tam_cabeca_vida = (120, 120)

    # Wizard cabeçudo / Diminuir tamanho da cabeça
    if personagem.nome == "Wizard":
        tam_cabeca_vida = (100, 100)

    # Cabeça
    head = pygame.transform.scale(personagem.image_face, tam_cabeca_vida).convert_alpha()

    # Tamanho Vida
    tam_vida = (207, 214)
    tam_barras = (208, 214)
    tam_barras_mana = (208, 215)

    # Sprite base vida
    vida_base = pygame.transform.scale(pygame.image.load('barras_vida/Vida_Base.png'), tam_vida).convert_alpha()

    # Sprite barras de vida
    barras_vida = []

    if personagem.envenenado[0]:
        for vida_index in range(10, 110, 10):
            barras_vida.append(pygame.transform.scale(pygame.image.load(f'barras_vida/veneno/{vida_index}.png'),
                                                      tam_barras).convert_alpha())

    else:
        for vida_index in range(10, 110, 10):
            barras_vida.append(pygame.transform.scale(pygame.image.load(f'barras_vida/{vida_index}.png'), tam_barras)
                               .convert_alpha())

    # Sprite mana
    mana = pygame.transform.scale(pygame.image.load('barras_mana/barra_EP.png'), tam_barras_mana).convert_alpha()

    # Mostrar base vida na tela
    janela.blit(vida_base, (posicaox, posicaoy))

    if personagem.vida_atual > 0:
        janela.blit(barras_vida[0], (posicaox - 27, posicaoy - 21))

    # Automatização do sistema para mostrar a vida dos personagens na tela
    posicao_barra = 14
    porcentagem_barra = 80

    for index in range(1, 11):
        if personagem.vida_atual >= personagem.vida_max - (personagem.vida_max * (porcentagem_barra / 100)):
            janela.blit(barras_vida[index], (posicaox - posicao_barra, posicaoy - 21))

        posicao_barra -= 13
        porcentagem_barra -= 10

    # Mana

    # Automatização do sistema para mostrar a Mana dos personagens na tela
    posicao_barra_mana = 26
    porcentagem_barra_mana = 90

    for index in range(1, 10):

        if personagem.mana_atual >= personagem.mana_max - (personagem.mana_max * (porcentagem_barra_mana / 100)):
            janela.blit(mana, (posicaox - posicao_barra_mana, posicaoy + 13))

        posicao_barra_mana -= 13
        porcentagem_barra_mana -= 10

    # Mostrar cabeças na barra de vida
    janela.blit(head, (posicaox - dif_head_x, posicaoy + dif_head_y))

    # Mostrar vida em texto
    janela.blit(vida_texto, (posicaox + 211, posicaoy + 80))

    # Mostrar mana em texto
    janela.blit(mana_texto, (posicaox + 210, posicaoy + 112))


def verificar_resultado_player(player, enemies):
    """+Função+
    - Destinada para verificar se todos os personagens do jogador ou do inimigos estão derrotados, se todos os
    personagens do jogador morrer, retornar "derrota", caso o contrário, retornar "vitória", e por ultimo, caso nem o
    jogador nem o inimigo tiverem todos os personagens derrotados, retornar "andamento" para que o jogo prossiga"""
    # Guardar quantos personagens que estão derrotados
    derrotados_player = 0
    derrotados_enemy = 0

    # Personagens do player derrotados
    for character_player in player:
        if character_player.derrotado:
            derrotados_player += 1

    # Personagens do inimigo derrotados
    for character in enemies:
        if character.derrotado:
            derrotados_enemy += 1

    # Verificar derrota
    if derrotados_player == 3:
        return "derrota"
    elif derrotados_enemy == len(enemies):
        return "vitoria"
    else:
        return "andamento"


def verificar_morte(personagem_selecionado):
    """+Função+
    - Destinada para verificar se o "personagem_selecionado" está com a vida zerada, se tiver, determinar o personagem
    como derrotado e deixar a imagem dele com a opacidade baixa(para sinalizar que o personagem morreu)
    """
    if personagem_selecionado.vida_atual < 0:
        personagem_selecionado.vida_atual = 0

    if personagem_selecionado.vida_atual > personagem_selecionado.vida_max:
        personagem_selecionado.vida_atual = personagem_selecionado.vida_max

    if personagem_selecionado.vida_atual == 0:
        personagem_selecionado.derrotado = True

        personagem_selecionado.image_ingame.set_alpha(45)
        personagem_selecionado.image_face.set_alpha(45)


def turno_selecao(personagem, tipo, todos_p, todos_e, diferenca_h):
    """+Função+
    - Destinada a, após o jogador escolher 'Ataque' ou 'Defesa', Mostrar uma lista com todas as defesas e ataques do
    personagem selecionado.

    personagem = personagem que está sendo selecionado
    tipo = se o jogador selecionou 'Ataque' ou 'Defesa'
    todos_p = lista com todos os personagens do jogador
    todos_e = lista com todos os personagens do jogador
    diferenca_h = diferença da cabeça destinada ao uso do mostrar_vida()
    """
    # Globais
    global ticks
    global delta

    # Sprite base ação do personagem
    base_acoes = pygame.transform.scale(pygame.image.load('batalha/base_acoes.png'), (1025, 1025)).convert_alpha()

    # Sprite cabeça / Mostrar a vez do personagem
    # Wizard Cabeçudo
    if personagem.nome == 'Wizard':
        turno_head = pygame.transform.scale(personagem.image_face, (270, 270)).convert_alpha()
    else:
        turno_head = pygame.transform.scale(personagem.image_face, (320, 320)).convert_alpha()

    # Lista ações
    acoes_texto = []

    # Fonte ações
    acoes_fonte = pygame.font.Font('alagard.ttf', 32)

    # Sprite Seta
    seta_sprite = pygame.transform.scale(pygame.image.load('batalha/seta_selecionado.png'), (100, 100)) \
        .convert_alpha()

    # Qual opção a seta está selecionada
    seta_selecionar = 0

    # Posicoes das setas
    # SETA 0 = (210, 516)
    # SETA 1 = (430, 516)
    # SETA 2 = (210, 555)
    # SETA 3 = (430, 555)
    # SETA 4 = (210, 594)
    # SETA 5 = (430, 594)

    # Posições dos textos
    # ação 0 = (280, 550)
    # ação 1 = (280, 590)
    # ação 2 = (500, 550)
    # ação 3 = (500, 590)
    # ação 4 = (280, 630)
    # ação 5 = (500, 630)

    seta_posicoes = [(210, 516), (430, 516), (210, 555), (430, 555), (210, 594), (430, 594)]
    acao_posicoes = [(280, 550), (500, 550), (280, 590), (500, 590), (280, 630), (500, 630)]

    # Testar o tipo
    quant_acoes = 0

    if tipo == 'ataque':

        for ataque in personagem.ataques:

            if ataque == 'Fogareu' and personagem.mana_atual < 8:
                acoes_texto.append(acoes_fonte.render(f'{ataque}', False, (180, 0, 0)).convert_alpha())

            elif ataque == 'Magico' and personagem.mana_atual < 5:
                acoes_texto.append(acoes_fonte.render(f'{ataque}', False, (180, 0, 0)).convert_alpha())

            elif ataque == 'Atordoar' and personagem.mana_atual < 20:
                acoes_texto.append(acoes_fonte.render(f'{ataque}', False, (180, 0, 0)).convert_alpha())

            else:
                acoes_texto.append(acoes_fonte.render(f'{ataque}', False, (0, 0, 0)).convert_alpha())

        quant_acoes = len(personagem.ataques)

    elif tipo == 'defesa':

        for defesa in personagem.defesas:

            if defesa == "Curar-se" and personagem.mana_atual < 5:
                acoes_texto.append(acoes_fonte.render(f'{defesa}', False, (180, 0, 0)).convert_alpha())

            elif defesa == "Arco vida" and personagem.mana_atual < 8:
                acoes_texto.append(acoes_fonte.render(f'{defesa}', False, (180, 0, 0)).convert_alpha())
            else:
                acoes_texto.append(acoes_fonte.render(f'{defesa}', False, (0, 0, 0)).convert_alpha())

        quant_acoes = len(personagem.defesas)

    # Sons
    confirma_som = pygame.mixer.Sound('sound/confirmar.mp3')
    navegar_menu_som = pygame.mixer.Sound('sound/navegar_menu.mp3')

    turno_selecao_rodando = True
    while turno_selecao_rodando:

        # Mostrar a arena na tela
        mostrar_arena(todos_p, todos_e)

        # Mostrar base do menu de ações
        janela.blit(base_acoes, (0, -18))

        # Cabeça Personagem Jogador
        if personagem.nome == 'Paladin':
            janela.blit(turno_head, (-40, 550))

        elif personagem.nome == 'Wizard':
            janela.blit(turno_head, (25, 565))

        else:
            janela.blit(turno_head, (15, 550))

        # Mostrar todas as ações do jogador
        for acao in range(0, len(acoes_texto)):
            janela.blit(acoes_texto[acao], acao_posicoes[acao])

        # Mostrar seta da ação selecionada
        janela.blit(seta_sprite, seta_posicoes[seta_selecionar])

        # Mostrar vida dos personagens
        mostrar_vida(todos_p[0], 680, 467, diferenca_h[0][0], diferenca_h[0][1])
        mostrar_vida(todos_p[1], 680, 541, diferenca_h[1][0], diferenca_h[1][1])
        mostrar_vida(todos_p[2], 680, 616, diferenca_h[2][0], diferenca_h[2][1])

        # Eventos
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    turno_selecao_rodando = False

                if event.key == pygame.K_DOWN:

                    # Lado Direito
                    if seta_selecionar == 2 and quant_acoes >= 5:
                        navegar_menu_som.play()
                        seta_selecionar = 4

                    if seta_selecionar == 0 and quant_acoes >= 3:
                        navegar_menu_som.play()
                        seta_selecionar = 2

                    # Lado Esquerdo
                    if seta_selecionar == 3 and quant_acoes >= 6:
                        navegar_menu_som.play()
                        seta_selecionar = 5

                    if seta_selecionar == 1 and quant_acoes >= 4:
                        navegar_menu_som.play()
                        seta_selecionar = 3

                if event.key == pygame.K_UP:

                    # Lado Direito
                    if seta_selecionar == 2:
                        navegar_menu_som.play()
                        seta_selecionar = 0

                    if seta_selecionar == 4:
                        navegar_menu_som.play()
                        seta_selecionar = 2

                    # Lado Esquerdo
                    if seta_selecionar == 3:
                        navegar_menu_som.play()
                        seta_selecionar = 1

                    if seta_selecionar == 5:
                        navegar_menu_som.play()
                        seta_selecionar = 3

                if event.key == pygame.K_RIGHT:

                    if seta_selecionar == 4 and quant_acoes >= 6:
                        navegar_menu_som.play()
                        seta_selecionar = 5

                    if seta_selecionar == 2 and quant_acoes >= 4:
                        navegar_menu_som.play()
                        seta_selecionar = 3

                    if seta_selecionar == 0 and quant_acoes >= 2:
                        navegar_menu_som.play()
                        seta_selecionar = 1

                if event.key == pygame.K_LEFT:

                    if seta_selecionar == 5:
                        navegar_menu_som.play()
                        seta_selecionar = 4

                    if seta_selecionar == 3:
                        navegar_menu_som.play()
                        seta_selecionar = 2

                    if seta_selecionar == 1:
                        navegar_menu_som.play()
                        seta_selecionar = 0

                if event.key == pygame.K_RETURN:

                    if tipo == 'ataque':

                        if personagem.ataques[seta_selecionar] == 'Basico':
                            confirma_som.play()
                            turno_fim = ataque_basico(personagem, todos_p, todos_e, diferenca_h)

                        elif personagem.ataques[seta_selecionar] == 'Fogareu':

                            if personagem.mana_atual >= 8:
                                confirma_som.play()
                                turno_fim = ataque_fogareu(personagem, todos_p, todos_e, diferenca_h)
                            else:
                                turno_fim = False

                        elif personagem.ataques[seta_selecionar] == 'Mordida':
                            confirma_som.play()
                            turno_fim = ataque_mordida(personagem, todos_p, todos_e, diferenca_h)

                        elif personagem.ataques[seta_selecionar] == 'Flecha Dupla':
                            confirma_som.play()
                            turno_fim = ataque_flecha_dupla(personagem, todos_p, todos_e, diferenca_h)

                        elif personagem.ataques[seta_selecionar] == 'Adaga':
                            confirma_som.play()
                            turno_fim = ataque_adaga(personagem, todos_p, todos_e, diferenca_h)

                        elif personagem.ataques[seta_selecionar] == 'Magico':

                            if personagem.mana_atual >= 5:
                                confirma_som.play()
                                turno_fim = ataque_magico(personagem, todos_p, todos_e, diferenca_h)

                            else:
                                turno_fim = False

                        elif personagem.ataques[seta_selecionar] == 'Atordoar':

                            if personagem.mana_atual >= 20:
                                confirma_som.play()
                                turno_fim = ataque_atordoar(personagem, todos_p, todos_e, diferenca_h)
                            else:
                                turno_fim = False

                        else:
                            turno_fim = False

                        if turno_fim:
                            return True

                    elif tipo == 'defesa':

                        if personagem.defesas[seta_selecionar] == 'Curar-se':

                            if personagem.mana_atual >= 5:
                                confirma_som.play()
                                turno_fim = cura_basico(personagem, todos_p, todos_e)
                            else:
                                turno_fim = False

                        elif personagem.defesas[seta_selecionar] == 'Arco vida':

                            if personagem.mana_atual >= 8:
                                confirma_som.play()
                                turno_fim = cura_flecha_vida(personagem, todos_p, todos_e, diferenca_h)
                            else:
                                turno_fim = False

                        elif personagem.defesas[seta_selecionar] == "Basico":
                            confirma_som.play()
                            turno_fim = defesa_basico(personagem, todos_p, todos_e)

                        elif personagem.defesas[seta_selecionar] == "Paladino":
                            confirma_som.play()
                            turno_fim = defesa_paladino(personagem, todos_p, todos_e)

                        else:
                            turno_fim = False

                        if turno_fim:
                            return True

        # Atualizar tela
        pygame.display.update()
        delta = ticks.tick(60)


"""ABAIXO TODOS OS ATAQUES/DEFESAS/CURAS"""

"turno_fim = para terminar a rodada caso a ação seja concluida"


def cura_flecha_vida(personagens, todos_player, todos_enemy, diferenca_head):
    resultado = selecionar_personagens_turno(personagens, 1, "player", todos_player, todos_enemy, diferenca_head)

    if resultado[0]:
        personagens.mana_atual -= 8
        turno_fim = calcular_cura(personagens, resultado[1], todos_player, todos_enemy, 'dificil')
    else:
        turno_fim = False

    return turno_fim


def cura_basico(personagens, todos_player, todos_enemy):
    turno_fim = calcular_cura(personagens, 'self', todos_player, todos_enemy, "medio")

    personagens.mana_atual -= 5

    return turno_fim


def ataque_atordoar(personagens, todos_player, todos_enemy, diferenca_head):
    resultado = selecionar_personagens_turno(personagens, 1, "enemy", todos_player, todos_enemy, diferenca_head)

    if resultado[0]:
        personagens.mana_atual -= 20
        turno_fim = calcular_dano(personagens, resultado[1], todos_player, todos_enemy, "dificil", "atordoar")
    else:
        turno_fim = False

    return turno_fim


def ataque_magico(personagens, todos_player, todos_enemy, diferenca_head):
    resultado = selecionar_personagens_turno(personagens, 1, "enemy", todos_player, todos_enemy, diferenca_head)

    if resultado[0]:
        personagens.mana_atual -= 5
        turno_fim = calcular_dano(personagens, resultado[1], todos_player, todos_enemy, "dificil")
    else:
        turno_fim = False

    return turno_fim


def ataque_adaga(personagens, todos_player, todos_enemy, diferenca_head):
    resultado = selecionar_personagens_turno(personagens, 1, "enemy", todos_player, todos_enemy, diferenca_head)

    if resultado[0]:
        turno_fim = calcular_dano(personagens, resultado[1], todos_player, todos_enemy, "dificil", "adaga")
    else:
        turno_fim = False

    return turno_fim


def ataque_flecha_dupla(personagens, todos_player, todos_enemy, diferenca_head):
    resultado = selecionar_personagens_turno(personagens, 2, "enemy", todos_player, todos_enemy, diferenca_head)

    if resultado[0]:
        turno_fim = calcular_dano(personagens, resultado[1], todos_player, todos_enemy, "dificil", "flecha dupla")
    else:
        turno_fim = False

    return turno_fim


def ataque_mordida(personagens, todos_player, todos_enemy, diferenca_head):
    resultado = selecionar_personagens_turno(personagens, 1, "enemy", todos_player, todos_enemy, diferenca_head)

    if resultado[0]:
        turno_fim = calcular_dano(personagens, resultado[1], todos_player, todos_enemy, "dificil", "mordida")
    else:
        turno_fim = False

    return turno_fim


def ataque_fogareu(personagens, todos_player, todos_enemy, diferenca_head):
    resultado = selecionar_personagens_turno(personagens, 1, "enemy", todos_player, todos_enemy, diferenca_head)

    if resultado[0]:
        personagens.mana_atual -= 8
        turno_fim = calcular_dano(personagens, resultado[1], todos_player, todos_enemy, "dificil", 'fogo')
    else:
        turno_fim = False

    return turno_fim


def ataque_basico(personagens, todos_player, todos_enemy, diferenca_head):
    resultado = selecionar_personagens_turno(personagens, 1, "enemy", todos_player, todos_enemy, diferenca_head)

    if resultado[0]:
        turno_fim = calcular_dano(personagens, resultado[1], todos_player, todos_enemy, "facil")
    else:
        turno_fim = False

    return turno_fim


def analisar(personagens, todos_player, todos_enemy, diferenca_head):
    if personagens.nome != "Priest":
        resultado = selecionar_personagens_turno(personagens, 1, "enemy", todos_player, todos_enemy, diferenca_head)
    else:
        resultado = [True, todos_enemy]

    if resultado[0]:
        turno_fim = calcular_dano(personagens, resultado[1], todos_player, todos_enemy, "dificil", "analisar")
    else:
        turno_fim = False

    personagens.mana_atual -= 18

    return turno_fim


def defesa_paladino(personagens, todos_player, todos_enemy):

    turno_fim = calcular_cura(personagens, todos_player, todos_player, todos_enemy, "medio", "defesa paladino")

    return turno_fim


def defesa_basico(personagens, todos_player, todos_enemy):

    turno_fim = calcular_cura(personagens, "self", todos_player, todos_enemy, "medio", "defesa basico")

    return turno_fim


def calcular_cura(curandeiro, alvo, todos_player, todos_enemy, dificuldade, tipo=''):
    """+Função+
    - Destinada para criar um minigame para o jogador, conforme sua perfomance no jogo, calculará a cura/defesa

    obs: essa função também está sendo usada para caso o jogador use uma defesa.

    curandeiro = personagem que realizou a ação
    alvo = lista com todos os alvos OU 'self' para uma cura a si mesmo
    todos_player = lista com todos os personagens do player
    todos_enemy = lista com todos o personagens do inimigo
    dificuldade = dificuldade do minigame
    tipo = o tipo da ação, se é cura ou defesa

    """
    # Globais
    global ticks
    global delta

    # Escuro
    fundo_minigame_cura = pygame.transform.scale(pygame.image.load('transicao/escuro.png'), (1024, 768)).convert_alpha()
    fade_transparencia = 0
    fade_in = True
    controle_travado = True
    fade_out = False

    # Fontes
    cura_taxa_fonte = pygame.font.Font('alagard.ttf', 42)

    # Imagens Atacante e Alvo

    curandeiro_image = pygame.transform.scale(curandeiro.image_ingame, (280, 280)).convert_alpha()
    alvo_image = []

    if alvo == 'self':
        alvo_image = []

    else:

        for pers in alvo:

            if tipo == "defesa paladino":

                if pers.nome != curandeiro.nome:
                    alvo_image.append(pygame.transform.flip(pygame.transform.scale(pers.image_ingame, (280, 280)),
                                                            True, False).convert_alpha())

            else:
                alvo_image.append(pygame.transform.flip(pygame.transform.scale(pers.image_ingame, (280, 280)), True,
                                                        False).convert_alpha())

    # Posição dos alvos
    alvo_pos = []

    if len(alvo_image) == 1:
        alvo_pos = [(780, 460)]

    elif len(alvo_image) == 2:
        alvo_pos = [(730, 380), (800, 485)]

    elif len(alvo_image) == 3:
        alvo_pos = [(725, 290), (805, 385), (725, 480)]

    # Barras de cura
    tam_barras = (1024, 1024)

    facil = pygame.transform.scale(pygame.image.load('barra_dificuldades/cura/facil.png'), tam_barras).convert_alpha()
    medio = pygame.transform.scale(pygame.image.load('barra_dificuldades/cura/medio.png'), tam_barras).convert_alpha()
    dificil = pygame.transform.scale(pygame.image.load('barra_dificuldades/cura/dificil.png'), tam_barras) \
        .convert_alpha()

    slash = pygame.transform.scale(pygame.image.load('barra_dificuldades/slash.png'), tam_barras).convert_alpha()

    # MINIGAME / Adaptar o jogo conforme dificuldades
    quantidade = 0
    velocidade = 0
    base_minigame = 0
    distancia = 0
    tipo_acerto = ''
    acerto_perfeito = 0
    acerto_ok = 0
    acerto_ruim = 0

    if dificuldade == "facil":
        quantidade = random.randint(2, 3)
        velocidade = random.randint(9, 14)
        distancia = random.randint(100, 160)
        base_minigame = facil

        acerto_perfeito = 3
        acerto_ok = 1
        acerto_ruim = -2

    elif dificuldade == 'medio':
        quantidade = random.randint(5, 7)
        velocidade = random.randint(14, 18)
        distancia = random.randint(80, 100)
        base_minigame = medio

        acerto_perfeito = 2
        acerto_ok = -1
        acerto_ruim = -2

    elif dificuldade == 'dificil':
        quantidade = random.randint(7, 12)
        velocidade = random.randint(18, 24)
        distancia = random.randint(50, 80)
        base_minigame = dificil

        acerto_perfeito = 1
        acerto_ok = -3
        acerto_ruim = -4

    # Textos
    tam_textos = (600, 600)
    perfeito = pygame.transform.scale(pygame.image.load('barra_dificuldades/perfeito.png'), tam_textos).convert_alpha()
    ok = pygame.transform.scale(pygame.image.load('barra_dificuldades/ok.png'), tam_textos).convert_alpha()
    ruim = pygame.transform.scale(pygame.image.load('barra_dificuldades/ruim.png'), tam_textos).convert_alpha()

    # Ponto Inicial
    ponto_diferenca = -512
    posicao_slash_x = []

    for ca in range(0, quantidade):
        posicao_slash_x.append(ponto_diferenca)
        ponto_diferenca -= distancia

    # Mostrar tecla para acertar barras
    spacebar = pygame.transform.scale(pygame.image.load('teclas/spacebar.png'), (400, 400)).convert_alpha()

    # Cura taxa
    cura_taxa = 4
    mostrar_cura_taxa = 0

    if tipo == "defesa basico" or tipo == "defesa paladino":
        cura_taxa_max = 32
        cura_taxa_min = 24
        cura_taxa = 8

    else:
        cura_taxa_max = 10
        cura_taxa_min = 4

    # Sons
    magia_sons = []
    for ca in range(1, 8):
        magia_sons.append(pygame.mixer.Sound(f'sound/minigame_cura/spell_0{ca}.ogg'))

    # Minigame
    minigame_time = True
    minigame_finished = [False]
    result_time = False
    dano_calc_rodando = True
    while dano_calc_rodando:

        # Mostrar Arena
        mostrar_arena(todos_player, todos_enemy)

        if not controle_travado:

            if minigame_time:

                minigame_rodando = True
                while minigame_rodando:
                    # Mostrar Arena
                    mostrar_arena(todos_player, todos_enemy)

                    # Escuro / Fundo escurecido
                    janela.blit(fundo_minigame_cura, (0, 0))

                    # Minigame / Base
                    janela.blit(base_minigame, (0, -352))

                    # Mostrar Personagens / Curandeiros / Alvos
                    janela.blit(curandeiro_image, (-5, 460))

                    for ca in range(0, len(alvo_image)):
                        janela.blit(alvo_image[ca], alvo_pos[ca])

                    # Mostrar Barras na tela
                    for valor in posicao_slash_x:
                        janela.blit(slash, (valor, -352))

                    # Mostrar performance ao acertar as barras
                    if tipo_acerto == 'perfeito':
                        janela.blit(perfeito, (210, 105))
                    elif tipo_acerto == 'ok':
                        janela.blit(ok, (210, 100))
                    elif tipo_acerto == 'ruim':
                        janela.blit(ruim, (210, 105))
                    else:
                        janela.blit(spacebar, (300, 180))

                    # Ajustar cura
                    if cura_taxa > cura_taxa_max:
                        cura_taxa = cura_taxa_max
                    if cura_taxa < cura_taxa_min:
                        cura_taxa = cura_taxa_min

                    # Carregar indicador de pontuação do minigame
                    if tipo == "defesa basico" or tipo == "defesa paladino":
                        mostrar_cura_taxa = cura_taxa_fonte.render(f'Defesa Maxima: ~{cura_taxa}%', False,
                                                                   (255, 255, 255)).convert_alpha()
                    else:
                        mostrar_cura_taxa = cura_taxa_fonte.render(f'Cura Maxima: ~{cura_taxa}%', False,
                                                                   (255, 255, 255)).convert_alpha()

                    janela.blit(mostrar_cura_taxa, (325, 690))

                    # Sons espada
                    magia_sons_index = random.randint(0, 6)

                    # Eventos
                    for event in pygame.event.get():

                        if event.type == pygame.QUIT:
                            exit()

                        if event.type == pygame.KEYDOWN:

                            if event.key == pygame.K_SPACE:

                                if len(posicao_slash_x) > 0:

                                    # Avaliar acerto do jogador
                                    if dificuldade == 'facil':

                                        if 240 < posicao_slash_x[0] < 367:
                                            tipo_acerto = 'perfeito'
                                            cura_taxa += acerto_perfeito
                                        elif (-15 < posicao_slash_x[0] < 240) or (368 < posicao_slash_x[0] < 431):
                                            tipo_acerto = 'ok'
                                            cura_taxa += acerto_ok
                                        elif (posicao_slash_x[0] < -16) or (posicao_slash_x[0] > 432):
                                            tipo_acerto = 'ruim'
                                            cura_taxa += acerto_ruim

                                    elif dificuldade == 'medio':

                                        if 312 < posicao_slash_x[0] < 367:
                                            tipo_acerto = 'perfeito'
                                            cura_taxa += acerto_perfeito
                                        elif (81 < posicao_slash_x[0] < 311) or (368 < posicao_slash_x[0] < 431):
                                            tipo_acerto = 'ok'
                                            cura_taxa += acerto_ok
                                        elif (posicao_slash_x[0] < 80) or (posicao_slash_x[0] > 432):
                                            tipo_acerto = 'ruim'
                                            cura_taxa += acerto_ruim

                                    elif dificuldade == 'dificil':

                                        if 336 < posicao_slash_x[0] < 370:
                                            tipo_acerto = 'perfeito'
                                            cura_taxa += acerto_perfeito
                                        elif (271 < posicao_slash_x[0] < 335) or (371 < posicao_slash_x[0] < 431):
                                            tipo_acerto = 'ok'
                                            cura_taxa += acerto_ok
                                        elif (posicao_slash_x[0] < 270) or (posicao_slash_x[0] > 431):
                                            tipo_acerto = 'ruim'
                                            cura_taxa += acerto_ruim

                                    magia_sons[magia_sons_index].play()
                                    posicao_slash_x.pop(0)

                    # Movimentar as barras
                    for valor in range(0, len(posicao_slash_x)):
                        posicao_slash_x[valor] += velocidade

                    # Verificar se a barra passou do ponto
                    if len(posicao_slash_x) > 0:

                        if posicao_slash_x[0] > 510:
                            tipo_acerto = 'ruim'
                            cura_taxa += acerto_ruim
                            posicao_slash_x.pop(0)

                    # Terminar jogo
                    if not minigame_finished[0]:

                        if len(posicao_slash_x) == 0:
                            minigame_finished = [True, 0]

                    else:

                        if minigame_finished[1] != 25:
                            minigame_finished[1] += 1

                        else:
                            minigame_time = False
                            minigame_rodando = False
                            result_time = True

                    pygame.display.update()
                    delta = ticks.tick(60)

            if result_time:

                # Fontes
                cura_fonte = pygame.font.Font('alagard.ttf', 45)

                # Dados
                tick_dados = 0
                dado_mostrando = 0
                dado_running = True
                tam_dados = (200, 200)

                # Carregar Dados
                dado = []
                for ca in range(0, 6):
                    dado.append(pygame.transform.scale(pygame.image.load(f'batalha/dados/cura/{ca}.png'), tam_dados)
                                .convert_alpha())

                # Cura

                # Caso Tipo == Defesa
                defendendo_texto = 0
                defendendo_image = 0
                rodadas_defendendo = 0
                if tipo == "defesa basico" or tipo == "defesa paladino":
                    mostrar_cura = False
                    cura = random.randint(int(curandeiro.defesa * (4 / 100)),
                                          int(curandeiro.defesa * (cura_taxa / 100)))
                    cura_texto = cura_fonte.render(f'+{cura}', False, (255, 255, 255)).convert_alpha()

                    rodadas_defendendo = random.randint(2, 5)
                    defendendo_image = pygame.transform.scale(pygame.image.load('cartas_icon/shield.png'),
                                                              (150, 150)).convert_alpha()

                    defendendo_texto = cura_fonte.render(f"{rodadas_defendendo} rodadas", False, (255, 255, 255))\
                        .convert_alpha()

                # Caso seja apenas cura
                else:

                    mostrar_cura = False
                    if alvo == 'self':
                        cura = random.randint(int(curandeiro.vida_max * (cura_taxa_min / 100)),
                                              int(curandeiro.vida_max * (cura_taxa / 100)))

                    else:
                        cura = random.randint(int(alvo[0].vida_max * (4 / 100)), int(alvo[0].vida_max * (cura_taxa /
                                                                                                         100)))
                    cura_texto = cura_fonte.render(f'+{cura}', False, (255, 255, 255)).convert_alpha()

                # Sons
                dado_som = pygame.mixer.Sound('sound/dados_rolando.mp3')
                dado_som_tocou = False

                terminar_rodada = [False]
                result_rodando = True
                while result_rodando:

                    # Mostrar Arena
                    mostrar_arena(todos_player, todos_enemy)

                    # Escuro
                    janela.blit(fundo_minigame_cura, (0, 0))

                    # Mostrar Cura maxima
                    janela.blit(mostrar_cura_taxa, (325, 690))

                    # Imagem Curandeiro
                    janela.blit(curandeiro_image, (-5, 460))

                    for ca in range(0, len(alvo_image)):
                        janela.blit(alvo_image[ca], alvo_pos[ca])

                    # Dados
                    janela.blit(dado[dado_mostrando], (350, 500))

                    if not dado_som_tocou:
                        dado_som.play()
                        dado_som_tocou = True

                    if tick_dados > 10 and dado_running:

                        if dado_mostrando < 5:
                            dado_mostrando += 1
                        else:

                            dado_mostrando = 0
                            dado_running = False
                            mostrar_cura = True

                        tick_dados = 0

                    tick_dados += 1

                    # Cura
                    if mostrar_cura:
                        janela.blit(cura_texto, (555, 580))

                        if tipo == "defesa basico" or tipo == "defesa paladino":
                            janela.blit(defendendo_texto, (525, 460))
                            janela.blit(defendendo_image, (360, 400))

                        if not terminar_rodada[0]:
                            terminar_rodada = [True, 0]

                    if terminar_rodada[0]:

                        if terminar_rodada[1] < 45:
                            terminar_rodada[1] += 1

                        else:
                            result_rodando = False
                            result_time = False
                            fade_out = True

                    # Eventos
                    for event in pygame.event.get():

                        if event.type == pygame.QUIT:
                            exit()

                    pygame.display.update()
                    delta = ticks.tick(60)

                # Aplicar cura / Defesa extra a todos os alvos
                if tipo == "defesa basico":
                    curandeiro.defesa_extra = [True, cura, rodadas_defendendo]

                elif tipo == "defesa paladino":

                    for pers in alvo:
                        pers.defesa_paladino = [True, cura, rodadas_defendendo]

                else:

                    if alvo == 'self':

                        if curandeiro.vida_atual + cura <= curandeiro.vida_max:
                            curandeiro.vida_atual += cura
                        else:
                            curandeiro.vida_atual = curandeiro.vida_max
                    else:

                        for pers in alvo:

                            if pers.vida_atual + cura <= pers.vida_max:
                                pers.vida_atual += cura
                            else:
                                pers.vida_atual = pers.vida_max

        # Eventos
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                exit()

        # Fade In
        if fade_in:

            if fade_transparencia < 165:
                fade_transparencia += 8
                fundo_minigame_cura.set_alpha(fade_transparencia)

            else:
                fade_in = False
                controle_travado = False

        # Fade Out
        if fade_out:

            if fade_transparencia > 0:
                fade_transparencia -= 8
                fundo_minigame_cura.set_alpha(fade_transparencia)

            else:

                return True

        # Escuro
        janela.blit(fundo_minigame_cura, (0, 0))

        pygame.display.update()
        delta = ticks.tick(60)


def calcular_dano(atacante, alvo, todos_p, todos_e, dificuldade, tipo=''):
    """+Função+
    - Destinada para criar um minigame para o jogador, conforme sua perfomance no jogo, calculará o dano/a analise

    obs: essa função também está sendo usada para caso o jogador use a função analisar.

    atacante = personagem que está atacando
    alvo = lista com todos os alvos
    todos_player = lista com todos os personagens do player
    todos_enemy = lista com todos o personagens do inimigo
    dificuldade = dificuldade do minigame
    tipo = o tipo da ação, se é ataque ou análise

    """
    # Globais
    global ticks
    global delta

    # Fontes
    dano_taxa_fonte = pygame.font.Font('alagard.ttf', 42)

    # Escuro
    fundo_minigame_dano = pygame.transform.scale(pygame.image.load('transicao/escuro.png'), (1024, 768)).convert_alpha()
    fade_transparencia = 0
    fade_in = True
    controle_travado = True
    fade_out = False

    # Imagens Atacante e Alvo
    atacante_image = pygame.transform.scale(atacante.image_ingame, (280, 280)).convert_alpha()
    alvos_image = []
    for pers in alvo:
        alvos_image.append(pygame.transform.scale(pers.image_ingame, (280, 280)).convert_alpha())

    # Posição dos alvos
    alvos_pos = []

    if len(alvos_image) == 1:
        alvos_pos = [(780, 460)]

    elif len(alvos_image) == 2:
        alvos_pos = [(730, 380), (800, 485)]

    elif len(alvos_image) == 3:
        alvos_pos = [(725, 290), (805, 385), (725, 480)]

    # Barra de dano
    tam_barras = (1024, 1024)

    facil = pygame.transform.scale(pygame.image.load('barra_dificuldades/facil.png'), tam_barras).convert_alpha()
    medio = pygame.transform.scale(pygame.image.load('barra_dificuldades/medio.png'), tam_barras).convert_alpha()
    dificil = pygame.transform.scale(pygame.image.load('barra_dificuldades/dificil.png'), tam_barras).convert_alpha()

    slash = pygame.transform.scale(pygame.image.load('barra_dificuldades/slash.png'), tam_barras).convert_alpha()

    # MINIGAME Informações / Adaptar o Jogo conforme dificuldades
    quantidade = 0
    velocidade = 0
    base_minigame = 0
    distancia = 0
    tipo_acerto = ''
    acerto_perfeito = 0
    acerto_ok = 0
    acerto_ruim = 0

    if dificuldade == "facil":
        quantidade = random.randint(2, 3)
        velocidade = random.randint(9, 14)
        distancia = random.randint(100, 160)
        base_minigame = facil

        acerto_perfeito = 8
        acerto_ok = 4
        acerto_ruim = -3

        # Vermelho / menor que -16 / maior que 432
        # amarelo / entre -15 e 240 / entre 368 e 431
        # verde / entre 240 e 367

    elif dificuldade == "medio":
        quantidade = random.randint(5, 7)
        velocidade = random.randint(14, 18)
        distancia = random.randint(80, 100)
        base_minigame = medio

        acerto_perfeito = 4
        acerto_ok = 1
        acerto_ruim = -5

        # Vermelho / menor que 80 / maior que 432
        # Amarelo / entre 81 e 311 / entre 376 e 431
        # Verde / entre 312 e 375

    elif dificuldade == "dificil":
        quantidade = random.randint(7, 12)
        velocidade = random.randint(18, 24)
        distancia = random.randint(50, 80)
        base_minigame = dificil

        acerto_perfeito = 2
        acerto_ok = -2
        acerto_ruim = -7

        # Vermelho / menor que 270 / maior que 432
        # Amarelo / entre 271 e 336 / entre 368 e 431
        # Verde / entre 272 e 335

    # Textos
    tam_textos = (600, 600)
    perfeito = pygame.transform.scale(pygame.image.load('barra_dificuldades/perfeito.png'), tam_textos).convert_alpha()
    ok = pygame.transform.scale(pygame.image.load('barra_dificuldades/ok.png'), tam_textos).convert_alpha()
    ruim = pygame.transform.scale(pygame.image.load('barra_dificuldades/ruim.png'), tam_textos).convert_alpha()

    # Ponto inicial
    ponto_diferenca = -512
    posicao_slash_x = []

    for ca in range(0, quantidade):
        posicao_slash_x.append(ponto_diferenca)
        ponto_diferenca -= distancia

    # Mostrar tecla para acertar barras
    spacebar = pygame.transform.scale(pygame.image.load('teclas/spacebar.png'), (400, 400)).convert_alpha()

    # Taxa dano
    mostrar_dano_taxa = 0

    if dificuldade == "facil":
        dano_taxa_min = 15
        dano_taxa_max = 65
        dano_taxa = 35
    else:
        dano_taxa_min = 25
        dano_taxa_max = 100
        dano_taxa = 50

    # Sons
    espada_sons = []
    for ca in range(1, 11):
        espada_sons.append(pygame.mixer.Sound(f'sound/minigame/sword.{ca}.ogg'))

    minigame_time = True
    minigame_finished = [False]
    result_time = False
    dano_calc_rodando = True
    while dano_calc_rodando:

        # Mostrar Arena
        mostrar_arena(todos_p, todos_e)

        if not controle_travado:

            if minigame_time:

                # MINIGAME decidir o dano
                minigame_rodando = True
                while minigame_rodando:

                    # Mostrar Arena / Fundo
                    mostrar_arena(todos_p, todos_e)

                    # Escuro / Fundo escurecido
                    janela.blit(fundo_minigame_dano, (0, 0))

                    # Minigame / Base
                    janela.blit(base_minigame, (0, -352))

                    # Mostrar personagens / Atacantes / Alvos
                    janela.blit(atacante_image, (-5, 460))

                    for ca in range(0, len(alvos_image)):
                        janela.blit(alvos_image[ca], alvos_pos[ca])

                    # Mostrar Barras na tela
                    for valor in posicao_slash_x:
                        janela.blit(slash, (valor, -352))

                    # Mostrar performance do jogador nas barras
                    if tipo_acerto == 'perfeito':
                        janela.blit(perfeito, (210, 105))
                    elif tipo_acerto == 'ok':
                        janela.blit(ok, (210, 100))
                    elif tipo_acerto == 'ruim':
                        janela.blit(ruim, (210, 105))
                    elif tipo_acerto == '':
                        janela.blit(spacebar, (300, 180))

                    # Mostrar taxa dano
                    if dano_taxa > dano_taxa_max:
                        dano_taxa = dano_taxa_max
                    elif dano_taxa < dano_taxa_min:
                        dano_taxa = dano_taxa_min

                    if tipo == "analisar":
                        mostrar_dano_taxa = dano_taxa_fonte.render(f'Valor Maximo: ~{dano_taxa:.0f}%', False,
                                                                   (255, 255, 255)).convert_alpha()
                    else:
                        mostrar_dano_taxa = dano_taxa_fonte.render(f'Dano Maximo: ~{dano_taxa:.0f}%', False,
                                                                   (255, 255, 255)).convert_alpha()

                    janela.blit(mostrar_dano_taxa, (325, 690))

                    # Som
                    espada_som_index = random.randint(0, 9)

                    # Eventos
                    for event in pygame.event.get():

                        if event.type == pygame.QUIT:
                            exit()

                        if event.type == pygame.KEYDOWN:

                            # Confirmar acerto Barra
                            if event.key == pygame.K_SPACE:

                                if len(posicao_slash_x) > 0:

                                    # Avaliar Acerto Jogador
                                    if dificuldade == 'facil':

                                        if 240 < posicao_slash_x[0] < 367:
                                            tipo_acerto = 'perfeito'
                                            dano_taxa += acerto_perfeito
                                        elif (-15 < posicao_slash_x[0] < 240) or (368 < posicao_slash_x[0] < 431):
                                            tipo_acerto = 'ok'
                                            dano_taxa += acerto_ok
                                        elif (posicao_slash_x[0] < -16) or (posicao_slash_x[0] > 432):
                                            tipo_acerto = 'ruim'
                                            dano_taxa += acerto_ruim

                                    elif dificuldade == 'medio':

                                        if 312 < posicao_slash_x[0] < 367:
                                            tipo_acerto = 'perfeito'
                                            dano_taxa += acerto_perfeito
                                        elif (81 < posicao_slash_x[0] < 311) or (368 < posicao_slash_x[0] < 431):
                                            tipo_acerto = 'ok'
                                            dano_taxa += acerto_ok
                                        elif (posicao_slash_x[0] < 80) or (posicao_slash_x[0] > 432):
                                            tipo_acerto = 'ruim'
                                            dano_taxa += acerto_ruim

                                    elif dificuldade == 'dificil':

                                        if 336 < posicao_slash_x[0] < 370:
                                            tipo_acerto = 'perfeito'
                                            dano_taxa += acerto_perfeito
                                        elif (271 < posicao_slash_x[0] < 335) or (371 < posicao_slash_x[0] < 431):
                                            tipo_acerto = 'ok'
                                            dano_taxa += acerto_ok
                                        elif (270 > posicao_slash_x[0]) or (posicao_slash_x[0] > 432):
                                            tipo_acerto = 'ruim'
                                            dano_taxa += acerto_ruim

                                    posicao_slash_x.pop(0)
                                    espada_sons[espada_som_index].play()

                    # Movimentar Barras
                    for ca in range(0, len(posicao_slash_x)):
                        posicao_slash_x[ca] += velocidade

                    # Testar se a barra passou do ponto
                    if len(posicao_slash_x) > 0:

                        if posicao_slash_x[0] > 510:
                            tipo_acerto = 'ruim'
                            dano_taxa += acerto_ruim
                            posicao_slash_x.pop(0)

                    # Verificar se terminou o Minigame
                    if not minigame_finished[0]:

                        if len(posicao_slash_x) == 0:
                            minigame_finished = [True, 0]

                    else:

                        if minigame_finished[1] != 25:
                            minigame_finished[1] += 1
                        else:
                            minigame_rodando = False
                            minigame_time = False
                            result_time = True

                    pygame.display.update()
                    delta = ticks.tick(60)

            if result_time:

                # Fontes
                dano_fonte = pygame.font.Font('alagard.ttf', 45)

                # Dados
                tick_dados = 0
                dado_mostrando = 0
                dado_running = True
                tam_dados = (200, 200)

                dados = []
                for ca in range(0, 6):
                    dados.append(pygame.transform.scale(pygame.image.load(f'batalha/dados/{ca}.png'), tam_dados)
                                 .convert_alpha())

                # Dano
                mostrar_dano = False
                if tipo != "analisar":
                    dano = random.randint(int(atacante.ataque * (25 / 100)), int(atacante.ataque * (dano_taxa / 100)))
                else:
                    dano = random.randint(1, 5) + 1
                dano_texto = dano_fonte.render(f'{dano - 1:.0f}', False, (255, 255, 255)).convert_alpha()

                # Fogo
                fogo_texto = 0
                fogo = 0
                fogo_tempo = 0
                if tipo == 'fogo':
                    fogo = pygame.transform.scale(pygame.image.load('efeitos/fogo.png'), (200, 200)).convert_alpha()
                    fogo_tempo = random.randint(2, 4)
                    fogo_texto = dano_fonte.render(f'+{fogo_tempo}', False, (255, 255, 255)).convert_alpha()

                # Roubo de vida / Mordida
                mordida_texto = 0
                mordida = 0
                vida_roubada = 0
                if tipo == 'mordida':
                    mordida = pygame.transform.scale(pygame.image.load('efeitos/mordida.png'), (200, 200)) \
                        .convert_alpha()

                    vida_roubada = int(dano * (random.randint(25, 90) / 100))

                    mordida_texto = dano_fonte.render(f'+{vida_roubada}', False, (255, 255, 255))

                # Atacar dois alvos
                if tipo == 'flecha dupla':
                    dano /= 2
                    dano_texto = dano_fonte.render(f'{dano:.0f} / {dano:.0f}', False, (255, 255, 255)).convert_alpha()

                # Atordoar
                atordoado = 0
                atordoado_texto = 0
                rodadas_atordoado = 0
                if tipo == 'atordoar':
                    rodadas_atordoado = random.randint(1, 2)
                    atordoado_texto = dano_fonte.render(f'+{rodadas_atordoado}', False, (255, 255, 255)).convert_alpha()
                    atordoado = pygame.transform.scale(pygame.image.load('efeitos/atordoado.png'), (200, 200))\
                        .convert_alpha()

                # Som
                dados_som = pygame.mixer.Sound('sound/dados_rolando.mp3')
                dados_som_tocou = False

                terminar_rodada = [False]
                result_rodando = True
                while result_rodando:

                    # Fundo
                    mostrar_arena(todos_p, todos_e)

                    # Fundo escurecido
                    janela.blit(fundo_minigame_dano, (0, 0))

                    # Mostrar taxa do dano
                    janela.blit(mostrar_dano_taxa, (325, 690))

                    # Personagens / Atacante / Alvos
                    janela.blit(atacante_image, (-5, 460))

                    for ca in range(0, len(alvos_image)):
                        janela.blit(alvos_image[ca], alvos_pos[ca])

                    # Dado

                    if not dados_som_tocou:
                        dados_som.play()
                        dados_som_tocou = True

                    janela.blit(dados[dado_mostrando], (350, 500))

                    if tick_dados > 10 and dado_running:

                        if dado_mostrando < 5:
                            dado_mostrando += 1
                        else:
                            dado_mostrando = 0
                            dado_running = False
                            mostrar_dano = True

                        tick_dados = 0

                    tick_dados += 1

                    # Dano
                    if mostrar_dano:
                        janela.blit(dano_texto, (555, 580))

                        if tipo == 'fogo':
                            janela.blit(fogo_texto, (545, 490))
                            janela.blit(fogo, (350, 400))

                        elif tipo == 'mordida':
                            janela.blit(mordida_texto, (545, 490))
                            janela.blit(mordida, (350, 390))

                        elif tipo == "atordoar":
                            janela.blit(atordoado_texto, (545, 480))
                            janela.blit(atordoado, (350, 390))

                        if not terminar_rodada[0]:
                            terminar_rodada = [True, 0]

                    if terminar_rodada[0]:

                        if terminar_rodada[1] < 45:
                            terminar_rodada[1] += 1
                        else:
                            result_rodando = False
                            result_time = False
                            fade_out = True

                    # Eventos
                    for event in pygame.event.get():

                        if event.type == pygame.QUIT:
                            exit()

                    pygame.display.update()
                    delta = ticks.tick(60)

                if tipo != "analisar":

                    for pers in alvo:
                        defesa_extra = 0

                        if pers.defesa_paladino[0]:
                            defesa_extra += pers.defesa_paladino[1]

                        if pers.defesa_extra[0]:
                            defesa_extra += pers.defesa_extra[1]

                        pers.vida_atual -= dano * (50 / (50 + pers.defesa + defesa_extra))

                        if tipo == 'fogo':
                            if not pers.queimando[0]:
                                pers.queimando = [True, fogo_tempo]
                            else:
                                pers.queimando[1] += fogo_tempo

                        if tipo == 'mordida':
                            atacante.vida_atual += vida_roubada

                        if tipo == 'atordoar':
                            pers.atordoado = [True, rodadas_atordoado]

                else:

                    for pers in alvo:
                        pers.revelado = [True, dano]

        # Eventos
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                exit()

        # Fade_in
        if fade_in:

            if fade_transparencia < 165:
                fade_transparencia += 8
                fundo_minigame_dano.set_alpha(fade_transparencia)
            else:
                fade_in = False
                controle_travado = False

        # Fade_Out
        if fade_out:

            if fade_transparencia > 0:
                fade_transparencia -= 8
                fundo_minigame_dano.set_alpha(fade_transparencia)

            else:

                dano_calc_rodando = False

        janela.blit(fundo_minigame_dano, (0, 0))

        pygame.display.update()
        delta = ticks.tick(60)

    return True


def selecionar_personagens_turno(personagens, num_alvos, tipo, personagens_p, personagens_e, difer_head):
    """+Função+
    - Destinada a mostrar um selecionador com todos os personagens(do inimigo ou do proprio player) para que possa
    definir um alvo para alguma ação do jogador, seja ataque, cura, defesa

    num_alvos = quantos alvos serão selecionados
    tipo = qual o tipo
    personagens_p = lista com personagens do player
    personagens_e = lista com personagens do inimigo

    difer_head = diferença na posição da cabeça destinada ao uso do mostrar_vida()
    """
    # Globais
    global ticks
    global delta

    # Fontes
    aviso_fonte = pygame.font.Font('alagard.ttf', 26)

    # Base Selecionar Jogadores / Inimigos
    base_selecao = pygame.transform.scale(pygame.image.load('batalha/base_selecao.png'), (1025, 1025)).convert_alpha()

    # Seleção
    selected = [pygame.transform.scale(pygame.image.load('batalha/selecionar_pers/unselected.png'), (250, 250))
                      .convert_alpha(),

                pygame.transform.scale(pygame.image.load('batalha/selecionar_pers/selected.png'), (250, 250))
                      .convert_alpha()]

    seta_selecao = pygame.transform.scale(pygame.image.load('batalha/selecionar_pers/a_select.png'), (250, 250)) \
        .convert_alpha()

    # Aviso para iniciar a ação
    tecla_confirma = pygame.transform.scale(pygame.image.load('teclas/spacebar.png'), (140, 140)).convert_alpha()
    confirma_texto = aviso_fonte.render("Confirmar", False, (0, 0, 0)).convert_alpha()

    # Sistema de seleção
    selecionado = []
    selecao_posicoes = []
    seta_selecionado = 0

    # Rosto Personagens
    image_face = []
    dif_quad = []

    # Arrumar posições dos quadrados
    if tipo == "enemy":

        if len(personagens_e) == 3:
            selecao_posicoes = [(2, 470), (216, 470), (429, 470)]
            selecionado = [0, 0, 0]

        elif len(personagens_e) == 2:
            selecao_posicoes = [(90, 470), (320, 470)]
            selecionado = [0, 0]

        elif len(personagens_e) == 1:
            selecao_posicoes = [(210, 470)]
            selecionado = [0]

        # Rosto personagem
        for ca in range(0, len(selecionado)):
            image_face.append(pygame.transform.scale(personagens_e[ca].image_face, (150, 150)).convert_alpha())

            # Centralizar rosto no quadrado
            if personagens_e[ca].nome == 'Dark Wizard':
                dif_quad.append((40, 80))
            elif personagens_e[ca].nome == 'Skeleton':
                dif_quad.append((55, 90))
            else:
                dif_quad.append((55, 80))

    elif tipo == "player":

        selecao_posicoes = [(2, 470), (216, 470), (429, 470)]
        selecionado = [0, 0, 0]

        # Rosto personagem
        for ca in range(0, len(selecionado)):
            image_face.append(pygame.transform.scale(personagens_p[ca].image_face, (150, 150)).convert_alpha())

            # Centralizar o rosto no quadrado
            if personagens_p[ca].nome == 'Paladin':
                dif_quad.append((40, 80))
            elif personagens_p[ca].nome == 'Hunter':
                dif_quad.append((60, 80))
            elif personagens_p[ca].nome == 'Wizard':
                dif_quad.append((60, 80))
            else:
                dif_quad.append((55, 80))

    # Sons
    navegar_menu_som = pygame.mixer.Sound('sound/navegar_menu.mp3')
    confirma_som = pygame.mixer.Sound('sound/confirmar.mp3')

    selecionar_personagens_rodando = True
    while selecionar_personagens_rodando:

        # Mostrar Arena
        mostrar_arena(personagens_p, personagens_e)

        # Mostrar Seleção / Base
        janela.blit(base_selecao, (0, -18))

        # Mostrar Quadrados para selecionar + Mostrar cabeças dos alvos
        for ca in range(0, len(selecionado)):
            janela.blit(selected[selecionado[ca]], selecao_posicoes[ca])

            janela.blit(image_face[ca], (selecao_posicoes[ca][0] + dif_quad[ca][0], selecao_posicoes[ca][1] +
                                         dif_quad[ca][1]))

        # Mostrar a seta de seleção
        janela.blit(seta_selecao, selecao_posicoes[seta_selecionado])

        # Mostrar Vida
        mostrar_vida(personagens_p[0], 680, 467, difer_head[0][0], difer_head[0][1])
        mostrar_vida(personagens_p[1], 680, 541, difer_head[1][0], difer_head[1][1])
        mostrar_vida(personagens_p[2], 680, 616, difer_head[2][0], difer_head[2][1])

        # Verificar se o jogador selecionou todos os alvos possíveis
        if num_alvos - selecionado.count(1) != 0:
            liberar_confirma = False

            if num_alvos - selecionado.count(1) == 1:
                aviso_selecao = aviso_fonte.render(f'Selecione mais {num_alvos - selecionado.count(1)} personagem',
                                                   False, (0, 0, 0)).convert_alpha()
            else:
                aviso_selecao = aviso_fonte.render(f'Selecione mais {num_alvos - selecionado.count(1)} personagens',
                                                   False, (0, 0, 0)).convert_alpha()

            janela.blit(aviso_selecao, (160, 720))

        else:
            liberar_confirma = True

            janela.blit(tecla_confirma, (175, 655))
            janela.blit(confirma_texto, (320, 710))

        # Eventos
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RIGHT:

                    if seta_selecionado == 1 and len(selecionado) == 3:
                        navegar_menu_som.play()
                        seta_selecionado += 1

                    if seta_selecionado == 0 and len(selecionado) >= 2:
                        navegar_menu_som.play()
                        seta_selecionado += 1

                if event.key == pygame.K_LEFT:

                    if seta_selecionado == 1:
                        navegar_menu_som.play()
                        seta_selecionado -= 1

                    if seta_selecionado == 2:
                        navegar_menu_som.play()
                        seta_selecionado -= 1

                if event.key == pygame.K_RETURN:

                    if selecionado[seta_selecionado] == 0:

                        if num_alvos - selecionado.count(1) != 0:

                            if tipo == 'enemy' and not personagens_e[seta_selecionado].derrotado:
                                confirma_som.play()
                                selecionado[seta_selecionado] = 1
                            elif tipo == 'player' and not personagens_p[seta_selecionado].derrotado:
                                confirma_som.play()
                                selecionado[seta_selecionado] = 1

                    elif selecionado[seta_selecionado] == 1:

                        confirma_som.play()
                        selecionado[seta_selecionado] = 0

                if event.key == pygame.K_SPACE:

                    if liberar_confirma:

                        pers_escolhidos = []
                        for ca in range(0, len(selecionado)):

                            if selecionado[ca] == 1:

                                if tipo == 'enemy':
                                    pers_escolhidos.append(personagens_e[ca])
                                elif tipo == 'player':
                                    pers_escolhidos.append(personagens_p[ca])

                        return [True, pers_escolhidos]

                if event.key == pygame.K_ESCAPE:
                    return [False]

        pygame.display.update()
        delta = ticks.tick(60)


def mostrar_lista(todos_personagens_player, todos_personagens_enemy):
    """
    +Função+
    - Destinada a mostrar uma lista com todos os personagens numa batalha, mostrando assim todas as cartas de cada um
    se um inimigo estiver 'revelado', assim, o jogo irá mostrar mais informações sobre o personagem
    """
    # Globais
    global ticks
    global delta

    # Sprite cartas
    cartas = pygame.transform.scale(pygame.image.load('personagens/carta.png'), (700, 700)).convert_alpha()

    # Posição carta
    carta_pos_x = [-175, 167, 509]

    # Escuro
    fundo_lista = pygame.transform.scale(pygame.image.load('transicao/escuro.png'), (1024, 768)).convert_alpha()
    fundo_lista.set_alpha(0)

    # Seta Sprite
    tam_seta = (300, 300)

    seta_direita = [pygame.transform.scale(pygame.image.load('selecao_menu/direita_uns.png'), tam_seta)
                          .convert_alpha()]

    seta_esquerda = [pygame.transform.scale(pygame.image.load('selecao_menu/esquerda_uns.png'), tam_seta)
                           .convert_alpha()]

    # Fade
    fade_transparencia = 0
    fade_in = True
    fade_out = False
    controle_travado = True

    # Sprite ícones de atributos do personagem
    heart_lifebar = [pygame.transform.scale(pygame.image.load('cartas_icon/heart.png'), (100, 100)).convert_alpha(),
                     pygame.transform.scale(pygame.image.load('cartas_icon/heart_empty.png'), (100, 100))
                           .convert_alpha()]

    heart_s_lifebar = [pygame.transform.scale(pygame.image.load('cartas_icon/paladin_heart.png'), (100, 100))
                             .convert_alpha(),

                       pygame.transform.scale(pygame.image.load('cartas_icon/paladin_heart_empty.png'), (100, 100))
                             .convert_alpha()]

    heart = [pygame.transform.scale(pygame.image.load('cartas_icon/heart.png'), (50, 50)).convert_alpha(),
             pygame.transform.scale(pygame.image.load('cartas_icon/heart_empty.png'), (50, 50)).convert_alpha()]

    heart_s = [pygame.transform.scale(pygame.image.load('cartas_icon/paladin_heart.png'), (50, 50)).convert_alpha(),
               pygame.transform.scale(pygame.image.load('cartas_icon/paladin_heart_empty.png'), (50, 50))
                     .convert_alpha()]

    mana = [pygame.transform.scale(pygame.image.load('cartas_icon/mana.png'), (40, 40)).convert_alpha(),
            pygame.transform.scale(pygame.image.load('cartas_icon/mana_empty.png'), (40, 40)).convert_alpha()]

    mana_s = [pygame.transform.scale(pygame.image.load('cartas_icon/mana_s.png'), (40, 40)).convert_alpha(),
              pygame.transform.scale(pygame.image.load('cartas_icon/mana_s_empty.png'), (40, 40)).convert_alpha()]

    attack = [pygame.transform.scale(pygame.image.load('cartas_icon/attack.png'), (40, 40)).convert_alpha(),
              pygame.transform.scale(pygame.image.load('cartas_icon/attack_strong.png'), (40, 40)).convert_alpha()]

    defense = [pygame.transform.scale(pygame.image.load('cartas_icon/shield.png'), (40, 40)).convert_alpha(),
               pygame.transform.scale(pygame.image.load('cartas_icon/paladin_shield.png'), (40, 40)).convert_alpha()]

    initiative = [pygame.transform.scale(pygame.image.load('cartas_icon/initiative.png'), (40, 40)).convert_alpha(),
                  pygame.transform.scale(pygame.image.load('cartas_icon/initiative_s.png'), (40, 40)).convert_alpha()]

    # Fontes
    nome_fonte = pygame.font.Font('alagard.ttf', 60)
    alternar_fonte = pygame.font.Font('alagard.ttf', 75)
    vida_fonte = pygame.font.Font('alagard.ttf', 40)
    mana_fonte = pygame.font.Font('alagard.ttf', 28)
    stat_fonte = pygame.font.Font('alagard.ttf', 24)
    misterio_fonte = pygame.font.Font('alagard.ttf', 180)

    # Texto
    inimigos_texto = alternar_fonte.render('Inimigos', False, (255, 255, 255)).convert_alpha()
    herois_texto = alternar_fonte.render('Herois', False, (255, 255, 255)).convert_alpha()

    misterio_texto = misterio_fonte.render('?', False, (0, 0, 0)).convert_alpha()

    # For / Carregar vida(texto)/nome/imagem do player
    player_vida_texto = []
    player_nomes_texto = []
    player_manas_texto = []
    player_imagens_pers = []
    player_vida_stat = []
    player_attack_stat = []
    player_defense_stat = []
    player_mana_stat = []
    player_initiative_stat = []
    player_extradefense_stat = []

    # Menu Mostrando
    tela_atual = 'player'

    for nc in range(0, len(todos_personagens_player)):
        # Carregar nomes / Player
        player_nomes_texto.append(nome_fonte.render(f'{todos_personagens_player[nc].nome}', False, (0, 0, 0))
                                  .convert_alpha())

        # Carregar imagens / Player
        player_imagens_pers.append(pygame.transform.scale(todos_personagens_player[nc].image_ingame, (145, 145))
                                   .convert_alpha())

        # Carregar texto vida (Barra de vida) / Player
        player_vida_texto.append(vida_fonte.render(f'{todos_personagens_player[nc].vida_atual:.0f} / '
                                                   f'{todos_personagens_player[nc].vida_max}', False, (0, 0, 0))
                                 .convert_alpha())

        # Carregar texto mana (Barra de mana)/ Player
        player_manas_texto.append(mana_fonte.render(f'{todos_personagens_player[nc].mana_atual:.0f} / '
                                                    f'{todos_personagens_player[nc].mana_max}', False, (0, 0, 120))
                                  .convert_alpha())

        # Carregar vida stat / Player
        player_vida_stat.append(stat_fonte.render(f'{todos_personagens_player[nc].vida_max}', False, (0, 0, 0))
                                .convert_alpha())

        # Carregar ataque stat / Player
        player_attack_stat.append(stat_fonte.render(f'{todos_personagens_player[nc].ataque}', False, (0, 0, 0))
                                  .convert_alpha())

        # Carregar defesa stat / Player
        player_defense_stat.append(stat_fonte.render(f'{todos_personagens_player[nc].defesa}', False, (0, 0, 0))
                                   .convert_alpha())

        # Carregar defesa extra stat / Player
        soma_defesa_extra = 0
        if todos_personagens_player[nc].defesa_extra[0]:
            soma_defesa_extra += todos_personagens_player[nc].defesa_extra[1]

        if todos_personagens_player[nc].defesa_paladino[0]:
            soma_defesa_extra += todos_personagens_player[nc].defesa_paladino[1]

        player_extradefense_stat.append(stat_fonte.render(f'+{soma_defesa_extra:.0f}', False, (0, 120, 0))
                                        .convert_alpha())

        # Carregar mana stat / Player
        player_mana_stat.append(stat_fonte.render(f'{todos_personagens_player[nc].mana_max}', False, (0, 0, 0))
                                .convert_alpha())

        # Carregar iniciativa stat / Player
        player_initiative_stat.append(stat_fonte.render(f'{todos_personagens_player[nc].iniciativa}', False, (0, 0, 0))
                                      .convert_alpha())

    # Inimigo
    carta_pos_x_e = []

    if len(todos_personagens_enemy) == 3:
        carta_pos_x_e = [-175, 167, 509]
    elif len(todos_personagens_enemy) == 2:
        carta_pos_x_e = [-25, 355]
    elif len(todos_personagens_enemy) == 1:
        carta_pos_x_e = [167]

    enemy_nomes_texto = []
    enemy_vida_texto = []
    enemy_mana_texto = []
    enemy_imagens_pers = []

    enemy_vida_stat = []
    enemy_attack_stat = []
    enemy_defense_stat = []
    enemy_mana_stat = []
    enemy_initiative_stat = []
    enemy_extradefense_stat = []
    enemy_revelado_stat = []
    for ca in range(0, len(todos_personagens_enemy)):
        # Carregar nomes / Enemy
        if todos_personagens_enemy[ca].nome == "Dark Wizard":
            enemy_nomes_texto.append(nome_fonte.render("Wizard", False, (0, 30, 105)).convert_alpha())
        elif todos_personagens_enemy[ca].nome == "Skeleton":
            enemy_nomes_texto.append(nome_fonte.render("Skeleto", False, (70, 70, 70)).convert_alpha())
        elif todos_personagens_enemy[ca].nome == "Jorge":
            enemy_nomes_texto.append(nome_fonte.render(" Jorge", False, (200, 0, 0)).convert_alpha())
        else:
            enemy_nomes_texto.append(nome_fonte.render(todos_personagens_enemy[ca].nome, False, (0, 0, 0))
                                     .convert_alpha())

        # Carregar imagens / Enemy
        enemy_imagens_pers.append(pygame.transform.scale(todos_personagens_enemy[ca].image_ingame, (145, 145))
                                  .convert_alpha())

        # Carregar texto vida (barra de vida) / Enemy
        enemy_vida_texto.append(vida_fonte.render(f'{todos_personagens_enemy[ca].vida_atual:.0f} / '
                                                  f'{todos_personagens_enemy[ca].vida_max}', False, (0, 0, 0))
                                .convert_alpha())

        # Carregar texto mana (barra de vida) / Enemy
        enemy_mana_texto.append(mana_fonte.render(f'{todos_personagens_enemy[ca].mana_atual:.0f} / '
                                                  f'{todos_personagens_enemy[ca].mana_max}', False, (0, 0, 120))
                                .convert_alpha())

        # Carregar vida stat / Enemy
        enemy_vida_stat.append(stat_fonte.render(f'{todos_personagens_enemy[ca].vida_max}', False, (0, 0, 0))
                               .convert_alpha())

        # Carregar ataque stat / Enemy
        enemy_attack_stat.append(stat_fonte.render(f'{todos_personagens_enemy[ca].ataque}', False, (0, 0, 0))
                                 .convert_alpha())

        # Carregar defesa stat / Enemy
        enemy_defense_stat.append(stat_fonte.render(f'{todos_personagens_enemy[ca].defesa}', False, (0, 0, 0))
                                  .convert_alpha())

        # Carregar defesa extra stat / Enemy
        soma_defesa_extra = 0
        if todos_personagens_enemy[ca].defesa_extra[0]:
            soma_defesa_extra += todos_personagens_enemy[ca].defesa_extra[1]
        enemy_extradefense_stat.append(stat_fonte.render(f'+{soma_defesa_extra:.0f}', False, (0, 120, 0))
                                       .convert_alpha())

        # Carregar mana stat / Enemy
        enemy_mana_stat.append(stat_fonte.render(f'{todos_personagens_enemy[ca].mana_max}', False, (0, 0, 0))
                               .convert_alpha())

        # Carregar iniciativa stat / Enemy
        enemy_initiative_stat.append(stat_fonte.render(f'{todos_personagens_enemy[ca].iniciativa}', False, (0, 0, 0))
                                     .convert_alpha())

        # Rodadas faltam para o revelado desaparecer
        if todos_personagens_enemy[ca].revelado[0]:
            enemy_revelado_stat.append(stat_fonte.render(f'{todos_personagens_enemy[ca].revelado[1]} Left', False,
                                                         (0, 0, 0)).convert_alpha())
        else:
            enemy_revelado_stat.append(0)

    # Aviso ESC
    base_aviso = pygame.transform.scale(pygame.image.load('teclas/aviso_3.png'), (250, 250)).convert_alpha()

    # Tecla ESC
    tecla_esc = pygame.transform.scale(pygame.image.load('teclas/esc.png'), (130, 130)).convert_alpha()

    # Posição AVISO / ESC para Sair
    posicao_aviso = 713
    aviso_mostrando = True

    # Aviso texto
    sair_texto = mana_fonte.render('Sair', False, (0, 0, 0)).convert_alpha()

    # base - mostrando = (382, 634) - escondido  = (382, 713)
    # tecla - mostrando = (385, 665)

    # Sons
    lista_sons = []
    for ca in range(1, 11):
        lista_sons.append(pygame.mixer.Sound(f'sound/lista/book_flip.{ca}.ogg'))
    lista_sons_index = random.randint(0, 9)
    lista_sons[lista_sons_index].play()

    navegar_menu_som = pygame.mixer.Sound('sound/navegar_menu.mp3')

    lista_rodando = True
    while lista_rodando:

        mostrar_arena(todos_personagens_player, todos_personagens_enemy)
        janela.blit(fundo_lista, (0, 0))

        # Aviso Sair Lista
        janela.blit(base_aviso, (382, posicao_aviso))
        janela.blit(tecla_esc, (385, posicao_aviso + 31))
        janela.blit(sair_texto, (525, posicao_aviso + 82))

        if not controle_travado and tela_atual == 'player':

            # Cartas / Player
            for ca in range(0, 3):
                janela.blit(cartas, (carta_pos_x[ca], 30))

            # Nomes / Player
            for ca in range(0, 3):
                janela.blit(player_nomes_texto[ca], (carta_pos_x[ca] + 250, 49))

            # Imagens / Player
            for ca in range(0, 3):
                janela.blit(player_imagens_pers[ca], (carta_pos_x[ca] + 280, 112))

            # Vidas TEXTO / Player
            for ca in range(0, 3):
                janela.blit(player_vida_texto[ca], (carta_pos_x[ca] + 295, 322))

            # Vidas ÍCONE / Player
            for ca in range(0, 3):

                if todos_personagens_player[ca].vida_max > 100:

                    if todos_personagens_player[ca].vida_atual > 0:
                        janela.blit(heart_s[0], (carta_pos_x[ca] + 210, 397))
                        janela.blit(heart_s_lifebar[0], (carta_pos_x[ca] + 202, 289))
                    else:
                        janela.blit(heart_s[1], (carta_pos_x[ca] + 210, 397))
                        janela.blit(heart_s_lifebar[1], (carta_pos_x[ca] + 202, 289))

                else:

                    if todos_personagens_player[ca].vida_atual > 0:
                        janela.blit(heart[0], (carta_pos_x[ca] + 210, 397))
                        janela.blit(heart_lifebar[0], (carta_pos_x[ca] + 202, 289))
                    else:
                        janela.blit(heart[1], (carta_pos_x[ca] + 210, 397))
                        janela.blit(heart_lifebar[1], (carta_pos_x[ca] + 202, 289))

            # Manas TEXTO / Player
            for ca in range(0, 3):
                janela.blit(player_manas_texto[ca], (carta_pos_x[ca] + 320, 365))

            # Manas ÍCONES / Player
            for ca in range(0, 3):

                if todos_personagens_player[ca].mana_max > 18:

                    if todos_personagens_player[ca].mana_atual > 0:
                        janela.blit(mana_s[0], (carta_pos_x[ca] + 210, 490))
                        janela.blit(mana_s[0], (carta_pos_x[ca] + 270, 355))
                    else:
                        janela.blit(mana_s[1], (carta_pos_x[ca] + 210, 490))
                        janela.blit(mana_s[1], (carta_pos_x[ca] + 270, 355))

                else:

                    if todos_personagens_player[ca].mana_atual > 0:
                        janela.blit(mana[0], (carta_pos_x[ca] + 208, 490))
                        janela.blit(mana[0], (carta_pos_x[ca] + 270, 355))
                    else:
                        janela.blit(mana[1], (carta_pos_x[ca] + 208, 490))
                        janela.blit(mana[1], (carta_pos_x[ca] + 270, 355))

            # Outros TEXTOS / Player
            for ca in range(0, 3):
                # Vida
                janela.blit(player_vida_stat[ca], (carta_pos_x[ca] + 220, 450))

                # Ataque
                janela.blit(player_attack_stat[ca], (carta_pos_x[ca] + 340, 450))

                # Defesa
                janela.blit(player_defense_stat[ca], (carta_pos_x[ca] + 450, 450))

                # Defesa extra
                janela.blit(player_extradefense_stat[ca], (carta_pos_x[ca] + 440, 473))

                # Mana
                janela.blit(player_mana_stat[ca], (carta_pos_x[ca] + 220, 532))

                # Iniciativa
                janela.blit(player_initiative_stat[ca], (carta_pos_x[ca] + 343, 532))

            # Outros ÍCONES / Player
            for ca in range(0, 3):

                # Ataque
                if todos_personagens_player[ca].ataque > 18:
                    janela.blit(attack[1], (carta_pos_x[ca] + 332, 405))
                else:
                    janela.blit(attack[0], (carta_pos_x[ca] + 332, 405))

                # Defesa
                if todos_personagens_player[ca].defesa > 15:
                    janela.blit(defense[1], (carta_pos_x[ca] + 440, 402))
                else:
                    janela.blit(defense[0], (carta_pos_x[ca] + 440, 402))

                # Iniciativa
                if todos_personagens_player[ca].iniciativa > 15:
                    janela.blit(initiative[1], (carta_pos_x[ca] + 332, 490))
                else:
                    janela.blit(initiative[0], (carta_pos_x[ca] + 332, 490))

            # Mostrar aviso para inimigos
            janela.blit(inimigos_texto, (650, 674))
            janela.blit(seta_direita[0], (837, 562))

        elif not controle_travado and tela_atual == 'enemy':

            # Cartas / Enemy
            for pos in carta_pos_x_e:
                janela.blit(cartas, (pos, 30))

            # Nomes e Imagens/ Enemy
            for ca in range(0, len(todos_personagens_enemy)):
                janela.blit(enemy_nomes_texto[ca], (carta_pos_x_e[ca] + 250, 49))
                janela.blit(enemy_imagens_pers[ca], (carta_pos_x_e[ca] + 280, 112))

            # Se inimigo estiver revelado / Enemy
            for ca in range(0, len(todos_personagens_enemy)):

                if todos_personagens_enemy[ca].revelado[0]:

                    # Vidas TEXTO / Enemy
                    janela.blit(enemy_vida_texto[ca], (carta_pos_x_e[ca] + 295, 322))

                    # Vidas ÍCONE / Enemy
                    if todos_personagens_enemy[ca].vida_max > 100:

                        if todos_personagens_enemy[ca].vida_atual > 0:
                            janela.blit(heart_s[0], (carta_pos_x_e[ca] + 210, 397))
                            janela.blit(heart_s_lifebar[0], (carta_pos_x_e[ca] + 202, 289))
                        else:
                            janela.blit(heart_s[1], (carta_pos_x_e[ca] + 210, 397))
                            janela.blit(heart_s_lifebar[0], (carta_pos_x_e[ca] + 202, 289))

                    else:

                        if todos_personagens_enemy[ca].vida_atual > 0:
                            janela.blit(heart[0], (carta_pos_x_e[ca] + 210, 397))
                            janela.blit(heart_lifebar[0], (carta_pos_x_e[ca] + 202, 289))
                        else:
                            janela.blit(heart[1], (carta_pos_x_e[ca] + 210, 397))
                            janela.blit(heart_lifebar[1], (carta_pos_x_e[ca] + 202, 289))

                    # Manas TEXTO / Enemy
                    janela.blit(enemy_mana_texto[ca], (carta_pos_x_e[ca] + 320, 365))

                    # Manas ÍCONE / Enemy
                    if todos_personagens_enemy[ca].mana_max > 18:

                        if todos_personagens_enemy[ca].mana_atual > 0:
                            janela.blit(mana_s[0], (carta_pos_x_e[ca] + 210, 490))
                            janela.blit(mana_s[0], (carta_pos_x_e[ca] + 270, 355))
                        else:
                            janela.blit(mana_s[1], (carta_pos_x_e[ca] + 210, 490))
                            janela.blit(mana_s[1], (carta_pos_x_e[ca] + 270, 355))

                    else:

                        if todos_personagens_enemy[ca].mana_atual > 0:
                            janela.blit(mana[0], (carta_pos_x_e[ca] + 210, 490))
                            janela.blit(mana[0], (carta_pos_x_e[ca] + 270, 355))
                        else:
                            janela.blit(mana[1], (carta_pos_x_e[ca] + 210, 490))
                            janela.blit(mana[1], (carta_pos_x_e[ca] + 270, 355))

                    # Outros ÍCONES / Enemy

                    # Ataque
                    if todos_personagens_enemy[ca].ataque > 18:
                        janela.blit(attack[1], (carta_pos_x_e[ca] + 332, 405))
                    else:
                        janela.blit(attack[0], (carta_pos_x_e[ca] + 332, 405))

                    # Defesa
                    if todos_personagens_enemy[ca].defesa > 15:
                        janela.blit(defense[1], (carta_pos_x_e[ca] + 440, 402))
                    else:
                        janela.blit(defense[0], (carta_pos_x_e[ca] + 440, 402))

                    # Iniciativa
                    if todos_personagens_enemy[ca].iniciativa > 15:
                        janela.blit(initiative[1], (carta_pos_x_e[ca] + 332, 490))
                    else:
                        janela.blit(initiative[0], (carta_pos_x_e[ca] + 332, 490))

                    # Outros TEXTOS / Enemy

                    # Vida / Enemy
                    janela.blit(enemy_vida_stat[ca], (carta_pos_x_e[ca] + 220, 450))

                    # Ataque / Enemy
                    janela.blit(enemy_attack_stat[ca], (carta_pos_x_e[ca] + 340, 450))

                    # Defesa / Enemy
                    janela.blit(enemy_defense_stat[ca], (carta_pos_x_e[ca] + 450, 450))

                    # Defesa Extra / Enemy
                    janela.blit(enemy_extradefense_stat[ca], (carta_pos_x_e[ca] + 440, 473))

                    # Mana / Enemy
                    janela.blit(enemy_mana_stat[ca], (carta_pos_x_e[ca] + 220, 532))

                    # Iniciativa / Enemy
                    janela.blit(enemy_initiative_stat[ca], (carta_pos_x_e[ca] + 343, 532))

                    # Revelado Faltando / Enemy
                    janela.blit(enemy_revelado_stat[ca], (carta_pos_x_e[ca] + 316, 565))

                else:

                    janela.blit(misterio_texto, (carta_pos_x_e[ca] + 308, 410))

            # Mostrar aviso para Heróis / Enemy
            janela.blit(seta_esquerda[0], (-105, 562))
            janela.blit(herois_texto, (95, 675))

        if aviso_mostrando:

            if posicao_aviso >= 634:
                posicao_aviso -= 7
        else:

            if posicao_aviso < 713:
                posicao_aviso += 7

        # Eventos
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.KEYDOWN and not controle_travado:

                if event.key == pygame.K_ESCAPE:
                    fade_out = True
                    controle_travado = True
                    aviso_mostrando = False

                    lista_sons_index = random.randint(0, 9)
                    lista_sons[lista_sons_index].play()

                if event.key == pygame.K_LEFT:
                    navegar_menu_som.play()
                    tela_atual = 'player'

                if event.key == pygame.K_RIGHT:
                    navegar_menu_som.play()
                    tela_atual = 'enemy'

        # Fade In
        if fade_in:

            if fade_transparencia <= 190:
                fade_transparencia += 8
            else:
                fade_in = False
                controle_travado = False

            fundo_lista.set_alpha(fade_transparencia)

        # Fade Out
        if fade_out:

            if fade_transparencia > 0:
                fade_transparencia -= 8
            else:
                lista_rodando = False

            fundo_lista.set_alpha(fade_transparencia)

        pygame.display.update()
        delta = ticks.tick(60)


def turno_player(personagem, vida_personagens, diferenca_head, personagens_p_arena, personagens_e_arena):
    """ +Função+
    - Destinado para o sistema de batalha do jogo, sendo essa função o turno do jogador

    - personagem = Personagem que vai jogar o turno(Classe)
    - vida_personagens = Todos os personagens do jogador, para mostrar a vida deles na barra de ações
    - diferenca_head = A diferença para que a cabeça dos personagens fique corretamente dentro do círculo da vida
    - personagens_p_arena = Personagens do jogador para mostrar-los na arena quando a função mostrar_arena for acionada
    - personagens_e_arena = Personagens do inimigo para mostrar-lod na arena quando a função mostrar_arena for acionada
    """

    # Globais
    global delta
    global ticks

    # Fontes
    opcoes_fonte = pygame.font.Font('alagard.ttf', 32)

    # Sprite base ação do personagem
    base_acoes = pygame.transform.scale(pygame.image.load('batalha/base_acoes.png'), (1025, 1025)).convert_alpha()

    # Sprite cabeça / Mostrar a vez do personagem
    # Wizard Cabeçudo
    if personagem.nome == 'Wizard':
        turno_head = pygame.transform.scale(personagem.image_face, (270, 270)).convert_alpha()
    else:
        turno_head = pygame.transform.scale(personagem.image_face, (320, 320)).convert_alpha()

    # Sprite Seta
    seta_sprite = pygame.transform.scale(pygame.image.load('batalha/seta_selecionado.png'), (100, 100)) \
        .convert_alpha()

    # Textos
    ataque = opcoes_fonte.render('Atacar', False, (0, 0, 0)).convert_alpha()
    defesa = opcoes_fonte.render('Defender', False, (0, 0, 0)).convert_alpha()

    lista = opcoes_fonte.render('Lista', False, (0, 0, 0)).convert_alpha()

    # Seta Selecionado
    seta_selecionar = 0
    turno_selecionado = ''

    # Posições para que a seta fique corretamente ao lado dos textos
    seta_posicoes_y = [516, 555, 594, 633]

    turno_fim = False

    # Sons
    confirma_som = pygame.mixer.Sound('sound/confirmar.mp3')
    navegar_menu_som = pygame.mixer.Sound('sound/navegar_menu.mp3')

    # Verificar se o turno está rodando
    rodando_turno = True
    while rodando_turno:
        # Testar se a mana atual é maior que 18, para indicar se é possivel analisar um inimigo
        if personagem.mana_atual >= 18:
            analise = opcoes_fonte.render('Analisar -18', False, (0, 0, 0)).convert_alpha()
            mana_analisar = pygame.transform.scale(pygame.image.load('cartas_icon/mana.png'), (40, 40)).convert_alpha()
        else:
            analise = opcoes_fonte.render('Analisar -18', False, (180, 0, 0)).convert_alpha()
            mana_analisar = pygame.transform.scale(pygame.image.load('cartas_icon/mana_empty.png'), (40, 40)) \
                .convert_alpha()

        mostrar_arena(personagens_p_arena, personagens_e_arena)

        janela.blit(base_acoes, (0, -18))

        # Cabeça Personagem Jogador
        if personagem.nome == 'Paladin':
            janela.blit(turno_head, (-40, 550))

        elif personagem.nome == 'Wizard':
            janela.blit(turno_head, (25, 565))

        else:
            janela.blit(turno_head, (15, 550))

        # Posições da SETA
        # X - FIXO = 210
        # Y - ATAQUE = 516
        # Y - DEFESA = 555
        # Y - ANALISE = 594

        if turno_selecionado == '':
            # Mostrar opções iniciais
            janela.blit(ataque, (280, 550))
            janela.blit(defesa, (280, 590))

            janela.blit(analise, (280, 630))
            janela.blit(mana_analisar, (450, 625))

            janela.blit(lista, (280, 670))

            # Mostrar a seta de seleção
            janela.blit(seta_sprite, (210, seta_posicoes_y[seta_selecionar]))

        elif turno_selecionado == 'ataque':
            confirma_som.play()
            turno_fim = turno_selecao(personagem, 'ataque', personagens_p_arena, personagens_e_arena, diferenca_head)
            turno_selecionado = ''

        elif turno_selecionado == 'defesa':
            confirma_som.play()
            turno_fim = turno_selecao(personagem, 'defesa', personagens_p_arena, personagens_e_arena, diferenca_head)
            turno_selecionado = ''

        elif turno_selecionado == 'analisar':

            if personagem.mana_atual >= 18:
                confirma_som.play()
                turno_fim = analisar(personagem, personagens_p_arena, personagens_e_arena, diferenca_head)

            turno_selecionado = ''
        elif turno_selecionado == 'lista':
            mostrar_lista(personagens_p_arena, personagens_e_arena)
            turno_selecionado = ''

        if turno_fim:
            break

        # Mostrar vida dos personagens
        mostrar_vida(vida_personagens[0], 680, 467, diferenca_head[0][0], diferenca_head[0][1])
        mostrar_vida(vida_personagens[1], 680, 541, diferenca_head[1][0], diferenca_head[1][1])
        mostrar_vida(vida_personagens[2], 680, 616, diferenca_head[2][0], diferenca_head[2][1])

        # Eventos
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.KEYDOWN:

                # Sistema para selecionar o menu de turno
                if event.key == pygame.K_DOWN:

                    if seta_selecionar < 3 and turno_selecionado == '':
                        navegar_menu_som.play()
                        seta_selecionar += 1

                if event.key == pygame.K_UP:

                    if seta_selecionar > 0 and turno_selecionado == '':
                        navegar_menu_som.play()
                        seta_selecionar -= 1

                if event.key == pygame.K_RETURN:

                    if seta_selecionar == 0:
                        turno_selecionado = 'ataque'
                    elif seta_selecionar == 1:
                        turno_selecionado = 'defesa'
                    elif seta_selecionar == 2:
                        turno_selecionado = 'analisar'
                    elif seta_selecionar == 3:
                        turno_selecionado = 'lista'

        pygame.display.update()
        delta = ticks.tick(60)


def mostrar_arena(personagens_player, personagens_enemy):
    """ +Função+
    - Destinada para mostrar os players em um arena dentro de uma janela no pygame

    - :param personagens_player: = lista com todos os personagens do jogador(Classe)
    - :param personagens_enemy: = lista com todos os personagens do inimigo(Classe)
    """

    posicoes_player = [(180, 80), (110, 215), (180, 335)]

    # Efeitos
    fogo = pygame.transform.scale(pygame.image.load('efeitos/fogo.png'), (120, 120)).convert_alpha()
    atordoado = pygame.transform.scale(pygame.image.load('efeitos/atordoado.png'), (120, 120)).convert_alpha()

    # Fundo
    fundo_battle = pygame.transform.scale(pygame.image.load('batalha/fundo_game.png'), (1024, 768)).convert_alpha()

    janela.blit(fundo_battle, (0, 20))
    janela.blit(fundo_battle, (0, -40))

    # Lado Player
    for ca in range(0, 3):
        janela.blit(personagens_player[ca].image_ingame, posicoes_player[ca])

        if personagens_player[ca].queimando[0]:
            janela.blit(fogo, (posicoes_player[ca][0] - 80, posicoes_player[ca][1] - 15))

        if personagens_player[ca].atordoado[0]:
            janela.blit(atordoado, (posicoes_player[ca][0] - 80, posicoes_player[ca][1] + 40))

    # Lado Enemy
    if len(grupo_enemy) == 1:
        janela.blit(personagens_enemy[0].image_ingame, (650, 220))

        # Caso o inimigo esteja pegando fogo
        if personagens_enemy[0].queimando[0]:
            janela.blit(fogo, (650 + 100, 220 - 20))

        # Caso o inimigo esteja atordoado
        if personagens_enemy[0].atordoado[0]:
            janela.blit(atordoado, (750, 250))

    elif len(grupo_enemy) == 2:
        janela.blit(personagens_enemy[0].image_ingame, (650, 130))
        janela.blit(personagens_enemy[1].image_ingame, (650, 320))

        # Caso o inimigo esteja pegando fogo
        if personagens_enemy[0].queimando[0]:
            janela.blit(fogo, (650 + 100, 130 - 20))
        if personagens_enemy[1].queimando[0]:
            janela.blit(fogo, (650 + 100, 320 - 20))

        # Caso o inimigo esteja atordoado
        if personagens_enemy[0].atordoado[0]:
            janela.blit(atordoado, (750, 170))
        if personagens_enemy[1].atordoado[0]:
            janela.blit(atordoado, (750, 360))

    elif len(grupo_enemy) == 3:
        janela.blit(personagens_enemy[0].image_ingame, (630, 100))
        janela.blit(personagens_enemy[1].image_ingame, (720, 210))
        janela.blit(personagens_enemy[2].image_ingame, (630, 330))

        # Caso o inimigo esteja pegando fogo
        if personagens_enemy[0].queimando[0]:
            janela.blit(fogo, (630 + 100, 100 - 20))
        if personagens_enemy[1].queimando[0]:
            janela.blit(fogo, (720 + 100, 210 - 20))
        if personagens_enemy[2].queimando[0]:
            janela.blit(fogo, (630 + 100, 330 - 20))

        # Caso o inimigo esteja atordoado
        if personagens_enemy[0].atordoado[0]:
            janela.blit(atordoado, (730, 140))
        if personagens_enemy[1].atordoado[0]:
            janela.blit(atordoado, (820, 250))
        if personagens_enemy[2].atordoado[0]:
            janela.blit(atordoado, (730, 370))


def verificar_efeitos(personagem_selecionado):
    """+Função+
    - Destinada a verificar todos os efeitos de um personagem, assim diminuindo 1 a cada round e desabilitando caso o
    numero de round para que o efeito passe seja excedido

    personagem_selecionado = personagem na qual será verificado os efeitos
    """
    # Fogo
    if personagem_selecionado.queimando[0]:

        if personagem_selecionado.queimando[1] > 0:

            personagem_selecionado.vida_atual -= 2
            personagem_selecionado.queimando[1] -= 1

        else:

            personagem_selecionado.queimando = [False]

    # Veneno
    if personagem_selecionado.envenenado[0]:

        if personagem_selecionado.envenenado[1] > 0:

            personagem_selecionado.vida_atual -= 4
            personagem_selecionado.envenenado[1] -= 1

        else:

            personagem_selecionado.envenenado = [False]


def turno_enemy(personagem, todos_player, todos_enemy, diferenca_head):
    """+Função+
    - Destinada a criar um round para que o inimigo tome a ação na batalha, atacando, defendendo ou curando

    personagem = personagem na qual irá realizar a ação
    todos_player = lista com todos os personagens do jogador
    todos_enemy = lista com todos os personagens do inimigo
    diferenca_head = diferença da posição da cabeça do personagem destinada para o uso do mostrar_vida()
    """
    # Globais
    global delta
    global ticks

    # Fontes
    pontos_fonte = pygame.font.Font('alagard.ttf', 42)

    # Base ações
    base_acoes = pygame.transform.scale(pygame.image.load('batalha/base_acoes.png'), (1025, 1025)).convert_alpha()

    # Cabeça
    if personagem.nome == "Skeleton":
        posicao_turno_head = (5, 570)
        turno_head = pygame.transform.scale(personagem.image_face, (320, 320)).convert_alpha()

    elif personagem.nome == "Dark Wizard":
        posicao_turno_head = (0, 560)
        turno_head = pygame.transform.scale(personagem.image_face, (270, 270)).convert_alpha()

    else:
        posicao_turno_head = (5, 570)
        turno_head = pygame.transform.scale(personagem.image_face, (320, 320)).convert_alpha()

    # Carregamento Imagem
    aguardando = []
    for ca in range(0, 9):
        aguardando.append(pygame.transform.scale(pygame.image.load(f'tela_loading/frame/{ca}.png'), (400, 400))
                          .convert_alpha())

    tick_aguardando = 0
    aguardando_selected = 0
    duracao_aguardando = 100

    # Sons
    dado_som = pygame.mixer.Sound('sound/dados_rolando.mp3')
    dado_som_tocou = False

    # Decisão Enemy
    # 0 = Ataque
    # 1 = Defesa
    # 2 = Cura
    decisao = random.randint(-2, 2)
    selecionados = []
    b_difer_head = []
    acao_imagem = 0
    escolha_ataque = 0
    escolha_defesa = 0
    dano = 0
    alvos = 0
    envenenado_texto = 0
    envenenado_imagem = 0
    rodadas_envenenado = 0
    defendendo_texto = 0
    defendendo_imagem = 0
    rodadas_defendendo = 0

    # Ataque
    if decisao <= 0:

        # Tipo ação / Imagem
        acao_imagem = pygame.transform.scale(pygame.image.load('acoes_enemy/atacar.png'), (100, 100)).convert_alpha()

        escolha_ataque = random.choice(personagem.ataques)

        # Ajustar os alvos ao escolher o ataque
        if escolha_ataque == "Basico":
            alvos = 1
        elif escolha_ataque == "Envenenamento":
            alvos = 2
            rodadas_envenenado = random.randint(1, 3)
            envenenado_texto = pontos_fonte.render(f'+{rodadas_envenenado}', False, (0, 120, 0)).convert_alpha()
            envenenado_imagem = pygame.transform.scale(pygame.image.load('efeitos/veneno.png'), (80, 80))\
                .convert_alpha()

        elif escolha_ataque == "Explosão Ossos":
            alvos = 3

        # Verificar se os alvos do jogador são suficientes para o número de alvos de um ataque
        player_vivos = 0
        for player in todos_player:

            if not player.derrotado:
                player_vivos += 1

        if player_vivos < alvos:
            alvos = player_vivos

        # Sistema de escolha / O inimigo escolhe qual player ataca
        selecionados = []
        while True:
            alvo_selecionado = random.randint(0, len(todos_player) - 1)

            if not todos_player[alvo_selecionado].derrotado:

                if alvo_selecionado in selecionados:
                    pass
                else:
                    selecionados.append(alvo_selecionado)

                    if todos_player[alvo_selecionado].nome == "Paladin":
                        b_difer_head.append(20)
                    else:
                        b_difer_head.append(0)

                    if len(selecionados) == alvos:
                        break

        dano = (personagem.ataque * (random.randint(25, 100) / 100))

    # Defesa
    elif decisao == 1:

        # Tipo ação / Imagem
        acao_imagem = pygame.transform.scale(pygame.image.load('acoes_enemy/defesa.png'), (100, 100)).convert_alpha()

        defendendo_imagem = pygame.transform.scale(pygame.image.load('cartas_icon/shield.png'), (80, 80))\
            .convert_alpha()

        escolha_defesa = random.choice(personagem.defesas)

        if escolha_defesa == "Basico":
            alvos = "self"
            rodadas_defendendo = random.randint(2, 3)

            if personagem.revelado[0]:
                defendendo_texto = pontos_fonte.render(f"+{rodadas_defendendo}", False, (0, 0, 0)).convert_alpha()
            else:
                defendendo_texto = pontos_fonte.render(f"?", False, (0, 0, 0)).convert_alpha()

        dano = personagem.defesa * (random.randint(40, 50) / 100)

    # Cura
    elif decisao == 2:

        # Tipo ação / Imagem
        acao_imagem = pygame.transform.scale(pygame.image.load('acoes_enemy/curar.png'), (100, 100)).convert_alpha()

        escolha_cura = random.choice(["Curar-se", "Curar aliado"])

        if escolha_cura == "Curar-se":
            alvos = "self"

        elif escolha_cura == "Curar aliado":
            alvos = 1

            # Verificar se os alvos do inimigo são suficientes para o número de alvos de uma cura
            enemy_vivos = 0
            for enemy in todos_enemy:

                if not enemy.derrotado:
                    enemy_vivos += 1

            if enemy_vivos < alvos:
                alvos = enemy_vivos

            if enemy_vivos >= 2:

                # Sistema para o curandeiro escolher alguem para curar
                while True:
                    alvo_selecionado = random.randint(0, len(todos_enemy) - 1)

                    if not todos_enemy[alvo_selecionado].derrotado:

                        if not todos_enemy[alvo_selecionado].nome == personagem.nome:
                            selecionados.append(alvo_selecionado)
                            b_difer_head.append(0)

                            break
            else:
                alvos = "self"

        dano = personagem.vida_atual * (random.randint(5, 8) / 100)

    # Carregar imagem do alvo

    alvos_pos = []
    if len(selecionados) == 1:
        alvos_pos = [(510 - b_difer_head[0], 620)]
    elif len(selecionados) == 2:
        alvos_pos = [(510 - b_difer_head[0], 560), (510 - b_difer_head[1], 660)]
    elif len(selecionados) == 3:
        alvos_pos = [(510 - b_difer_head[0], 520), (510 - b_difer_head[1], 590), (510 - b_difer_head[2], 670)]

    alvo_image = []
    for valor in selecionados:
        if decisao <= 0:
            alvo_image.append(pygame.transform.scale(todos_player[valor].image_face, (150, 150)).convert_alpha())
        else:
            alvo_image.append(pygame.transform.scale(todos_enemy[valor].image_face, (150, 150)).convert_alpha())

    # Rodar dado para contar dano
    tam_dados = (200, 200)
    dado_rodando = True
    dado_mostrando = 0
    tick_dado = 0
    dado = []
    for ca in range(0, 6):
        dado.append(pygame.transform.scale(pygame.image.load(f'batalha/dados/{ca}.png'), tam_dados).convert_alpha())

    # Textos
    dano_texto = pontos_fonte.render(f'{dano:.0f}', False, (0, 0, 0)).convert_alpha()

    result_time = False
    aguardando_time = True
    mostrar_pontos = False
    terminar_rodada = [False]

    turno_enemy_rodando = True
    while turno_enemy_rodando:

        # Mostrar arena
        mostrar_arena(todos_player, todos_enemy)

        # Base ações
        janela.blit(base_acoes, (0, -18))

        # Cabeça
        janela.blit(turno_head, posicao_turno_head)

        # Mostrar vida / Canto inferior direito
        mostrar_vida(todos_player[0], 680, 467, diferenca_head[0][0], diferenca_head[0][1])
        mostrar_vida(todos_player[1], 680, 541, diferenca_head[1][0], diferenca_head[1][1])
        mostrar_vida(todos_player[2], 680, 616, diferenca_head[2][0], diferenca_head[2][1])

        if aguardando_time:

            # Aguardando
            if duracao_aguardando > 0:
                janela.blit(aguardando[aguardando_selected], (245, 440))

                if tick_aguardando < 5:
                    tick_aguardando += 1
                else:
                    tick_aguardando = 0

                    if aguardando_selected >= 8:
                        aguardando_selected = 1
                    else:
                        aguardando_selected += 1

                duracao_aguardando -= 1

            else:

                if not result_time:
                    result_time = True
                    aguardando_time = False

        # Resultado
        if result_time:

            # Dado
            janela.blit(dado[dado_mostrando], (308, 570))

            # Mostrar qual ação o personagem está tomando
            janela.blit(acao_imagem, (250, 615))

            # Mostrar alvos

            for ca in range(0, len(selecionados)):
                janela.blit(alvo_image[ca], alvos_pos[ca])

            # Dado

            if not dado_som_tocou:
                dado_som.play()
                dado_som_tocou = True

            if dado_rodando:

                if tick_dado >= 10:

                    if dado_mostrando >= 5:
                        dado_mostrando = 0
                        dado_rodando = False

                        if personagem.revelado or decisao <= 0:
                            mostrar_pontos = True

                        terminar_rodada = [True, 0]

                    else:
                        dado_mostrando += 1

                    tick_dado = 0

                tick_dado += 1

            else:

                # Mostrar Dano/Cura/Defesa
                if mostrar_pontos:
                    janela.blit(dano_texto, (480, 650))

                    if decisao <= 0:

                        if escolha_ataque == "Envenenamento":
                            janela.blit(envenenado_texto, (455, 550))
                            janela.blit(envenenado_imagem, (370, 530))

                    elif decisao == 1:

                        if escolha_defesa == "Basico":
                            janela.blit(defendendo_texto, (455, 550))
                            janela.blit(defendendo_imagem, (370, 530))

                if terminar_rodada[0]:

                    if terminar_rodada[1] < 45:
                        terminar_rodada[1] += 1
                    else:

                        if decisao <= 0:

                            for alvo in selecionados:
                                defesa_alvo = 0
                                defesa_alvo += todos_player[alvo].defesa

                                if todos_player[alvo].defesa_extra[0]:
                                    defesa_alvo += todos_player[alvo].defesa_extra[1]

                                if todos_player[alvo].defesa_paladino[0]:
                                    defesa_alvo += todos_player[alvo].defesa_paladino[1]

                                todos_player[alvo].vida_atual -= dano * (50 / (50 + defesa_alvo))

                                if escolha_ataque == "Envenenamento":
                                    todos_player[alvo].envenenado = [True, rodadas_envenenado]

                        elif decisao == 1:
                            if alvos == "self":
                                personagem.defesa_extra = [True, dano, rodadas_defendendo]

                        elif decisao == 2:

                            if alvos == "self":

                                if personagem.vida_atual + dano < personagem.vida_max:
                                    personagem.vida_atual += dano
                                else:
                                    personagem.vida_atual = personagem.vida_max

                            else:
                                for alvo in selecionados:

                                    if todos_enemy[alvo].vida_atual + dano < todos_enemy[alvo].vida_max:
                                        todos_enemy[alvo].vida_atual += dano
                                    else:
                                        todos_enemy[alvo].vida_atual = todos_enemy[alvo].vida_max

                        return True

        # Eventos
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                exit()

        pygame.display.update()
        delta = ticks.tick(60)


def verificar_defesa_extra(todos_personagens):
    """
    +Função+
    - Destinada a verificar a defesa extra de um personagem, caso o numero de rodadas defendendo termine, a defesa extra
    será desabilitada
    """
    for personagem in todos_personagens:

        # Defesa Extra
        if personagem.defesa_extra[0]:

            if personagem.defesa_extra[2] > 0:
                personagem.defesa_extra[2] -= 1

            if personagem.defesa_extra[2] == 0:

                personagem.defesa_extra = [False]

        # Defesa Paladino
        if personagem.defesa_paladino[0]:

            if personagem.defesa_paladino[2] > 0:
                personagem.defesa_paladino[2] -= 1

            if personagem.defesa_paladino[2] == 0:

                personagem.defesa_paladino = [False]


def verificar_revelado(todos_personagens):
    """
    +Função
    - Destinada a verificar o estado de 'revelado' do personagem, caso o numero de rodadas revelado restante acabe, o
    estado de 'revelado' é desabilitado
    """
    for personagem in todos_personagens:

        # Revelado
        if personagem.revelado[0]:

            if personagem.revelado[1] > 0:
                personagem.revelado[1] -= 1

            if personagem.revelado[1] == 0:
                personagem.revelado = [False]


def carregar_mana(todos_player, todos_enemy):
    """
    +Função+
    - Destinada a recarregar a mana em +2 para todos os personagens
    """
    for pers in todos_player:

        if pers.mana_atual + 2 <= pers.mana_max:
            pers.mana_atual += 2
        else:
            pers.mana_atual = pers.mana_max

    for pers in todos_enemy:

        if pers.mana_atual + 2 <= pers.mana_max:
            pers.mana_atual += 2
        else:
            pers.mana_atual = pers.mana_max


def resultado_jogo(tipo):
    """
    +Função+
    - Destinada a mostrar uma tela de game over, mostrando se o jogador ganhou ou perdeu a batalha, voltar para o menu
    e reiniciar todas as classes
    """

    # Globais
    global delta
    global ticks

    # Reiniciar personagens
    reiniciar_classes()

    # Escuro
    escuro_resultado = pygame.transform.scale(pygame.image.load('transicao/escuro.png'), (1024, 768)).convert_alpha()

    controle_travado = True
    result = 0
    result_pos = 0
    result_som = 0
    # Derrota
    if tipo == "derrota":
        pygame.display.set_caption('IntroSouls - Derrota!')
        result = pygame.transform.scale(pygame.image.load('resultado_jogo/derrota.png'), (500, 500)).convert_alpha()
        result_pos = (267, 130)

        result_som = pygame.mixer.Sound('sound/Derrota.ogg')
        result_som.set_volume(150)

    # Vitoria
    elif tipo == "vitoria":
        pygame.display.set_caption('IntroSouls - Vitória!')
        result = pygame.transform.scale(pygame.image.load('resultado_jogo/vitoria.png'), (500, 500)).convert_alpha()
        result_pos = (263, 130)

        result_som = pygame.mixer.Sound('sound/Vitoria.mp3')
        result_som.set_volume(125)

    result_som.play(-1)

    # Sons
    confirma_som = pygame.mixer.Sound('sound/confirmar.mp3')

    # Ok
    ok = pygame.transform.scale(pygame.image.load('selecao_menu/ok_s.png'), (225, 225)).convert_alpha()

    resultado_fade_in = True
    resultado_fade_out = False
    fade_transparencia = 0

    resultado_jogo_rodando = True
    while resultado_jogo_rodando:

        janela.blit(escuro_resultado, (0, 0))
        janela.blit(result, result_pos)

        if not controle_travado:
            janela.blit(ok, (400, 320))

        # Eventos
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RETURN:

                    if not controle_travado:
                        confirma_som.play()
                        controle_travado = True
                        resultado_fade_out = True

        # Fade in
        if resultado_fade_in:

            if fade_transparencia < 255:
                fade_transparencia += 5
            else:
                resultado_fade_in = False
                controle_travado = False

            result.set_alpha(fade_transparencia)

        if resultado_fade_out:

            if fade_transparencia > 0:
                fade_transparencia -= 5
            else:
                result_som.stop()
                menu()

            result.set_alpha(fade_transparencia)

        pygame.display.update()
        delta = ticks.tick(60)


def batalha(player_chars, enemy_chars, difer_head, tipo=''):
    """
    +Função+
    - Destinada a organizar uma batalha

    player_chars = lista com os personagens do player
    enemy_chars = lista com os personagens do inimigo
    difer_head = diferença da posição da cabeça destinada ao uso do mostrar_vida()
    """
    # Globais
    global delta
    global ticks

    # Sprite Base ações Player
    base_sem_acao = pygame.transform.scale(pygame.image.load('batalha/base_sem_acao.png'), (1025, 1025)).convert_alpha()

    # Escuro / Fade In / Fade Out
    escuro_batalha = pygame.transform.scale(pygame.image.load('transicao/escuro.png'), (1024, 768)).convert_alpha()
    fade_in = False
    fade_transparencia_batalha = 0

    # Musica
    if tipo == 'introcomp':
        pygame.mixer.music.load('sound/Batalha1.mp3')
    else:
        pygame.mixer.music.load('sound/Batalha1.mp3')

    pygame.mixer.music.play(-1)

    # Sistema de turnos
    rodando_batalha = True
    while rodando_batalha:

        mostrar_arena(player_chars, enemy_chars)

        janela.blit(base_sem_acao, (0, -18))

        # Mostrar vida dos personagens
        mostrar_vida(player_chars[0], 680, 467, difer_head[0][0], difer_head[0][1])
        mostrar_vida(player_chars[1], 680, 541, difer_head[1][0], difer_head[1][1])
        mostrar_vida(player_chars[2], 680, 616, difer_head[2][0], difer_head[2][1])

        for ca in range(0, len(player_chars)):

            # Verificar resultado do jogo
            resultado = verificar_resultado_player(player_chars, enemy_chars)
            if resultado != "andamento":
                break

            # Vez dos personagens do player
            if not player_chars[ca].derrotado:

                if not player_chars[ca].atordoado[0]:
                    pygame.display.set_caption(f"IntroSouls - Vez de {player_chars[ca].nome}!")
                    turno_player(player_chars[ca], player_chars, difer_head, player_chars, enemy_chars)
                else:

                    if player_chars[ca].atordoado[1] > 0:
                        player_chars[ca].atordoado[1] -= 1

                    if player_chars[ca].atordoado[1] == 0:
                        player_chars[ca].atordoado = [False]

            # Verificar se alguem morreu / Player / Enemy
            for player_morte in range(0, 3):
                verificar_efeitos(player_chars[player_morte])
                verificar_morte(player_chars[player_morte])

            for enemy_morte in range(0, len(enemy_chars)):
                verificar_efeitos(enemy_chars[enemy_morte])
                verificar_morte(enemy_chars[enemy_morte])

            verificar_revelado(enemy_chars)
            verificar_defesa_extra(enemy_chars)
            carregar_mana(player_chars, enemy_chars)

        for ca in range(0, len(enemy_chars)):

            # Verificar resultado do jogo
            resultado = verificar_resultado_player(player_chars, enemy_chars)
            if resultado != "andamento":
                break

            # Vez dos personagens do inimigo
            if not enemy_chars[ca].derrotado:

                if not enemy_chars[ca].atordoado[0]:
                    pygame.display.set_caption(f"IntroSouls - Vez de {enemy_chars[ca].nome}!")
                    turno_enemy(enemy_chars[ca], player_chars, enemy_chars, difer_head)
                else:

                    if enemy_chars[ca].atordoado[1] > 0:
                        enemy_chars[ca].atordoado[1] -= 1

                    if enemy_chars[ca].atordoado[1] == 0:
                        enemy_chars[ca].atordoado = [False]

            # Verificar se alguem morreu / Player / Enemy
            for player_morte in range(0, 3):
                verificar_efeitos(player_chars[player_morte])
                verificar_morte(player_chars[player_morte])

            for enemy_morte in range(0, len(enemy_chars)):
                verificar_efeitos(enemy_chars[enemy_morte])
                verificar_morte(enemy_chars[enemy_morte])

            verificar_defesa_extra(player_chars)
            carregar_mana(player_chars, enemy_chars)

        # Eventos
        for event_battle in pygame.event.get():

            if event_battle.type == pygame.QUIT:
                exit()

        # Verificar batalha
        # Verificar se o jogador ganhou ou perdeu, logo após, fazer um fade

        resultado = verificar_resultado_player(player_chars, enemy_chars)

        if resultado != "andamento":

            if not fade_in:
                fade_in = True
                fade_transparencia_batalha = 0

        # Fade in
        if fade_in:

            if fade_transparencia_batalha < 255:
                fade_transparencia_batalha += 8
                escuro_batalha.set_alpha(fade_transparencia_batalha)

            else:
                pygame.mixer.music.stop()
                resultado_jogo(resultado)

            janela.blit(escuro_batalha, (0, 0))

        pygame.display.update()
        delta = ticks.tick(60)


def preparar_batalha(grupo_selecionado, tipo=''):
    """
    +Função+
    - Destinada a preparar uma batalha, organizando todas os ataques, imagens, parâmetros de cada personagem e
    organizando para que a função batalha() inicie.

    grupo_selecionado = uma lista com strings com o nome dos personagens que o jogador irá batalha, assim o programa vai
    criar classes com essas strings!

    tipo = determina quais inimigos vão estar na batalha
    """

    # Globais
    global janela
    global delta
    global ticks
    global grupo_player
    global grupo_enemy
    global dif_head

    tam_char = (180, 180)
    tam_char_enemy = (175, 175)
    tam_head = (100, 100)

    # Ao adicionar um personagem
    # 1 - Adicionar imagem do personagem
    # 2 - Adicionar imagem da cabeça do personagem (Na vida)
    # 3 - A diferença da posição para que a cabeça fique corretamente na barra de vida

    if tipo == 'introcomp':
        grupo_enemy = [jorge_stat, thiago_stat]
    else:
        grupo_enemy = [skeleton_stat, darkwizard_stat]

    if "rogue" in grupo_selecionado:
        grupo_player.append(rogue_stat)

    if "hunter" in grupo_selecionado:
        grupo_player.append(hunter_stat)

    if "priest" in grupo_selecionado:
        grupo_player.append(priest_stat)

    if "wizard" in grupo_selecionado:
        grupo_player.append(wizard_stat)

    if "paladin" in grupo_selecionado:
        grupo_player.append(paladin_stat)

    # Players
    for c in range(0, 3):

        if grupo_player[c].nome == 'Hunter':
            grupo_player[c].image_ingame = pygame.transform.scale(pygame.image.load('personagens/hunter sprite.png'),
                                                                  tam_char).convert_alpha()

            grupo_player[c].image_face = pygame.transform.scale(pygame.image.load('personagens/cabeça/hunter.png'),
                                                                tam_head).convert_alpha()

            dif_head.append((10, 62))
            grupo_player[c].ataques = ['Basico', 'Magico', 'Flecha Dupla', 'Adaga']
            grupo_player[c].defesas = ['Basico', 'Curar-se', 'Arco vida']

        elif grupo_player[c].nome == 'Priest':
            grupo_player[c].image_ingame = pygame.transform.scale(pygame.image.load('personagens/PRIEST_NoShadow.png'),
                                                                  tam_char).convert_alpha()

            grupo_player[c].image_face = pygame.transform.scale(pygame.image.load('personagens/cabeça/priest.png'),
                                                                tam_head).convert_alpha()

            dif_head.append((12, 66))
            grupo_player[c].ataques = ['Basico', 'Magico', 'Atordoar']
            grupo_player[c].defesas = ['Basico', 'Curar-se']

        elif grupo_player[c].nome == 'Paladin':
            grupo_player[c].image_ingame = pygame.transform.scale(pygame.image.load('personagens/Paladino.png'),
                                                                  tam_char).convert_alpha()

            grupo_player[c].image_face = pygame.transform.scale(pygame.image.load('personagens/cabeça/paladino.png'),
                                                                tam_head).convert_alpha()

            dif_head.append((30, 62))

            grupo_player[c].ataques = ['Basico', 'Magico']
            grupo_player[c].defesas = ['Basico', 'Curar-se', 'Paladino']

        elif grupo_player[c].nome == 'Wizard':
            grupo_player[c].image_ingame = pygame.transform.scale(pygame.image.load('personagens/wizardfinal.png'),
                                                                  tam_char).convert_alpha()

            grupo_player[c].image_face = pygame.transform.scale(pygame.image.load('personagens/cabeça/wizard.png'),
                                                                tam_head).convert_alpha()

            dif_head.append((7, 68))
            grupo_player[c].ataques = ['Basico', 'Magico', 'Fogareu']
            grupo_player[c].defesas = ['Basico', 'Curar-se']

        elif grupo_player[c].nome == 'Rogue':
            grupo_player[c].image_ingame = pygame.transform.scale(pygame.image.load('personagens/rogue.png'),
                                                                  tam_char).convert_alpha()

            grupo_player[c].image_face = pygame.transform.scale(pygame.image.load('personagens/cabeça/rogue.png'),
                                                                tam_head).convert_alpha()

            dif_head.append((15, 64))
            grupo_player[c].ataques = ['Basico', 'Magico', 'Mordida']
            grupo_player[c].defesas = ['Basico', 'Curar-se']

    # Inimigos
    for c in range(0, len(grupo_enemy)):

        if grupo_enemy[c].nome == 'Skeleton':
            grupo_enemy[c].image_ingame = pygame.transform.flip(pygame.transform.scale(pygame.image.load(
                'personagens/caveira sprite 2.png'), tam_char_enemy), True, False).convert_alpha()

            grupo_enemy[c].image_face = pygame.transform.flip(pygame.transform.scale(pygame.image.load(
                'personagens/cabeça/skeleto.png'), tam_head), True, False).convert_alpha()

            grupo_enemy[c].ataques = ['Basico', "Explosão Ossos"]
            grupo_enemy[c].defesas = ['Basico', 'Curar-se']

        elif grupo_enemy[c].nome == 'Dark Wizard':
            grupo_enemy[c].image_ingame = pygame.transform.flip(pygame.transform.scale(pygame.image.load(
                'personagens/dark_wizard.png'), tam_char_enemy), True, False).convert_alpha()

            grupo_enemy[c].image_face = pygame.transform.flip(pygame.transform.scale(pygame.image.load(
                'personagens/cabeça/dwizard.png'), tam_head), True, False).convert_alpha()

            grupo_enemy[c].ataques = ['Basico', 'Envenenamento']
            grupo_enemy[c].defesas = ['Basico', 'Curar-se']

        elif grupo_enemy[c].nome == 'Jorge':
            grupo_enemy[c].image_ingame = pygame.transform.flip(pygame.transform.scale(pygame.image.load(
                'personagens/jorge.png'), tam_char_enemy), True, False).convert_alpha()

            grupo_enemy[c].image_face = pygame.transform.scale(pygame.image.load('personagens/cabeça/jorge.png'),
                                                               tam_head).convert_alpha()

            grupo_enemy[c].ataques = ['Basico', 'Envenenamento', 'Explosão Ossos']
            grupo_enemy[c].defesas = ['Basico', 'Curar-se']

        elif grupo_enemy[c].nome == 'Thiago':
            grupo_enemy[c].image_ingame = pygame.transform.flip(pygame.transform.scale(pygame.image.load(
                'personagens/Thiago.png'), tam_char_enemy), False, False).convert_alpha()

            grupo_enemy[c].image_face = pygame.transform.scale(pygame.image.load('personagens/cabeça/thiago.png'),
                                                               tam_head).convert_alpha()

            grupo_enemy[c].ataques = ['Basico', 'Envenenamento', 'Explosão Ossos']
            grupo_enemy[c].defesas = ['Basico', 'Curar-se']

    batalha(grupo_player, grupo_enemy, dif_head, tipo)


"TODO ABAIXO TODAS AS FUNÇÕES DO MENU"


class Window:
    def __init__(self, window_x, window_y):
        self.window_x = window_x
        self.window_y = window_y

    def get_resolution(self):
        return self.window_x, self.window_y


# Aviso grupo cheio
def aviso_gcheio(rodando_pers):
    """Pequeno aviso mostrando que o grupo está cheio, e, não é possivel adicionar mais personagens no grupo (apenas na
    seleção de personagens)"""

    # Globais
    global janela
    global delta

    # Sprites
    tela_aviso = pygame.transform.scale(pygame.image.load('selecao_menu/avisotela/aviso.png'), (850, 850))\
        .convert_alpha()
    opcao_ok = pygame.transform.scale(pygame.image.load('selecao_menu/ok_s.png'), (325, 325)).convert_alpha()

    # Fontes
    aviso_fonte = pygame.font.Font('alagard.ttf', 46)
    aviso = aviso_fonte.render('Selecione apenas 3 Personagens', False, (0, 0, 0)).convert_alpha()

    # Sons
    confirma_som = pygame.mixer.Sound('sound/confirmar.mp3')

    tela_aviso_aberta = True
    while tela_aviso_aberta:

        janela.blit(tela_aviso, (90, -5))
        janela.blit(aviso, (180, 220))
        janela.blit(opcao_ok, (345, 451))

        for evento_gcheio in pygame.event.get():
            if evento_gcheio.type == pygame.QUIT:
                exit()

            if evento_gcheio.type == pygame.KEYDOWN:

                if evento_gcheio.key == pygame.K_RETURN or evento_gcheio.key == pygame.K_ESCAPE:
                    confirma_som.play()
                    tela_aviso_aberta = False

        delta = ticks.tick(60)
        pygame.display.update()

    return rodando_pers


def selecao_personagens():
    """
    +Função+
    - Destinada a mostrar um menu para que o jogador possa selecionar os personagens, selecionando pelo menos 3 deles
    """
    # Globais
    global janela
    global delta
    global ticks
    global escuro
    global rodando
    global grupo

    # Janela Nome
    pygame.display.set_caption("IntroSouls - Personagens")

    # Fontes Sistema
    pygame.font.init()
    nomes_fonte = pygame.font.Font('alagard.ttf', 65)
    stats_fonte = pygame.font.Font('alagard.ttf', 28)
    select_fonte = pygame.font.Font('alagard.ttf', 42)
    start_fonte = pygame.font.Font('alagard.ttf', 26)
    erro_fonte = pygame.font.Font('alagard.ttf', 30)

    select_text = select_fonte.render('  Selecionar', False, (0, 0, 0)).convert_alpha()
    unselect_text = select_fonte.render('Desselecionar', False, (0, 0, 0)).convert_alpha()

    # Cartas Base
    tamanho_carta = (800, 800)
    y_carta = 50
    carta = pygame.transform.scale(pygame.image.load('personagens/carta.png'), tamanho_carta).convert_alpha()

    # Setas navegação
    tamanho_setas = (500, 500)
    direita = [pygame.transform.scale(pygame.image.load('selecao_menu/direita_uns.png'), tamanho_setas).convert_alpha(),
               pygame.transform.scale(pygame.image.load('selecao_menu/direita_s.png'), tamanho_setas).convert_alpha()]

    esquerda = [
        pygame.transform.scale(pygame.image.load('selecao_menu/esquerda_uns.png'), tamanho_setas).convert_alpha(),
        pygame.transform.scale(pygame.image.load('selecao_menu/esquerda_s.png'), tamanho_setas).convert_alpha()]

    # PERSONAGENS

    # TEXTOS

    # CARREGAR STATS / TEXTO

    vida_max_stats = [stats_fonte.render(str(hunter_stat.vida_max), False, (0, 0, 0)).convert_alpha(),
                      stats_fonte.render(str(priest_stat.vida_max), False, (0, 0, 0)).convert_alpha(),
                      stats_fonte.render(str(paladin_stat.vida_max), False, (0, 0, 0)).convert_alpha(),
                      stats_fonte.render(str(wizard_stat.vida_max), False, (0, 0, 0)).convert_alpha(),
                      stats_fonte.render(str(rogue_stat.vida_max), False, (0, 0, 0)).convert_alpha()]

    ataque_stats = [stats_fonte.render(str(hunter_stat.ataque), False, (0, 0, 0)).convert_alpha(),
                    stats_fonte.render(str(priest_stat.ataque), False, (0, 0, 0)).convert_alpha(),
                    stats_fonte.render(str(paladin_stat.ataque), False, (0, 0, 0)).convert_alpha(),
                    stats_fonte.render(str(wizard_stat.ataque), False, (0, 0, 0)).convert_alpha(),
                    stats_fonte.render(str(rogue_stat.ataque), False, (0, 0, 0)).convert_alpha()]

    defesa_stats = [stats_fonte.render(str(hunter_stat.defesa), False, (0, 0, 0)).convert_alpha(),
                    stats_fonte.render(str(priest_stat.defesa), False, (0, 0, 0)).convert_alpha(),
                    stats_fonte.render(str(paladin_stat.defesa), False, (0, 0, 0)).convert_alpha(),
                    stats_fonte.render(str(wizard_stat.defesa), False, (0, 0, 0)).convert_alpha(),
                    stats_fonte.render(str(rogue_stat.defesa), False, (0, 0, 0)).convert_alpha()]

    mana_max_stats = [stats_fonte.render(str(hunter_stat.mana_max), False, (0, 0, 0)).convert_alpha(),
                      stats_fonte.render(str(priest_stat.mana_max), False, (0, 0, 0)).convert_alpha(),
                      stats_fonte.render(str(paladin_stat.mana_max), False, (0, 0, 0)).convert_alpha(),
                      stats_fonte.render(str(wizard_stat.mana_max), False, (0, 0, 0)).convert_alpha(),
                      stats_fonte.render(str(rogue_stat.mana_max), False, (0, 0, 0)).convert_alpha()]

    iniciativa_stats = [stats_fonte.render(str(hunter_stat.iniciativa), False, (0, 0, 0)).convert_alpha(),
                        stats_fonte.render(str(priest_stat.iniciativa), False, (0, 0, 0)).convert_alpha(),
                        stats_fonte.render(str(paladin_stat.iniciativa), False, (0, 0, 0)).convert_alpha(),
                        stats_fonte.render(str(wizard_stat.iniciativa), False, (0, 0, 0)).convert_alpha(),
                        stats_fonte.render(str(rogue_stat.iniciativa), False, (0, 0, 0)).convert_alpha()]

    # Posição Y dos stats
    y_stats_1 = 525
    y_stats_2 = 595

    # NOMES
    # Posição Y dos nomes
    y_nomes = 75
    nomes = [nomes_fonte.render(hunter_stat.nome, False, (0, 0, 0)).convert_alpha(),
             nomes_fonte.render(priest_stat.nome, False, (0, 0, 0)).convert_alpha(),
             nomes_fonte.render(paladin_stat.nome, False, (0, 0, 0)).convert_alpha(),
             nomes_fonte.render(wizard_stat.nome, False, (0, 0, 0)).convert_alpha(),
             nomes_fonte.render(rogue_stat.nome, False, (0, 0, 0)).convert_alpha()]

    # Carregar sprites / Normal
    # Posição Y dos personagens
    y_personagens = 125
    tam_pers = (200, 200)

    # Tamanho Hunter, Wizard e Rogue diferente dos outros devido ao seu tamanho maior
    hunter = pygame.transform.scale(pygame.image.load('personagens/hunter sprite.png'), (170, 170)).convert_alpha()
    wizard = pygame.transform.scale(pygame.image.load('personagens/wizardfinal.png'), (180, 180)).convert_alpha()
    rogue = pygame.transform.scale(pygame.image.load('personagens/rogue.png'), (170, 170)).convert_alpha()

    priest = pygame.transform.scale(pygame.image.load('personagens/PRIEST_NoShadow.png'), tam_pers).convert_alpha()
    paladino = pygame.transform.scale(pygame.image.load('personagens/Paladino.png'), tam_pers).convert_alpha()

    # Carregar sprites / Cabeça
    # Posição Y das cabeças
    y_head = 355
    tam_head = (135, 135)

    # Tamanho da cabeça Wizard diferente dos outros devido ao seu tamanho maior
    wizard_h = pygame.transform.scale(pygame.image.load('personagens/cabeça/wizard.png'), (107, 107)).convert_alpha()

    hunter_h = pygame.transform.scale(pygame.image.load('personagens/cabeça/hunter.png'), tam_head).convert_alpha()
    priest_h = pygame.transform.scale(pygame.image.load('personagens/cabeça/priest.png'), tam_head).convert_alpha()
    paladino_h = pygame.transform.scale(pygame.image.load('personagens/cabeça/paladino.png'), tam_head).convert_alpha()
    rogue_h = pygame.transform.scale(pygame.image.load('personagens/cabeça/rogue.png'), tam_head).convert_alpha()

    # Ícones / Stats
    icone_tam = (50, 50)
    # VIDA E MANA
    # Valores 0 = Vida/Mana Cheias
    # Valores 1 = Vida/Mana Vazias
    # Strong = Stat Forte

    # O RESTANTE
    # Valores 0 = Stat Normal
    # Valores 1 = Stat Forte

    # Ataque
    attack = [pygame.transform.scale(pygame.image.load('cartas_icon/attack.png'), icone_tam).convert_alpha(),
              pygame.transform.scale(pygame.image.load('cartas_icon/attack_strong.png'), icone_tam).convert_alpha()]
    y_attack = 476

    # Coração
    heart = [pygame.transform.scale(pygame.image.load('cartas_icon/heart.png'), icone_tam).convert_alpha(),
             pygame.transform.scale(pygame.image.load('cartas_icon/heart_empty.png'), icone_tam).convert_alpha()]

    heart_strong = [
        pygame.transform.scale(pygame.image.load('cartas_icon/paladin_heart.png'), icone_tam).convert_alpha(),

        pygame.transform.scale(pygame.image.load('cartas_icon/paladin_heart_empty.png'), icone_tam)
              .convert_alpha()]
    y_heart = 475

    # Mana
    mana = [pygame.transform.scale(pygame.image.load('cartas_icon/mana.png'), icone_tam).convert_alpha(),
            pygame.transform.scale(pygame.image.load('cartas_icon/mana_empty.png'), icone_tam).convert_alpha()]

    mana_strong = [pygame.transform.scale(pygame.image.load('cartas_icon/mana_s.png'), icone_tam).convert_alpha(),
                   pygame.transform.scale(pygame.image.load('cartas_icon/mana_s_empty.png'), icone_tam).convert_alpha()]
    y_mana = 550

    # Escudo
    shield = [pygame.transform.scale(pygame.image.load('cartas_icon/shield.png'), icone_tam).convert_alpha(),
              pygame.transform.scale(pygame.image.load('cartas_icon/paladin_shield.png'), icone_tam).convert_alpha()]
    y_shield = 475

    # Iniciativa
    initiative = [pygame.transform.scale(pygame.image.load('cartas_icon/initiative.png'), icone_tam).convert_alpha(),
                  pygame.transform.scale(pygame.image.load('cartas_icon/initiative_s.png'), icone_tam).convert_alpha()]
    y_initiative = 546

    # Icone vida
    icone_vida = pygame.transform.scale(pygame.image.load('barras_vida/Vida_Cheia.png'), (250, 250)).convert_alpha()
    y_vida = y_carta + 230

    # Teste Fundo
    fundo_personagens = pygame.transform.scale(pygame.image.load('batalha/fundo_game.png'), (1324, 1068))\
        .convert_alpha()

    # Localização fixa das cartas
    carta_posicoes_x = [-1040, -460, 120, 700, 1280]

    # Grupo / Seleção de Personagens
    grupo = []

    select = [pygame.transform.scale(pygame.image.load('personagens/Selecionado_grupo/select_uns.png'), (301, 213))
                    .convert_alpha(),

              pygame.transform.scale(pygame.image.load('personagens/Selecionado_grupo/select_s.png'), (301, 213))
                    .convert_alpha()]

    unselect = [pygame.transform.scale(pygame.image.load('personagens/Selecionado_grupo/unselect_uns.png'), (301, 213))
                      .convert_alpha(),

                pygame.transform.scale(pygame.image.load('personagens/Selecionado_grupo/unselect_s.png'), (301, 213))
                      .convert_alpha()]

    selecionado_grupo = [0, 0, 0, 0, 0]

    y_selecionar = 550
    y_select_text = 635

    # Sistema mostrar grupo
    grupo_sprite = pygame.transform.scale(pygame.image.load('selecao_menu/grupo_base.png'), (655, 655)).convert_alpha()

    # Posição grupo_base / atual / destino
    pos_grupo_atual = 501

    # Sprite icone da cabeça do personagem
    icone_cabeca_grupo = pygame.transform.scale(pygame.image.load('personagens/cabeça/icone_cabeca.png'), (223, 223)) \
        .convert_alpha()

    # Posição carta 1 (Quando outras cartas estão selecionadas)
    carta1_pos = [140, -450, -1040, -1630, -2220]

    # Escuro / Fade Out / Fade In

    # Resetar transparência
    escuro.set_alpha(255)

    fade_out = [True]
    fade_in = [False]
    fade_transparencia = 255

    # Aviso iniciar jogo
    aviso_iniciar = pygame.transform.scale(pygame.image.load('teclas/aviso_3.png'), (342, 342)).convert_alpha()
    espaco = pygame.transform.scale(pygame.image.load('teclas/spacebar.png'), (155, 155)).convert_alpha()
    start_text = start_fonte.render('Para iniciar!', False, (0, 0, 0)).convert_alpha()
    aviso_iniciar_pos = 586

    # Primeira tecla apertada
    primeiro_mov = False

    # MENSAGEM ERRO AO INICIAR JOGO
    erro_start_time = 0
    erro_start_pos = 680
    erro_aviso = pygame.transform.scale(pygame.image.load('teclas/aviso_3.png'), (400, 400)).convert_alpha()

    # Liberar o jogador de executar comandos no teclado
    selecionar_comando = False

    # Sons
    confirma_som = pygame.mixer.Sound('sound/confirmar.mp3')
    navegar_menu_som = pygame.mixer.Sound('sound/navegar_menu.mp3')

    rodando_pers = True
    movimentando = [False]
    while rodando_pers:
        # Resetar Estado Setas: Selecionado -> Não Selecionado
        seta_direita_s = 0
        seta_esquerda_s = 0

        # Animação Trocar Carta
        if movimentando[0]:

            if movimentando[1] == 'R':

                if carta_posicoes_x[0] <= movimentando[2]:
                    for i in range(0, 5):
                        carta_posicoes_x[i] += 10
                else:
                    movimentando = [False]

            elif movimentando[1] == 'L':

                if carta_posicoes_x[0] >= movimentando[2]:
                    for i in range(0, 5):
                        carta_posicoes_x[i] -= 10
                else:
                    movimentando = [False]

        janela.blit(fundo_personagens, (-149, -280))

        # Mostrar Cartas e ícones de cada um
        # Carta 1
        janela.blit(carta, (carta_posicoes_x[0] - 20, y_carta))

        # Vida/1
        janela.blit(icone_vida, (carta_posicoes_x[0] + 245, y_vida))

        # Stats 1 linha/1
        janela.blit(heart[0], ((carta_posicoes_x[0] + 245) - 20, y_heart))
        janela.blit(attack[0], ((carta_posicoes_x[0] + 375) - 20, y_attack))
        janela.blit(shield[0], ((carta_posicoes_x[0] + 500) - 20, y_shield))

        # Stats 2 linha/1
        janela.blit(mana_strong[0], ((carta_posicoes_x[0] + 240) - 20, y_mana))
        janela.blit(initiative[1], ((carta_posicoes_x[0] + 375) - 20, y_initiative))

        # Personagem / Hunter /1
        janela.blit(hunter, ((carta_posicoes_x[0] + 290), y_personagens + 15))

        # Nome/1
        janela.blit(nomes[0], (carta_posicoes_x[0] + 271, y_nomes))

        # Cabeça/1
        janela.blit(hunter_h, (carta_posicoes_x[0] + 235, y_head))

        # Stats Texto/1

        # Linha 1 /1
        janela.blit(vida_max_stats[0], (carta_posicoes_x[0] + 231, y_stats_1))
        janela.blit(ataque_stats[0], (carta_posicoes_x[0] + 370, y_stats_1))
        janela.blit(defesa_stats[0], (carta_posicoes_x[0] + 493, y_stats_1))

        # Linha 2 /1
        janela.blit(mana_max_stats[0], (carta_posicoes_x[0] + 236, y_stats_2))
        janela.blit(iniciativa_stats[0], (carta_posicoes_x[0] + 370, y_stats_2))

        # Carta 2
        janela.blit(carta, (carta_posicoes_x[1] - 15, y_carta))

        # Vida/2
        janela.blit(icone_vida, (carta_posicoes_x[1] + 245, y_vida))

        # Stats 1 linha/2
        janela.blit(heart[0], ((carta_posicoes_x[1] + 245) - 15, y_heart))
        janela.blit(attack[0], ((carta_posicoes_x[1] + 375) - 15, y_attack))
        janela.blit(shield[0], ((carta_posicoes_x[1] + 500) - 15, y_shield))

        # Stats 2 linha/2
        janela.blit(mana_strong[0], ((carta_posicoes_x[1] + 240) - 15, y_mana))
        janela.blit(initiative[1], ((carta_posicoes_x[1] + 375) - 15, y_initiative))

        # Personagem / Priest /2
        janela.blit(priest, ((carta_posicoes_x[1] + 290), y_personagens))

        # Nome/2
        janela.blit(nomes[1], (carta_posicoes_x[1] + 290, y_nomes))

        # Cabeça/2
        janela.blit(priest_h, (carta_posicoes_x[1] + 231, y_head))

        # Stats Texto/2

        # Linha 1 /2
        janela.blit(vida_max_stats[1], (carta_posicoes_x[1] + 237, y_stats_1))
        janela.blit(ataque_stats[1], (carta_posicoes_x[1] + 375, y_stats_1))
        janela.blit(defesa_stats[1], (carta_posicoes_x[1] + 504, y_stats_1))

        # Linha 2 /2
        janela.blit(mana_max_stats[1], (carta_posicoes_x[1] + 237, y_stats_2))
        janela.blit(iniciativa_stats[1], (carta_posicoes_x[1] + 375, y_stats_2))

        # Carta 3
        janela.blit(carta, (carta_posicoes_x[2], y_carta))

        # Vida/3
        janela.blit(icone_vida, (carta_posicoes_x[2] + 260, y_vida))

        # Stats 1 linha/3
        janela.blit(heart_strong[0], (carta_posicoes_x[2] + 245, y_heart))
        janela.blit(attack[1], (carta_posicoes_x[2] + 375, y_attack))
        janela.blit(shield[1], (carta_posicoes_x[2] + 500, y_shield))

        # Stats 2 linha/3
        janela.blit(mana[0], (carta_posicoes_x[2] + 240, y_mana))
        janela.blit(initiative[0], (carta_posicoes_x[2] + 375, y_initiative))

        # Personagem / Paladino /3
        janela.blit(paladino, (carta_posicoes_x[2] + 290, y_personagens))

        # Nome/3
        janela.blit(nomes[2], (carta_posicoes_x[2] + 285, y_nomes))

        # Cabeça/3
        janela.blit(paladino_h, (carta_posicoes_x[2] + 231, y_head))

        # Stats Texto/3

        # Linha 1 /3
        janela.blit(vida_max_stats[2], (carta_posicoes_x[2] + 250, y_stats_1))
        janela.blit(ataque_stats[2], (carta_posicoes_x[2] + 385, y_stats_1))
        janela.blit(defesa_stats[2], (carta_posicoes_x[2] + 510, y_stats_1))

        # Linha 2 /3
        janela.blit(mana_max_stats[2], (carta_posicoes_x[2] + 261, y_stats_2))
        janela.blit(iniciativa_stats[2], (carta_posicoes_x[2] + 392, y_stats_2))

        # Carta 4
        janela.blit(carta, (carta_posicoes_x[3] + 10, y_carta))

        # Vida/4
        janela.blit(icone_vida, (carta_posicoes_x[3] + 270, y_vida))

        # Stats 1 linha/4
        janela.blit(heart[0], ((carta_posicoes_x[3] + 245) + 10, y_heart))
        janela.blit(attack[1], ((carta_posicoes_x[3] + 375) + 10, y_attack))
        janela.blit(shield[0], ((carta_posicoes_x[3] + 500) + 10, y_shield))

        # Stats 2 linha/4
        janela.blit(mana_strong[0], ((carta_posicoes_x[3] + 240) + 10, y_mana))
        janela.blit(initiative[0], ((carta_posicoes_x[3] + 375) + 10, y_initiative))

        # Personagem / Wizard /4
        janela.blit(wizard, (carta_posicoes_x[3] + 310, y_personagens + 8))

        # Nome/4
        janela.blit(nomes[3], (carta_posicoes_x[3] + 305, y_nomes))

        # Cabeça/4
        janela.blit(wizard_h, (carta_posicoes_x[3] + 270, y_head + 8))

        # Stats Texto/4

        # Linha 1 /4
        janela.blit(vida_max_stats[3], (carta_posicoes_x[3] + 265, y_stats_1))
        janela.blit(ataque_stats[3], (carta_posicoes_x[3] + 397, y_stats_1))
        janela.blit(defesa_stats[3], (carta_posicoes_x[3] + 525, y_stats_1))

        # Linha 2 /4
        janela.blit(mana_max_stats[3], (carta_posicoes_x[3] + 265, y_stats_2))
        janela.blit(iniciativa_stats[3], (carta_posicoes_x[3] + 397, y_stats_2))

        # Carta 5
        janela.blit(carta, (carta_posicoes_x[4] + 20, y_carta))

        # Vida/5
        janela.blit(icone_vida, (carta_posicoes_x[4] + 280, y_vida))

        # Stats 1 linha/5
        janela.blit(heart[0], ((carta_posicoes_x[4] + 245) + 20, y_heart))
        janela.blit(attack[0], ((carta_posicoes_x[4] + 375) + 20, y_attack))
        janela.blit(shield[0], ((carta_posicoes_x[4] + 500) + 20, y_shield))

        # Stats 2 linha/5
        janela.blit(mana[0], ((carta_posicoes_x[4] + 240) + 20, y_mana))
        janela.blit(initiative[1], ((carta_posicoes_x[4] + 375) + 20, y_initiative))

        # Personagem / Rogue /5
        janela.blit(rogue, (carta_posicoes_x[4] + 330, y_personagens + 15))

        # Nome/5
        janela.blit(nomes[4], (carta_posicoes_x[4] + 325, y_nomes))

        # Cabeça/5
        janela.blit(rogue_h, (carta_posicoes_x[4] + 270, y_head))

        # Stats Texto/5

        # Linha 1 /5
        janela.blit(vida_max_stats[4], (carta_posicoes_x[4] + 272, y_stats_1))
        janela.blit(ataque_stats[4], (carta_posicoes_x[4] + 410, y_stats_1))
        janela.blit(defesa_stats[4], (carta_posicoes_x[4] + 535, y_stats_1))

        # Linha 2 /5
        janela.blit(mana_max_stats[4], (carta_posicoes_x[4] + 277, y_stats_2))
        janela.blit(iniciativa_stats[4], (carta_posicoes_x[4] + 407, y_stats_2))

        # Sistema seleção personagens
        opcao = []
        opcao_text = []

        for index in range(0, 5):

            if selecionado_grupo[index] == 0:

                if carta_posicoes_x[0] == carta1_pos[index]:
                    opcao.append(select[1])
                else:
                    opcao.append(select[0])

                opcao_text.append(select_text)

            elif selecionado_grupo[index] == 1:

                if carta_posicoes_x[0] == carta1_pos[index]:
                    opcao.append(unselect[1])
                else:
                    opcao.append(unselect[0])

                opcao_text.append(unselect_text)

        janela.blit(opcao[0], (carta_posicoes_x[0] + 222, y_selecionar))
        janela.blit(opcao_text[0], (carta_posicoes_x[0] + 243, y_select_text))

        janela.blit(opcao[1], (carta_posicoes_x[1] + 228, y_selecionar))
        janela.blit(opcao_text[1], (carta_posicoes_x[1] + 250, y_select_text))

        janela.blit(opcao[2], (carta_posicoes_x[2] + 243, y_selecionar))
        janela.blit(opcao_text[2], (carta_posicoes_x[2] + 264, y_select_text))

        janela.blit(opcao[3], (carta_posicoes_x[3] + 253, y_selecionar))
        janela.blit(opcao_text[3], (carta_posicoes_x[3] + 275, y_select_text))

        janela.blit(opcao[4], (carta_posicoes_x[4] + 263, y_selecionar))
        janela.blit(opcao_text[4], (carta_posicoes_x[4] + 285, y_select_text))

        # Mostrar o seu grupo / Personagens que foram selecionados
        # 389 -> valor y para mostrar o sprite
        # 501 -> valor y para esconder o sprite

        # Sprite grupo_base
        # Caso não tenha nenhum personagem selecionado, o sprite se esconde
        if selecionado_grupo.count(1) > 0:
            pos_grupo = 389
        else:
            pos_grupo = 501

        # Animação sprite aparecendo e se escondendo
        if pos_grupo_atual != pos_grupo:

            if pos_grupo_atual < pos_grupo:
                pos_grupo_atual += 2
            elif pos_grupo_atual > pos_grupo:
                pos_grupo_atual -= 2

        # Mostrar sprite
        janela.blit(grupo_sprite, (542, pos_grupo_atual))

        # Mostrar personagens selecionados no grupo_sprite
        # X -> [1: 664, 2: 756, 3: 849]
        # Y FIXO -> 603

        # Reiniciar grupo para recolocar
        grupo_mostrar = []

        # Ajustas as cabeças no icone corretamente
        grupo_ajustar_x = []
        grupo_ajustar_y = []

        grupo_posicoes_x = [664, 756, 849]

        # Sistema para guardar todos os personagens selecionados no grupo
        for i in range(0, 5):

            if selecionado_grupo[i] == 1:

                if i == 0:
                    grupo_mostrar.append(hunter_h)
                    grupo_ajustar_x.append(58)
                    grupo_ajustar_y.append(68)
                elif i == 1:
                    grupo_mostrar.append(priest_h)
                    grupo_ajustar_x.append(50)
                    grupo_ajustar_y.append(70)
                elif i == 2:
                    grupo_mostrar.append(paladino_h)
                    grupo_ajustar_x.append(34)
                    grupo_ajustar_y.append(70)
                elif i == 3:
                    grupo_mostrar.append(wizard_h)
                    grupo_ajustar_x.append(64)
                    grupo_ajustar_y.append(78)
                elif i == 4:
                    grupo_mostrar.append(rogue_h)
                    grupo_ajustar_x.append(54)
                    grupo_ajustar_y.append(70)

        # Mostrar grupo na tela / acima do grupo_sprite
        if pos_grupo_atual == 389:

            for i in range(0, len(grupo_mostrar)):
                janela.blit(icone_cabeca_grupo, (grupo_posicoes_x[i], 603))
                janela.blit(grupo_mostrar[i], (grupo_posicoes_x[i] + grupo_ajustar_x[i], 603 + grupo_ajustar_y[i]))

        # Mostrar a tecla para continuar / Depois de selecionar todos / Ao iniciar o jogo
        # X -> FIXO = -12
        # Y -> Amostra: 586 Escondido: 693

        # Posição alvo do aviso para iniciar o jogo
        if selecionado_grupo.count(1) == 3:
            aviso_iniciar_trgt = 586

        elif not primeiro_mov:
            aviso_iniciar_trgt = 586

        else:
            aviso_iniciar_trgt = 693

        # Animação Aviso para iniciar o jogo
        if aviso_iniciar_pos > aviso_iniciar_trgt:
            aviso_iniciar_pos -= 3

        if aviso_iniciar_pos < aviso_iniciar_trgt:
            aviso_iniciar_pos += 3

        janela.blit(aviso_iniciar, (-12, aviso_iniciar_pos))
        janela.blit(espaco, (-12 + 20, aviso_iniciar_pos + 53))
        janela.blit(start_text, (-12 + 169, aviso_iniciar_pos + 116))

        # Atualizar Personagens faltando
        personagens_faltando = 3 - selecionado_grupo.count(1)

        if personagens_faltando > 1:
            erro_text = erro_fonte.render(f'Selecione {personagens_faltando} Personagens', False,
                                          (0, 0, 0)).convert_alpha()
        else:
            erro_text = erro_fonte.render(f'Selecione {personagens_faltando} Personagem', False,
                                          (0, 0, 0)).convert_alpha()

        # Mostrar erro ao iniciar o jogo / Falta personagens para selecionar
        # X FIXO -> 314
        # Y -> Amostra: 300 Escondido: 680
        janela.blit(erro_aviso, (314, erro_start_pos))

        if personagens_faltando > 1:
            janela.blit(erro_text, (314 + 32, erro_start_pos + 136))
        else:
            janela.blit(erro_text, (314 + 38, erro_start_pos + 136))

        # Verificar se o tempo para mostrar a mensagem de erro terminou
        if erro_start_time != 0:
            erro_start_time -= 1
            erro_start_trgt = 300
        else:
            erro_start_trgt = 680

        # Animação mensagem de erro
        if erro_start_pos > erro_start_trgt:
            erro_start_pos -= 10

        if erro_start_pos < erro_start_trgt:
            erro_start_pos += 10

        # Eventos
        for evento_pers in pygame.event.get():
            if evento_pers.type == pygame.QUIT:
                exit()

            if evento_pers.type == pygame.KEYDOWN and selecionar_comando:

                if evento_pers.key == pygame.K_RIGHT:
                    seta_direita_s = 1

                    if not movimentando[0] and carta_posicoes_x[4] > 100:
                        navegar_menu_som.play()
                        movimentando = [True, 'L', carta_posicoes_x[0] - 580]

                if evento_pers.key == pygame.K_LEFT:
                    seta_esquerda_s = 1

                    if not movimentando[0] and carta_posicoes_x[0] < 140:
                        navegar_menu_som.play()
                        movimentando = [True, 'R', carta_posicoes_x[0] + 580]

                # Sistema Selecionar Personagem ao apertar ENTER
                if evento_pers.key == pygame.K_RETURN:

                    if carta_posicoes_x[0] in carta1_pos:

                        if carta_posicoes_x[0] == carta1_pos[0]:

                            if selecionado_grupo[0] == 0:

                                if selecionado_grupo.count(1) < 3:
                                    confirma_som.play()
                                    selecionado_grupo[0] = 1
                                else:
                                    confirma_som.play()
                                    rodando_pers = aviso_gcheio(rodando_pers)

                            elif selecionado_grupo[0] == 1:
                                confirma_som.play()
                                selecionado_grupo[0] = 0

                        if carta_posicoes_x[0] == carta1_pos[1]:

                            if selecionado_grupo[1] == 0:

                                if selecionado_grupo.count(1) < 3:
                                    confirma_som.play()
                                    selecionado_grupo[1] = 1
                                else:
                                    confirma_som.play()
                                    rodando_pers = aviso_gcheio(rodando_pers)

                            elif selecionado_grupo[1] == 1:
                                confirma_som.play()
                                selecionado_grupo[1] = 0

                        if carta_posicoes_x[0] == carta1_pos[2]:

                            if selecionado_grupo[2] == 0:

                                if selecionado_grupo.count(1) < 3:
                                    confirma_som.play()
                                    selecionado_grupo[2] = 1
                                else:
                                    confirma_som.play()
                                    rodando_pers = aviso_gcheio(rodando_pers)

                            elif selecionado_grupo[2] == 1:
                                confirma_som.play()
                                selecionado_grupo[2] = 0

                        if carta_posicoes_x[0] == carta1_pos[3]:

                            if selecionado_grupo[3] == 0:

                                if selecionado_grupo.count(1) < 3:
                                    confirma_som.play()
                                    selecionado_grupo[3] = 1
                                else:
                                    confirma_som.play()
                                    rodando_pers = aviso_gcheio(rodando_pers)

                            elif selecionado_grupo[3] == 1:
                                confirma_som.play()
                                selecionado_grupo[3] = 0

                        if carta_posicoes_x[0] == carta1_pos[4]:

                            if selecionado_grupo[4] == 0:

                                if selecionado_grupo.count(1) < 3:
                                    confirma_som.play()
                                    selecionado_grupo[4] = 1
                                else:
                                    confirma_som.play()
                                    rodando_pers = aviso_gcheio(rodando_pers)

                            elif selecionado_grupo[4] == 1:
                                confirma_som.play()
                                selecionado_grupo[4] = 0

                if evento_pers.key == pygame.K_SPACE:

                    # Mostrar Erro ao selecionar menos de 3 personagens
                    if selecionado_grupo.count(1) != 3:
                        erro_start_time = 180
                    else:

                        # Verificar selecionados e colocar no grupo
                        for i in range(0, 5):

                            if selecionado_grupo[i] == 1:

                                if i == 0:
                                    grupo.append('hunter')
                                elif i == 1:
                                    grupo.append('priest')
                                elif i == 2:
                                    grupo.append('paladin')
                                elif i == 3:
                                    grupo.append('wizard')
                                elif i == 4:
                                    grupo.append('rogue')

                                confirma_som.play()
                                fade_in = [True, 'space']

                # Voltar pro menu inicial com efeito fade in
                if evento_pers.key == pygame.K_ESCAPE:
                    confirma_som.play()
                    fade_in = [True, 'escape']

                # Marcar que o primeiro movimento ja foi executado
                if not primeiro_mov:
                    primeiro_mov = True

        # Mostrar setas / Selecionadas ou não
        janela.blit(direita[seta_direita_s], (550, 165))
        janela.blit(esquerda[seta_esquerda_s], (-15, 165))

        # Fade Out
        if fade_out[0]:

            if fade_transparencia > 0:

                fade_transparencia -= 8
                escuro.set_alpha(fade_transparencia)
            else:
                fade_out = [False]
                selecionar_comando = True

            janela.blit(escuro, (0, 0))

        # Fade In
        if fade_in[0]:

            selecionar_comando = False

            if fade_transparencia < 255:

                fade_transparencia += 8
                escuro.set_alpha(fade_transparencia)

            else:

                if fade_in[1] == 'escape':
                    rodando_pers = False
                elif fade_in[1] == 'space':
                    pygame.mixer.music.stop()
                    tela_carregar(grupo)

            janela.blit(escuro, (0, 0))

        delta = ticks.tick(60)
        pygame.display.update()


# Função para tela de sair do jogo
def confirma_sair():
    """
    +Função+
     - Mostra uma tela confirmando ao jogador se realmente quer sair, contendo as opções SIM e NÃO.
    """

    # Sprites
    tela_sair = pygame.transform.scale(pygame.image.load('menu_sair/tela.png'), (850, 850)).convert_alpha()

    sim = [pygame.transform.scale(pygame.image.load('selecao_menu/sim_uns.png'), (325, 325)).convert_alpha(),
           pygame.transform.scale(pygame.image.load('selecao_menu/sim_s.png'), (325, 325)).convert_alpha()]

    nao = [pygame.transform.scale(pygame.image.load('selecao_menu/nao_uns.png'), (325, 325)).convert_alpha(),
           pygame.transform.scale(pygame.image.load('selecao_menu/nao_s.png'), (325, 325)).convert_alpha()]

    # Variáveis
    global rodando
    global janela
    global delta

    sair_selecionado = "nao"
    sair_rodando = True

    # Mudar nome da janela
    pygame.display.set_caption("IntroSouls - Sair?")

    # Sons
    confirma_som = pygame.mixer.Sound('sound/confirmar.mp3')
    navegar_menu_som = pygame.mixer.Sound('sound/navegar_menu.mp3')

    while sair_rodando:

        # Mostrar tela de sair
        janela.blit(tela_sair, (90, -5))

        # Mostrar opções
        if sair_selecionado == "sim":
            janela.blit(sim[1], (340, 270))
            janela.blit(nao[0], (340, 445))
        elif sair_selecionado == "nao":
            janela.blit(sim[0], (340, 270))
            janela.blit(nao[1], (340, 445))

        # Eventos
        for evento_sair in pygame.event.get():

            if evento_sair.type == pygame.QUIT:
                exit()

            if evento_sair.type == pygame.KEYDOWN:

                if evento_sair.key == pygame.K_DOWN:
                    navegar_menu_som.play()
                    sair_selecionado = "nao"

                if evento_sair.key == pygame.K_UP:
                    navegar_menu_som.play()
                    sair_selecionado = "sim"

                if evento_sair.key == pygame.K_RETURN:

                    if sair_selecionado == "sim":
                        exit()
                    else:
                        confirma_som.play()
                        sair_rodando = False

                if evento_sair.key == pygame.K_BACKSPACE:
                    sair_rodando = False

        # Atualizar tela
        delta = ticks.tick(60)
        pygame.display.update()


def tela_carregar(grupo_jogadores, tipo=''):
    """
    +Função+
    - Mostra uma tela de carregamento antes da batalha começar.
    """
    # Variáveis
    global janela
    global delta
    global ticks
    global rodando
    global escuro

    # Janela Nome
    pygame.display.set_caption("IntroSouls - Carregando...")

    # Telas de carregamento
    tela_loading = pygame.transform.scale(pygame.image.load('tela_loading/tela_loading.png'), (1024, 768))\
        .convert_alpha()
    tela_reversed = pygame.transform.flip(tela_loading, True, False).convert_alpha()

    # Icone carregando
    tamanho_icone = (250, 250)
    icone = []
    for a in range(0, 9):
        icone.append(pygame.transform.scale(pygame.image.load(f'tela_loading/frame/{a}.png').convert_alpha(),
                                            tamanho_icone))

    intervalo_icone = 0
    icone_mostrar = 0

    # Tempo e execução
    running = True

    # Movimento tela
    x_loading = 0

    # Fade out
    fade_out_carregamento = True
    fade_in_carregamento = False
    fade_transparencia_carregamento = 255

    # Travada dramática
    sleep(random.randint(1, 3))

    # Tempo de loading dramático
    tempo_parar_loading = random.randint(500, 1200)

    # Frames
    frames = 0

    # Musica
    pygame.mixer.music.load('sound/Loading.wav')
    pygame.mixer.music.play(-1)
    while running:

        x_loading -= 0.6
        janela.blit(tela_loading, (x_loading, 0))
        janela.blit(tela_reversed, (x_loading + 768, 0))

        if intervalo_icone > 6:

            if icone_mostrar >= 8:
                icone_mostrar = 1
            else:
                icone_mostrar += 1

            intervalo_icone = 0

        janela.blit(icone[icone_mostrar], (800, 550))

        if frames > tempo_parar_loading:
            fade_in_carregamento = True

        for evento_carregar in pygame.event.get():
            if evento_carregar.type == pygame.QUIT:
                exit()

        intervalo_icone += 1

        # Fade out
        if fade_out_carregamento:

            if fade_transparencia_carregamento > 0:
                fade_transparencia_carregamento -= 8
                escuro.set_alpha(fade_transparencia_carregamento)

            else:
                fade_out_carregamento = False

            janela.blit(escuro, (0, 0))

        # Fade in
        if fade_in_carregamento:

            if fade_transparencia_carregamento < 255:
                fade_transparencia_carregamento += 8
                escuro.set_alpha(fade_transparencia_carregamento)

            else:
                pygame.mixer.music.stop()
                preparar_batalha(grupo_jogadores, tipo)

            janela.blit(escuro, (0, 0))

        delta = ticks.tick(60)
        pygame.display.update()
        # tela de carregamento vai de 500 ticks a 1200

        # Frames
        frames += 1


def iniciar_jogo():
    """
    +Função+
    - Inicia o jogo, mostrando uma pequena tela de carregamento e intruções para começar a jogar
    """
    # Globais
    global ticks
    global delta

    # Sprites
    escuro_iniciar = pygame.transform.scale(pygame.image.load('transicao/escuro.png'), (1024, 768)).convert_alpha()
    logo = [pygame.transform.scale(pygame.image.load('logo/chave_esquerda.png'), (300, 300)).convert_alpha(),
            pygame.transform.scale(pygame.image.load('logo/INTRO.png'), (300, 300)).convert_alpha(),
            pygame.transform.scale(pygame.image.load('logo/SOULS.png'), (300, 300)).convert_alpha(),
            pygame.transform.scale(pygame.image.load('logo/chave_direita.png'), (300, 300)).convert_alpha()]

    fade_out = False
    fade_transparencia = 255

    # Sprite Icone carregando
    carregando_icone = []
    for ca in range(0, 9):
        carregando_icone.append(pygame.transform.scale(pygame.image.load(f'tela_loading/frame/{ca}.png'), (400, 400))
                                .convert_alpha())
    tick_carregando = 0
    tick_selected = 0
    tempo_carregamento = random.randint(400, 600)
    carregamento_tick = 0

    # Nome Janela
    pygame.display.set_caption("IntroSouls")

    start_rodando = True
    while start_rodando:
        janela.blit(escuro_iniciar, (0, 0))

        # Logo
        janela.blit(logo[0], (38, 90))
        janela.blit(logo[1], (208, 130))
        janela.blit(logo[2], (523, 130))
        janela.blit(logo[3], (698, 90))

        # Icone carregamento / Sistema
        if carregamento_tick > 100 and not fade_out:
            janela.blit(carregando_icone[tick_selected], (315, 200))

            if tick_carregando < 10:
                tick_carregando += 1
            else:

                if tick_selected >= 8:
                    tick_selected = 1
                else:
                    tick_selected += 1

                tick_carregando = 0

        # Criar um tempo para o jogo "carregar"
        carregamento_tick += 1
        if carregamento_tick >= tempo_carregamento:
            fade_out = True

        # Eventos
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                exit()

        # Fade Out
        if fade_out:

            if fade_transparencia > 0:
                fade_transparencia -= 4
            else:
                tutorial_teclas()

            for item in logo:
                item.set_alpha(fade_transparencia)

        pygame.display.update()
        delta = ticks.tick(60)


def tutorial_teclas():
    """
    +Função+
    - Função destinada a mostrar um tutorial mostrando as teclas
    """
    # Globais
    global ticks
    global delta

    # Sprite Opção Ok
    ok = pygame.transform.scale(pygame.image.load("selecao_menu/ok_s.png"), (350, 350)).convert_alpha()

    # Sprite Comandos
    comandos = pygame.image.load('teclas/comandos.png').convert_alpha()
    comandos.set_alpha(0)

    fade_in = True
    fade_out = False
    fade_transparencia = 0

    controle_travado = True

    # Escuro
    escuro_comandos = pygame.transform.scale(pygame.image.load('transicao/escuro.png'), (1024, 768)).convert_alpha()

    # Som
    confirma_som = pygame.mixer.Sound('sound/confirmar.mp3')

    comandos_rodando = True
    while comandos_rodando:

        janela.blit(escuro_comandos, (0, 0))
        janela.blit(comandos, (0, 0))

        if not controle_travado:
            janela.blit(ok, (335, 425))

        # Eventos
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RETURN and not controle_travado:

                    confirma_som.play()
                    fade_out = True
                    fade_transparencia = 255
                    controle_travado = True

        # Fade In
        if fade_in:

            if fade_transparencia < 255:
                fade_transparencia += 5
            else:
                fade_in = False
                controle_travado = False

            comandos.set_alpha(fade_transparencia)

        # Fade Out
        if fade_out:

            if fade_transparencia > 0:
                fade_transparencia -= 5
            else:
                menu()

            comandos.set_alpha(fade_transparencia)

        pygame.display.update()
        delta = ticks.tick(60)


def tela_creditos():

    # Globais
    global delta
    global ticks

    pygame.display.set_caption('IntroSouls - Créditos')

    # Escuro
    escuro_creditos = pygame.image.load('creditos/escuro_creditos.png').convert_alpha()

    # Creditos imagem
    creditos = pygame.image.load('creditos/credito.png').convert_alpha()
    creditos_posicoes_y = 0

    fade_transparencia = 0
    fade_in = True
    creditos.set_alpha(fade_transparencia)

    creditos_rodando = True
    while creditos_rodando:

        janela.blit(escuro_creditos, (0, 0))
        janela.blit(creditos, (0, creditos_posicoes_y))

        if not fade_in:
            creditos_posicoes_y -= 2

        if creditos_posicoes_y <= -2000:
            menu()

        # Eventos
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                exit()

        # Fade_in
        if fade_in:

            if fade_transparencia < 255:
                fade_transparencia += 2
            else:
                fade_in = False

            creditos.set_alpha(fade_transparencia)

        pygame.display.update()
        delta = ticks.tick(60)


def menu():
    """
    +Função+
    - Mostra um menu para que o jogador possa iniciar o jogo, junto, com um pequeno console para digitar comandos.
    """
    # Globais
    global rodando
    global ticks
    global delta

    # Fonte
    aviso_console_fonte = pygame.font.Font('alagard.ttf', 22)
    comando_fonte = pygame.font.Font('alagard.ttf', 55)

    pygame.display.set_caption("IntroSouls - Menu")

    # Carregar Sprites
    jogar = [pygame.transform.scale(pygame.image.load('selecao_menu/jogar_uns.png').convert_alpha(), (325, 325)),
             pygame.transform.scale(pygame.image.load('selecao_menu/jogar_s.png').convert_alpha(), (325, 325))]

    creditos = [pygame.transform.scale(pygame.image.load('selecao_menu/creditos_uns.png').convert_alpha(), (325, 325)),
                pygame.transform.scale(pygame.image.load('selecao_menu/creditos_s.png').convert_alpha(), (325, 325))]

    sair = [pygame.transform.scale(pygame.image.load('selecao_menu/sair_uns.png').convert_alpha(), (325, 325)),
            pygame.transform.scale(pygame.image.load('selecao_menu/sair_s.png').convert_alpha(), (325, 325))]

    logo = [pygame.transform.scale(pygame.image.load('logo/chave_esquerda.png').convert_alpha(), (400, 400)),
            pygame.transform.scale(pygame.image.load('logo/INTRO.png').convert_alpha(), (400, 400)),
            pygame.transform.scale(pygame.image.load('logo/SOULS.png').convert_alpha(), (400, 400)),
            pygame.transform.scale(pygame.image.load('logo/chave_direita.png').convert_alpha(), (400, 400))]

    for item in logo:
        item.set_alpha(0)

    fundo_menu = pygame.transform.scale(pygame.image.load('batalha/fundo_game.png'), (1324, 1068)).convert_alpha()

    fade_transparencia_menu = 0
    fade_in_menu = [False]

    selecionado = 'jogar'

    # Habilitar Comandos Teclado
    comando_hab = False
    console_hab = False

    # Posição das opções no menu
    y_opcoes = 225
    x_opcoes = 345
    distancia = 150

    # Preparar animação logo
    transparencia = 0
    anim_logo = True

    # Console
    console_base = pygame.transform.scale(pygame.image.load('teclas/console_base.png'), (1024, 200)).convert_alpha()

    # Aviso Console
    aviso_sair = pygame.transform.scale(pygame.image.load('teclas/aviso_3.png'), (300, 300)).convert_alpha()
    aviso_sair_texto = aviso_console_fonte.render("Sair do console", False, (0, 0, 0)).convert_alpha()
    aviso_sair_tecla = pygame.transform.scale(pygame.image.load('teclas/esc.png'), (130, 130)).convert_alpha()
    comando_digitado = ''

    # Musica
    pygame.mixer.music.load('sound/Menu.mp3')
    pygame.mixer.music.play()

    # Som
    confirma_som = pygame.mixer.Sound('sound/confirmar.mp3')
    navegar_menu_som = pygame.mixer.Sound('sound/navegar_menu.mp3')

    # Loop
    rodando = True
    while rodando:

        janela.blit(fundo_menu, (-149, -280))

        # Mostrar logo na tela
        janela.blit(logo[0], (-145, -100))
        janela.blit(logo[1], (100, -50))
        janela.blit(logo[2], (535, -53))
        janela.blit(logo[3], (780, -100))

        # Animação
        # Aumentar opacidade a cada tick
        if anim_logo:

            # Opacidade == 255 -> Não opaco
            if transparencia <= 255:

                # Aplicar transparência em cada parte da logo
                transparencia += 2
                for c in range(0, 4):
                    logo[c].set_alpha(transparencia)

            else:
                # Habilitar controle e terminar animação
                anim_logo = False
                comando_hab = True

        # Mostrar opções na tela
        if comando_hab and not console_hab:
            if selecionado == 'jogar':
                janela.blit(jogar[1], (x_opcoes, y_opcoes))
                janela.blit(creditos[0], (x_opcoes, y_opcoes + distancia))
                janela.blit(sair[0], (x_opcoes, y_opcoes + (distancia * 2)))

            elif selecionado == 'creditos':
                janela.blit(jogar[0], (x_opcoes, y_opcoes))
                janela.blit(creditos[1], (x_opcoes, y_opcoes + distancia))
                janela.blit(sair[0], (x_opcoes, y_opcoes + (distancia * 2)))

            elif selecionado == 'sair':
                janela.blit(jogar[0], (x_opcoes, y_opcoes))
                janela.blit(creditos[0], (x_opcoes, y_opcoes + distancia))
                janela.blit(sair[1], (x_opcoes, y_opcoes + (distancia * 2)))

        else:
            janela.blit(jogar[0], (x_opcoes, y_opcoes))
            janela.blit(creditos[0], (x_opcoes, y_opcoes + distancia))
            janela.blit(sair[0], (x_opcoes, y_opcoes + (distancia * 2)))

        # Caso o console esteja habilitado
        if console_hab:
            janela.blit(console_base, (0, 640))
            janela.blit(aviso_sair, (733, 608))
            janela.blit(aviso_sair_texto, (855, 713))
            janela.blit(aviso_sair_tecla, (742, 658))

            mostrar_comando = comando_fonte.render(f"{comando_digitado}_", False, (255, 255, 255)).convert_alpha()
            janela.blit(mostrar_comando, (10, 715))

        # Detectar Eventos
        for event in pygame.event.get():

            # Eventos de saída
            if event.type == pygame.QUIT:
                exit()

            # Detectar comando do teclado
            if event.type == pygame.KEYDOWN:

                if comando_hab and not console_hab:
                    # NAVEGAÇÃO
                    if event.key == pygame.K_UP:

                        if selecionado == 'sair':
                            navegar_menu_som.play()
                            selecionado = 'creditos'

                        elif selecionado == 'creditos':
                            navegar_menu_som.play()
                            selecionado = 'jogar'

                    if event.key == pygame.K_DOWN:

                        if selecionado == 'jogar':
                            navegar_menu_som.play()
                            selecionado = 'creditos'

                        elif selecionado == 'creditos':
                            navegar_menu_som.play()
                            selecionado = 'sair'

                    # Iniciar o console
                    if event.key == pygame.K_SLASH:
                        console_hab = True
                    if event.key == pygame.K_m:
                        console_hab = True

                # CONFIRMA / Opções do menu
                if event.key == (pygame.K_RETURN or pygame.K_z) and not console_hab:

                    if selecionado == 'jogar' and comando_hab:
                        confirma_som.play()
                        fade_transparencia_menu = 0
                        fade_in_menu = [True, 'jogar']
                        comando_hab = False
                    elif selecionado == 'creditos' and comando_hab:
                        confirma_som.play()
                        fade_transparencia_menu = 0
                        fade_in_menu = [True, 'creditos']
                        comando_hab = False

                    elif selecionado == 'sair' and comando_hab:
                        confirma_som.play()
                        confirma_sair()
                        pygame.display.set_caption("IntroSouls - Menu")

                if console_hab:

                    # Comandos Console
                    if event.key == pygame.K_ESCAPE:
                        comando_digitado = ''
                        console_hab = False

                    # Apagar caractere
                    if event.key == pygame.K_BACKSPACE:

                        if len(comando_digitado) > 0:
                            comando_digitado = comando_digitado[0:-1]

                    # Confirmar codigo
                    if event.key == pygame.K_RETURN:

                        if comando_digitado == 'introcomp':
                            fade_in_menu = [True, 'introcomp']

                        confirma_som.play()

                        comando_digitado = ''
                        console_hab = False

                    if len(comando_digitado) < 16:

                        # Mds o que é isso
                        if event.key == pygame.K_a:
                            comando_digitado += 'a'
                        if event.key == pygame.K_b:
                            comando_digitado += 'b'
                        if event.key == pygame.K_c:
                            comando_digitado += 'c'
                        if event.key == pygame.K_d:
                            comando_digitado += 'd'
                        if event.key == pygame.K_e:
                            comando_digitado += 'e'
                        if event.key == pygame.K_f:
                            comando_digitado += 'f'
                        if event.key == pygame.K_g:
                            comando_digitado += 'g'
                        if event.key == pygame.K_h:
                            comando_digitado += 'h'
                        if event.key == pygame.K_i:
                            comando_digitado += 'i'
                        if event.key == pygame.K_j:
                            comando_digitado += 'j'
                        if event.key == pygame.K_k:
                            comando_digitado += 'k'
                        if event.key == pygame.K_l:
                            comando_digitado += 'l'
                        if event.key == pygame.K_m:
                            comando_digitado += 'm'
                        if event.key == pygame.K_n:
                            comando_digitado += 'n'
                        if event.key == pygame.K_o:
                            comando_digitado += 'o'
                        if event.key == pygame.K_p:
                            comando_digitado += 'p'
                        if event.key == pygame.K_q:
                            comando_digitado += 'q'
                        if event.key == pygame.K_r:
                            comando_digitado += 'r'
                        if event.key == pygame.K_s:
                            comando_digitado += 's'
                        if event.key == pygame.K_t:
                            comando_digitado += 't'
                        if event.key == pygame.K_u:
                            comando_digitado += 'u'
                        if event.key == pygame.K_v:
                            comando_digitado += 'v'
                        if event.key == pygame.K_w:
                            comando_digitado += 'w'
                        if event.key == pygame.K_x:
                            comando_digitado += 'x'
                        if event.key == pygame.K_y:
                            comando_digitado += 'y'
                        if event.key == pygame.K_z:
                            comando_digitado += 'z'

        # Fade in
        if fade_in_menu[0]:

            if fade_transparencia_menu < 255:
                fade_transparencia_menu += 8
                escuro.set_alpha(fade_transparencia_menu)
            else:

                if fade_in_menu[1] == 'jogar':
                    selecao_personagens()
                    fade_in_menu = [False]
                    comando_hab = True

                # Batalha secreta
                elif fade_in_menu[1] == 'introcomp':
                    pygame.mixer.music.stop()
                    tela_carregar(['priest', 'paladin', 'rogue'], 'introcomp')

                if fade_in_menu[1] == 'creditos':
                    tela_creditos()

            janela.blit(escuro, (0, 0))

        # Atualização do display e ticks
        delta = ticks.tick(60)
        pygame.display.update()


# Iniciar Pygame
pygame.init()

# Grupo Player
grupo_player = []
dif_head = []

# Grupo Enemy
grupo_enemy = []

# Janelas
janela_dimensoes = Window(1024, 768)
janela = pygame.display.set_mode((janela_dimensoes.get_resolution()))
pygame.display.set_caption("IntroSouls - Menu")

# Grupo Personagens
grupo = []

# Transição
escuro = pygame.transform.scale(pygame.image.load('transicao/escuro.png'), (1024, 768)).convert_alpha()

# Clock
ticks = pygame.time.Clock()
delta = 0

# Rodando
rodando = True

# Musica e sons
pygame.mixer.init()

# Iniciar
iniciar_jogo()
