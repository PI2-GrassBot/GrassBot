import pygame
import random
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from core.core import Core
from mock_sensors import MockSensors

# Configurações iniciais
LARGURA, ALTURA = 600, 600
TAMANHO_CORTADOR = 30
COR_GRAMA = (34, 139, 34)  # Verde
COR_CORTADOR = (255, 0, 0)  # Vermelho
COR_OBSTACULO = (0, 0, 0)  # Preto
COR_ESTACAO = (0, 0, 255)  # Azul
COR_TEXTO = (255, 255, 255)  # Branco

# Inicialização do pygame
pygame.init()
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Emulador - Cortador de Grama Automatizado")

# Fonte para exibir informações
tamanho_fonte = 20
fonte = pygame.font.Font(None, tamanho_fonte)

grama_cortada = [[False for _ in range(LARGURA // TAMANHO_CORTADOR)] for _ in range(ALTURA // TAMANHO_CORTADOR)]

# Classe do Cortador de Grama
class Cortador:
    def __init__(self, estacao_carga):
        self.core = Core(random.randint(0, LARGURA // TAMANHO_CORTADOR - 1) * TAMANHO_CORTADOR,
                         random.randint(0, ALTURA // TAMANHO_CORTADOR - 1) * TAMANHO_CORTADOR,
                         2, True, 100)
        self.sensores = MockSensors()
        self.direcao = "RIGHT"
        self.visitados = set()
        self.estacao_carga = estacao_carga

    def mover(self):
        if self.core.bateria <= 10:
            self.ir_para_estacao()
            return

        self.visitados.add((self.core.x, self.core.y))

        if self.detectar_obstaculo():
            self.direcao = self.recaucular_rota()
            self.sensores.set_all_sensors(False)

        if self.direcao == "UP":
            self.core.y -= TAMANHO_CORTADOR
        elif self.direcao == "DOWN":
            self.core.y += TAMANHO_CORTADOR
        elif self.direcao == "LEFT":
            self.core.x -= TAMANHO_CORTADOR
        elif self.direcao == "RIGHT":
            self.core.x += TAMANHO_CORTADOR

        self.core.x = max(0, min(self.core.x, LARGURA - TAMANHO_CORTADOR))
        self.core.y = max(0, min(self.core.y, ALTURA - TAMANHO_CORTADOR))

        grama_cortada[self.core.y // TAMANHO_CORTADOR][self.core.x // TAMANHO_CORTADOR] = True
        self.core.consumir_bateria()

    def ir_para_estacao(self):
        if (self.core.x, self.core.y) == self.estacao_carga:
            self.core.recarregar_bateria()
        else:
            if self.core.x < self.estacao_carga[0]:
                self.core.x += TAMANHO_CORTADOR
            elif self.core.x > self.estacao_carga[0]:
                self.core.x -= TAMANHO_CORTADOR

            if self.core.y < self.estacao_carga[1]:
                self.core.y += TAMANHO_CORTADOR
            elif self.core.y > self.estacao_carga[1]:
                self.core.y -= TAMANHO_CORTADOR

    def detectar_obstaculo(self):
        arestas = {
            "UP": (self.core.x, self.core.y - TAMANHO_CORTADOR),
            "DOWN": (self.core.x, self.core.y + TAMANHO_CORTADOR),
            "LEFT": (self.core.x - TAMANHO_CORTADOR, self.core.y),
            "RIGHT": (self.core.x + TAMANHO_CORTADOR, self.core.y)
        }

        obstaculo_detectado = False

        for direcao, aresta in arestas.items():
            x, y = aresta

            if (x, y) in obstaculos:
                self.sensores.set_sensor(direcao, True)
                obstaculo_detectado = True

            if x < 0 or x >= LARGURA or y < 0 or y >= ALTURA:
                self.sensores.set_sensor(direcao, True)
                obstaculo_detectado = True

        return obstaculo_detectado

    def recaucular_rota(self):
        direcoes_possiveis = []
        mapa_direcoes = {
            "UP": (self.core.x, self.core.y - TAMANHO_CORTADOR),
            "DOWN": (self.core.x, self.core.y + TAMANHO_CORTADOR),
            "LEFT": (self.core.x - TAMANHO_CORTADOR, self.core.y),
            "RIGHT": (self.core.x + TAMANHO_CORTADOR, self.core.y)
        }

        for direcao, posicao in mapa_direcoes.items():
            x, y = posicao
            if not self.sensores.get_sensor_status(direcao) and (x, y) not in self.visitados:
                direcoes_possiveis.append((direcao, posicao))

        if not direcoes_possiveis:
            for direcao, posicao in mapa_direcoes.items():
                if not self.sensores.get_sensor_status(direcao):
                    direcoes_possiveis.append((direcao, posicao))

        if direcoes_possiveis:
            return direcoes_possiveis[0][0]

        return "UP"

# Lista de obstáculos
obstaculos = []

# Estação de carga
estacao_carga = (0, 0)

# Inicializar o cortador
cortador = Cortador(estacao_carga)

# Loop principal
rodando = True
clock = pygame.time.Clock()

while rodando:
    tela.fill(COR_GRAMA)

    for i in range(len(grama_cortada)):
        for j in range(len(grama_cortada[i])):
            if grama_cortada[i][j]:
                pygame.draw.rect(tela, (144, 238, 144), (j * TAMANHO_CORTADOR, i * TAMANHO_CORTADOR, TAMANHO_CORTADOR, TAMANHO_CORTADOR))

    for obstaculo in obstaculos:
        pygame.draw.rect(tela, COR_OBSTACULO, (obstaculo[0], obstaculo[1], TAMANHO_CORTADOR, TAMANHO_CORTADOR))

    pygame.draw.rect(tela, COR_ESTACAO, (estacao_carga[0], estacao_carga[1], TAMANHO_CORTADOR, TAMANHO_CORTADOR))

    cortador.mover()

    pygame.draw.rect(tela, COR_CORTADOR, (cortador.core.x, cortador.core.y, TAMANHO_CORTADOR, TAMANHO_CORTADOR))

    # Exibir informações da bateria
    texto_bateria = fonte.render(f"Bateria: {cortador.core.bateria}%", True, COR_TEXTO)
    tela.blit(texto_bateria, (10, 10))

    pygame.display.flip()
    clock.tick(10)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = evento.pos
            obstaculo_x = (mouse_x // TAMANHO_CORTADOR) * TAMANHO_CORTADOR
            obstaculo_y = (mouse_y // TAMANHO_CORTADOR) * TAMANHO_CORTADOR
            if (obstaculo_x, obstaculo_y) not in obstaculos:
                obstaculos.append((obstaculo_x, obstaculo_y))

pygame.quit()
