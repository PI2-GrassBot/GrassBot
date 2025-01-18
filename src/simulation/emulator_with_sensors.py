import pygame
import random
import sys
import os
from collections import deque

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from core.core import Core
from mock_sensors import MockSensors

# Configurações iniciais
PANEL_WIDTH = 300
PANEL_COLOR = (0, 0, 0)
LARGURA, ALTURA = 900, 600
TAMANHO_CORTADOR = 30
COR_GRAMA = (34, 139, 34)  # Verde
COR_CONCRETO = (169, 169, 169)  # Cinza
COR_CORTADOR = (255, 0, 0)  # Vermelho
COR_OBSTACULO = (246, 120, 40)  # Laranja
COR_ESTACAO = (0, 0, 255)  # Azul
COR_TEXTO = (255, 255, 255)  # Branco

# Inicialização do pygame
pygame.init()
tela = pygame.display.set_mode((LARGURA + PANEL_WIDTH, ALTURA))
pygame.display.set_caption("Emulador - Cortador de Grama Automatizado")

# Fonte para exibir informações
tamanho_fonte = 20
fonte = pygame.font.Font(None, tamanho_fonte)

grama_cortada = [[False for _ in range(LARGURA // TAMANHO_CORTADOR)] for _ in range(ALTURA // TAMANHO_CORTADOR)]

# Lista de obstáculos
obstaculos = [(x, 0) for x in range(0, LARGURA, TAMANHO_CORTADOR)] + \
             [(x, ALTURA - TAMANHO_CORTADOR) for x in range(0, LARGURA, TAMANHO_CORTADOR)] + \
             [(0, y) for y in range(0, ALTURA, TAMANHO_CORTADOR)] + \
             [(LARGURA - TAMANHO_CORTADOR, y) for y in range(0, ALTURA, TAMANHO_CORTADOR)]

# Classe do Cortador de Grama
class Cortador:
    def __init__(self):
        self.core = Core(
            random.randint(1, LARGURA // TAMANHO_CORTADOR - 2) * TAMANHO_CORTADOR,
            random.randint(1, ALTURA // TAMANHO_CORTADOR - 2) * TAMANHO_CORTADOR
        )
        self.sensores = MockSensors(
            screen=tela,
            tile_size=TAMANHO_CORTADOR,
            obstacles=obstaculos,
            concrete_zones=[
                pygame.Rect(200, 100, 100, 300),
                pygame.Rect(400, 200, 200, 100),
                pygame.Rect(600, 400, 150, 150),
            ]
        )
        self.direcao = "RIGHT"

    def obter_cor_bloco(self, x, y):
        """Obtém a cor do bloco no mapa."""
        return tela.get_at((x + TAMANHO_CORTADOR // 2, y + TAMANHO_CORTADOR // 2))[:3]

    def cortar_bloco(self, x, y):
        """Marca o bloco como cortado."""
        posicao_x = x // TAMANHO_CORTADOR
        posicao_y = y // TAMANHO_CORTADOR
        grama_cortada[posicao_y][posicao_x] = True

    def mover(self):
        # Verifica blocos adjacentes
        for dx, dy in [(-TAMANHO_CORTADOR, 0), (TAMANHO_CORTADOR, 0), (0, -TAMANHO_CORTADOR), (0, TAMANHO_CORTADOR)]:
            vizinho_x, vizinho_y = self.core.x + dx, self.core.y + dy
            if 0 <= vizinho_x < LARGURA and 0 <= vizinho_y < ALTURA:
                posicao_x = vizinho_x // TAMANHO_CORTADOR
                posicao_y = vizinho_y // TAMANHO_CORTADOR
                if not grama_cortada[posicao_y][posicao_x] and self.obter_cor_bloco(vizinho_x, vizinho_y) == COR_GRAMA:
                    self.core.x, self.core.y = vizinho_x, vizinho_y
                    self.cortar_bloco(vizinho_x, vizinho_y)
                    return  # Move-se para o bloco adjacente e para a execução

        # Se nenhum bloco adjacente está disponível, busca o próximo bloco mais próximo
        destino = self.encontrar_grama_mais_proxima()
        if destino:
            destino_x, destino_y = destino
            self.direcao = self.calcular_direcao(destino_x, destino_y)

            # Calcula nova posição com base na direção
            nova_x, nova_y = self.core.x, self.core.y
            if self.direcao == "UP":
                nova_y -= TAMANHO_CORTADOR
            elif self.direcao == "DOWN":
                nova_y += TAMANHO_CORTADOR
            elif self.direcao == "LEFT":
                nova_x -= TAMANHO_CORTADOR
            elif self.direcao == "RIGHT":
                nova_x += TAMANHO_CORTADOR

            if 0 <= nova_x < LARGURA and 0 <= nova_y < ALTURA:
                self.core.x, self.core.y = nova_x, nova_y
                self.cortar_bloco(nova_x, nova_y)

    def encontrar_grama_mais_proxima(self):
        """Usa BFS para encontrar a posição mais próxima de grama não cortada."""
        fila = deque([(self.core.x, self.core.y)])  # Começa na posição atual
        visitados = set()
        visitados.add((self.core.x, self.core.y))

        while fila:
            x, y = fila.popleft()

            # Verifica se é grama não cortada
            pos_x, pos_y = x // TAMANHO_CORTADOR, y // TAMANHO_CORTADOR
            if not grama_cortada[pos_y][pos_x] and self.obter_cor_bloco(x, y) == COR_GRAMA:
                return x, y

            # Adiciona os vizinhos à fila
            for dx, dy in [(-TAMANHO_CORTADOR, 0), (TAMANHO_CORTADOR, 0), (0, -TAMANHO_CORTADOR), (0, TAMANHO_CORTADOR)]:
                novo_x, novo_y = x + dx, y + dy
                if (0 <= novo_x < LARGURA and 0 <= novo_y < ALTURA and
                        (novo_x, novo_y) not in visitados and self.obter_cor_bloco(novo_x, novo_y) != COR_CONCRETO):
                    fila.append((novo_x, novo_y))
                    visitados.add((novo_x, novo_y))

        return None

    def calcular_direcao(self, destino_x, destino_y):
        """Calcula a direção para o destino."""
        if self.core.x < destino_x:
            return "RIGHT"
        elif self.core.x > destino_x:
            return "LEFT"
        elif self.core.y < destino_y:
            return "DOWN"
        elif self.core.y > destino_y:
            return "UP"
        return self.direcao

# Classe do Painel
class Painel:
    def __init__(self, cortador):
        self.cortador = cortador

    def desenhar(self):
        pygame.draw.rect(tela, PANEL_COLOR, (LARGURA, 0, PANEL_WIDTH, ALTURA))
        info = [
            f"Posição: ({self.cortador.core.x // TAMANHO_CORTADOR}, {self.cortador.core.y // TAMANHO_CORTADOR})",
        ]
        for i, texto in enumerate(info):
            tela.blit(fonte.render(texto, True, COR_TEXTO), (LARGURA + 10, 10 + i * 30))

# Loop principal
cortador = Cortador()
painel = Painel(cortador)
clock = pygame.time.Clock()
rodando = True

while rodando:
    tela.fill(COR_GRAMA)

    # Desenhar concreto
    pisos_concreto = [
        (200, 100, 100, 300),
        (400, 200, 200, 100),
        (600, 400, 150, 150),
    ]
    for x, y, w, h in pisos_concreto:
        pygame.draw.rect(tela, COR_CONCRETO, (x, y, w, h))

    # Desenhar grama cortada
    for i, linha in enumerate(grama_cortada):
        for j, cortada in enumerate(linha):
            if cortada:
                pygame.draw.rect(tela, (144, 238, 144), (j * TAMANHO_CORTADOR, i * TAMANHO_CORTADOR, TAMANHO_CORTADOR, TAMANHO_CORTADOR))

    cortador.mover()
    pygame.draw.rect(tela, COR_CORTADOR, (cortador.core.x, cortador.core.y, TAMANHO_CORTADOR, TAMANHO_CORTADOR))
    pygame.display.flip()
    clock.tick(10)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

pygame.quit()
