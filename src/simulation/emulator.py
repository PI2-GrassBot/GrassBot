import pygame
import random

import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from core.core import Core
from mock_sensors import MockSensors

# Configurações iniciais
LARGURA, ALTURA = 500, 500
TAMANHO_CORTADOR = 30
COR_GRAMA = (34, 139, 34)  # Verde
COR_CORTADOR = (255, 0, 0)  # Vermelho
COR_OBSTACULO = (0, 0, 0)  # Preto

# Inicialização do pygame
pygame.init()
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Emulador - Cortador de Grama Automatizado")

# Criar um grid para visualizar a grama cortada
grama_cortada = [[False for _ in range(LARGURA // TAMANHO_CORTADOR)] for _ in range(ALTURA // TAMANHO_CORTADOR)]

# Classe do Cortador de Grama
class Cortador:
    def __init__(self):
        self.core = Core(random.randint(0, LARGURA // TAMANHO_CORTADOR - 1) * TAMANHO_CORTADOR,
                         random.randint(0, ALTURA // TAMANHO_CORTADOR - 1) * TAMANHO_CORTADOR,
                         2, True)
        self.sensores = MockSensors()
        self.direcao = "RIGHT"

    def mover(self):
        self.core.mover(self.direcao)
        if self.detectar_obstaculo():
            self.direcao = self.core.recaucular_rota(self.sensores.avalia_ambiente())
            self.sensores.set_all_sensors(False)
        

        # Mantém dentro dos limites da tela
        self.core.x = max(0, min(self.core.x, LARGURA - TAMANHO_CORTADOR))
        self.core.y = max(0, min(self.core.y, ALTURA - TAMANHO_CORTADOR))

        # Marca a grama como cortada
        grama_cortada[self.core.y // TAMANHO_CORTADOR][self.core.x // TAMANHO_CORTADOR] = True

    def detectar_obstaculo(self):
        """"
        Veriica se alguma das arestas do cortador esta em contato com um obstaculo ou limite da tela e atualiza os sensores.
        """
        arestas = {
            "UP": (self.core.x, self.core.y),
            "DOWN": (self.core.x, self.core.y + TAMANHO_CORTADOR),
            "LEFT": (self.core.x, self.core.y),
            "RIGHT": (self.core.x + TAMANHO_CORTADOR, self.core.y)
        }


         # Verifica se a aresta do cortador está em contato com algum limite
        for direcao, aresta in arestas.items():
           
            if (aresta[1] == 0 and direcao == "UP"):
                self.sensores.set_sensor(direcao, True)
                print("Limite da tela detectado na direcao: ", direcao)
            elif (aresta[1] == ALTURA - (TAMANHO_CORTADOR-TAMANHO_CORTADOR) and direcao == "DOWN"):
                self.sensores.set_sensor(direcao, True)
                print("Limite da tela detectado na direcao: ", direcao)

            if (aresta[0] == 0 and direcao == "LEFT"):
                self.sensores.set_sensor(direcao, True)
                print("Limite da tela detectado na direcao: ", direcao)
            elif (aresta[0] == LARGURA and direcao == "RIGHT"):
                self.sensores.set_sensor(direcao, True)
                print("Limite da tela detectado na direcao: ", direcao)


        if any(self.sensores.avalia_ambiente()):
            return True
        return False
    


# Lista de obstáculos
obstaculos = []

# Inicializar o cortador
cortador = Cortador()

# Loop principal
rodando = True
clock = pygame.time.Clock()

while rodando:
    tela.fill(COR_GRAMA)

    # Desenhar a grama cortada
    for i in range(len(grama_cortada)):
        for j in range(len(grama_cortada[i])):
            if grama_cortada[i][j]:
                pygame.draw.rect(tela, (144, 238, 144), (j * TAMANHO_CORTADOR, i * TAMANHO_CORTADOR, TAMANHO_CORTADOR, TAMANHO_CORTADOR))

    # Desenhar obstáculos
    for obstaculo in obstaculos:
        pygame.draw.rect(tela, COR_OBSTACULO, (obstaculo[0], obstaculo[1], TAMANHO_CORTADOR, TAMANHO_CORTADOR))

    # Mover o cortador
    cortador.mover()

    # Desenhar o cortador
    pygame.draw.rect(tela, COR_CORTADOR, (cortador.core.x, cortador.core.y, TAMANHO_CORTADOR, TAMANHO_CORTADOR))

    # Atualizar tela
    pygame.display.flip()
    clock.tick(10)  # Controla a velocidade da simulação

    # Eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            # Adiciona um obstáculo na posição clicada pelo usuário
            mouse_x, mouse_y = evento.pos
            obstaculo_x = (mouse_x // TAMANHO_CORTADOR) * TAMANHO_CORTADOR
            obstaculo_y = (mouse_y // TAMANHO_CORTADOR) * TAMANHO_CORTADOR
            if (obstaculo_x, obstaculo_y) not in obstaculos:
                obstaculos.append((obstaculo_x, obstaculo_y))

pygame.quit()
