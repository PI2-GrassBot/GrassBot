import random

class Core:
    def __init__(self, x: int, y: int, velocidade: int, power: bool):
        """
        Classe responsável pelo controle principal do cortador de grama.
        :param x: Posição X inicial do cortador.
        :param y: Posição Y inicial do cortador.
        :param velocidade: Velocidade de movimento do cortador.
        :param power: Estado ligado/desligado do cortador.
        """
        self.x = x
        self.y = y
        self.velocidade = velocidade
        self.power = power

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
        if not self.power:
            return

        if direcao == "UP":
            self.y -= self.velocidade
        elif direcao == "DOWN":
            self.y += self.velocidade
        elif direcao == "LEFT":
            self.x -= self.velocidade
        elif direcao == "RIGHT":
            self.x += self.velocidade

    def get_posicao(self):
        """Retorna a posição atual do cortador."""
        return self.x, self.y
    
    def recaucular_rota(self, sensores):
        """
        Recalcula a rota do cortador baseado nos sensores.
        :param sensores: Lista de sensores ativados.
        """
        direcoes_possiveis = []
        if not sensores[0]:  # Sensor A (cima livre)
            direcoes_possiveis.append("UP")
        if not sensores[1]:  # Sensor B (baixo livre)
            direcoes_possiveis.append("DOWN")
        if not sensores[2]:  # Sensor C (esquerda livre)
            direcoes_possiveis.append("LEFT")
        if not sensores[3]:  # Sensor D (direita livre)
            direcoes_possiveis.append("RIGHT")
        
        if direcoes_possiveis:
            return random.choice(direcoes_possiveis)
        return "UP"  # Direção padrão caso nenhuma outra seja fornecida
