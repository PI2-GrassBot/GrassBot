import json
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

class Core:
    def __init__(self, x: int, y: int):
        """
        Classe responsável pelo controle principal do cortador de grama.
        :param x: Posição X inicial do cortador.
        :param y: Posição Y inicial do cortador.
        :param velocidade: Velocidade de movimento do cortador.
        :param power: Estado ligado/desligado do cortador.
        :param bateria: Nível inicial da bateria do cortador.
        """
        self.x = x
        self.y = y
        self.atualiza_comando()


    def ligar(self):
        """Liga o cortador."""
        self.power = True

    def desligar(self):
        """Desliga o cortador."""
        self.power = False

    def mover(self, direcao: str):
        """
        Move o cortador na direção especificada.
        :param direcao: Direção do movimento ("UP", "DOWN", "LEFT", "RIGHT").
        """
        if not self.power or self.bateria <= 0:
            print("Cortador desligado ou sem bateria.")
            return

        if direcao == "UP":
            self.y -= self.velocidade
        elif direcao == "DOWN":
            self.y += self.velocidade
        elif direcao == "LEFT":
            self.x -= self.velocidade
        elif direcao == "RIGHT":
            self.x += self.velocidade

        # self.consumir_bateria()

    def atualiza_comando(self):

        with open('src/api/data/data.json') as f:
            data = json.load(f)

        self.power = data['ligado']            
        self.velocidade = data['velocidade']
        self.altura = data['altura_corte']

        return self.power, self.velocidade, self.altura

    def get_posicao(self):
        """Retorna a posição atual do cortador."""
        return self.x, self.y

    # def consumir_bateria(self):
    #     """Reduz a bateria a cada movimento."""
    #     if self.bateria > 0:
    #         self.bateria -= 1

    def recarregar_bateria(self):
        """Recarrega a bateria do cortador."""
        self.bateria = 100

    # def recaucular_rota(self, sensores, direcao_atual=None):
    #     """
    #     Recalcula a rota do cortador baseado nos sensores.
    #     :param sensores: Lista de sensores ativados.
    #     :param direcao_atual: Direção atual do movimento (opcional).
    #     """
    #     direcoes_possiveis = []

    #     # Mapeia sensores às direções
    #     mapa_direcoes = {
    #         0: "UP",
    #         1: "DOWN",
    #         2: "LEFT",
    #         3: "RIGHT"
    #     }

        # # Adiciona direções livres
        # for i, sensor in enumerate(sensores):
        #     if not sensor:  # Direção está livre
        #         direcoes_possiveis.append(mapa_direcoes[i])

        # # Prioriza manter a direção atual
        # if direcao_atual in direcoes_possiveis:
        #     return direcao_atual

        # # Escolhe aleatoriamente entre as direções disponíveis
        # if direcoes_possiveis:
        #     return random.choice(direcoes_possiveis)

        # # Caso nenhuma direção esteja disponível, retornar "UP" como padrão
        # return "UP"
