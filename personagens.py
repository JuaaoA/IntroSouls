
class Character:
    def __init__(self, nome, vida_max, ataque, defesa, mana_max, iniciativa):
        self.nome = nome
        self.derrotado = False
        self.vida_max = vida_max
        self.vida_atual = vida_max
        self.ataque = ataque
        self.defesa = defesa
        self.mana_max = mana_max
        self.mana_atual = mana_max
        self.iniciativa = iniciativa
        self.defesa_paladino = [False]
        self.image_ingame = 0
        self.image_face = 0
        self.revelado = [False]
        self.queimando = [False]
        self.envenenado = [False]
        self.defesa_extra = [False]
        self.atordoado = [False]
        self.ataques = ['Basico', 'Flecha Dupla', 'Fogareu', 'Mordida', 'Adaga', 'teste6']
        self.defesas = ['Basico', 'Curar-se', 'Arco vida', 'Paladino']


class Hunter(Character):

    def __str__(self):
        print('')


class Priest(Character):

    def __str__(self):
        print('')


class Paladin(Character):

    def __str__(self):
        print('')


class Wizard(Character):

    def __str__(self):
        print('')


class Rogue(Character):

    def __str__(self):
        print('')


class Jorge(Character):

    def __str__(self):
        print('')


class Thiago(Character):

    def __str__(self):
        print('')


class Skeleton(Character):

    def __str__(self):
        print('')


class DarkWizard(Character):

    def __str__(self):
        print('')


# Reiniciar Todos os stats dos personagens
def reiniciar_classes():

    global hunter_stat
    global priest_stat
    global paladin_stat
    global wizard_stat
    global rogue_stat
    global skeleton_stat
    global darkwizard_stat

    # STATS
    hunter_stat = Hunter('Hunter', 100, 14, 10, 20, 17)
    priest_stat = Priest('Priest', 75, 13, 5, 25, 16)
    paladin_stat = Paladin('Paladin', 150, 30, 25, 5, 8)
    wizard_stat = Wizard('Wizard', 75, 20, 7, 30, 12)
    rogue_stat = Rogue('Rogue', 100, 16, 12, 13, 18)

    # STATS ENEMIES
    skeleton_stat = Skeleton('Skeleton', 60, 12, 9, 0, 15)
    darkwizard_stat = DarkWizard('Dark Wizard', 80, 15, 9, 60, 13)


# CASO QUEIRA ADICIONAR MAIS UM PERSONAGEM / ADICIONE A CLASSE E NA FUNÇÃO BATALHA() E COLOQUE A IMAGEM CARREGADA

# STATS
hunter_stat = Hunter('Hunter', 100, 14, 10, 20, 17)

priest_stat = Priest('Priest', 75, 13, 5, 25, 16)

paladin_stat = Paladin('Paladin', 150, 30, 25, 5, 8)

wizard_stat = Wizard('Wizard', 75, 20, 7, 30, 12)

rogue_stat = Rogue('Rogue', 100, 16, 12, 13, 18)

jorge_stat = Jorge('Jorge', 130, 32, 15, 19, 64)

thiago_stat = Thiago('Thiago', 125, 28, 13, 99, 12)

# STATS ENEMIES
skeleton_stat = Skeleton('Skeleton', 60, 17, 9, 0, 15)

darkwizard_stat = DarkWizard('Dark Wizard', 80, 19, 9, 60, 13)
