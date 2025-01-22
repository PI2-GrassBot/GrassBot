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
        self.posicao_atual = (self.x, self.y)


    def ligar(self):
        """Liga o cortador."""
        self.power = True

    def desligar(self):
        """Desliga o cortador."""
        self.power = False

    

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
