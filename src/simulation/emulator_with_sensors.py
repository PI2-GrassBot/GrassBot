import pygame
import random
import sys
import os

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
COR_OBSTACULO = (246, 120, 40)  # Preto
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

# Classe do Cortador de Grama
class Cortador:
    def __init__(self, estacao_carga):
        self.core = Core(random.randint(1, LARGURA // TAMANHO_CORTADOR - 2) * TAMANHO_CORTADOR,
                         random.randint(1, ALTURA // TAMANHO_CORTADOR - 2) * TAMANHO_CORTADOR,
                         1, True, 100)
        
        self.sensores = MockSensors(
            screen=tela,
            tile_size=TAMANHO_CORTADOR,
            obstacles=obstaculos,
            concrete_zones=[
                pygame.Rect(200, 100, 100, 300),  # Um bloco retangular de concreto
                pygame.Rect(400, 200, 200, 100),  # Outro bloco retangular
                pygame.Rect(600, 400, 150, 150),  # Um bloco quadrado
            ]
        )
        self.direcao = "RIGHT"
        self.visitados = set()
  

    def mover(self):
        self.visitados.add((self.core.x, self.core.y))

        
        # Detectar obstáculo com o sensor ultrassônico
        if self.sensores.sensor_ultrassonico(self.core.x, self.core.y, self.direcao) or self.sensores.sensor_cor(self.core.x, self.core.y, self.direcao) == "Concreto":
            # para o cortador e recaucula a rota
            self.core.velocidade = 0
            self.direcao = self.recaucular_rota()



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

    def recaucular_rota(self):
        direcao_atual = self.direcao
        if direcao_atual == "UP":
            direcoes = ["LEFT", "RIGHT", "DOWN"]
        elif direcao_atual == "DOWN":
            direcoes = ["LEFT", "RIGHT", "UP"]
        elif direcao_atual == "LEFT":
            direcoes = ["UP", "DOWN", "RIGHT"]
        elif direcao_atual == "RIGHT":
            direcoes = ["UP", "DOWN", "LEFT"]
        
        for direcao in direcoes:
            if direcao == "UP":
                x, y = self.core.x, self.core.y - TAMANHO_CORTADOR
            elif direcao == "DOWN":
                x, y = self.core.x, self.core.y + TAMANHO_CORTADOR
            elif direcao == "LEFT":
                x, y = self.core.x - TAMANHO_CORTADOR, self.core.y
            elif direcao == "RIGHT":
                x, y = self.core.x + TAMANHO_CORTADOR, self.core.y
            
            # verfificar se x,y esta em self.visitados ou obstaculos
            if (x, y) not in obstaculos:
                return direcao
            



# Classe do Painel
class Painel:
    def __init__(self, cortador, largura=PANEL_WIDTH, altura=ALTURA):
        self.largura = largura
        self.altura = altura
        self.cortador = cortador
        self.velocidade = cortador.core.velocidade
        self.altura = cortador.core.altura
        self.power = cortador.core.power

        self.sensor_ultrassonico = cortador.sensores.sensor_ultrassonico(cortador.core.x, cortador.core.y, cortador.direcao)

        self.sensor_cor = cortador.sensores.sensor_cor(cortador.core.x, cortador.core.y, cortador.direcao)
 

    def desenhar(self):
        # Desenhar o painel a esquerda da tela
        pygame.draw.rect(tela, (0,0,0), (LARGURA, 0, self.largura, self.altura))

        # Exibir informações do cortador

        texto_posicao = fonte.render(f"Posição: ({self.cortador.core.x // TAMANHO_CORTADOR}, {self.cortador.core.y // TAMANHO_CORTADOR})", True, COR_TEXTO)
        tela.blit(texto_posicao, (LARGURA + 10, 10))

        texto_velocidade = fonte.render(f"Velocidade: {self.velocidade}", True, COR_TEXTO)
        tela.blit(texto_velocidade, (LARGURA + 10, 40))

        texto_altura = fonte.render(f"Altura: {self.altura}", True, COR_TEXTO)
        tela.blit(texto_altura, (LARGURA + 10, 70))

        texto_power = fonte.render(f"Power: {self.power}", True, COR_TEXTO)
        tela.blit(texto_power, (LARGURA + 10, 100))

        # Exibir informações dos sensores
        texto_sensor_ultrassonico = fonte.render(f"Sensor Ultrassônico: {self.sensor_ultrassonico}", True, COR_TEXTO)
        tela.blit(texto_sensor_ultrassonico, (LARGURA + 10, 130))

        texto_sensor_cor = fonte.render(f"Sensor de Cor: {self.sensor_cor}", True, COR_TEXTO)
        tela.blit(texto_sensor_cor, (LARGURA + 10, 160))



    
    def atualizar(self):
        # Atualizar informações do cortador
        self.velocidade = self.cortador.core.velocidade
        self.altura = self.cortador.core.altura
        self.power = self.cortador.core.power

        # Atualizar informações dos sensores
        self.sensor_ultrassonico = self.cortador.sensores.sensor_ultrassonico (self.cortador.core.x, self.cortador.core.y, self.cortador.direcao)
        self.sensor_cor = self.cortador.sensores.sensor_cor(self.cortador.core.x, self.cortador.core.y, self.cortador.direcao)




# Lista de obstáculos
obstaculos = []

# Estação de carga
estacao_carga = (0, 0)

# Inicializar o cortador
cortador = Cortador(estacao_carga)
painel = Painel(cortador)

# Loop principal
rodando = True
clock = pygame.time.Clock()

while rodando:
    
    # Desenhar o mapa ao lado direito do painel
    tela.fill(COR_GRAMA)

    # Desenhar o painel
    painel.desenhar()
    painel.atualizar()

    
    
    # Áreas de pisos de concreto no mapa
    pisos_concreto = [
        # Define aqui as coordenadas e dimensões dos blocos de concreto
        (200, 100, 100, 300),  # Um bloco retangular de concreto
        (400, 200, 200, 100),  # Outro bloco retangular
        (600, 400, 150, 150),  # Um bloco quadrado
    ]
    
    # Desenhar os blocos de concreto
    for piso in pisos_concreto:
        x, y, largura, altura = piso
        pygame.draw.rect(tela, COR_CONCRETO, (x, y, largura, altura))
    
    
    # Cria obstcaulos ao redor do mapa
    for i in range(0, LARGURA, TAMANHO_CORTADOR):
        obstaculos.append((i, 0))
        obstaculos.append((i, ALTURA - TAMANHO_CORTADOR))
    for i in range(0, ALTURA, TAMANHO_CORTADOR):
        obstaculos.append((0, i))
        obstaculos.append((LARGURA - TAMANHO_CORTADOR, i))
    
    


    for i in range(len(grama_cortada)):
        for j in range(len(grama_cortada[i])):
            if grama_cortada[i][j]:
                pygame.draw.rect(tela, (144, 238, 144), (j * TAMANHO_CORTADOR, i * TAMANHO_CORTADOR, TAMANHO_CORTADOR, TAMANHO_CORTADOR))

    for obstaculo in obstaculos:
        pygame.draw.rect(tela, COR_OBSTACULO, (obstaculo[0], obstaculo[1], TAMANHO_CORTADOR, TAMANHO_CORTADOR))

    # pygame.draw.rect(tela, COR_ESTACAO, (estacao_carga[0], estacao_carga[1], TAMANHO_CORTADOR, TAMANHO_CORTADOR))

    cortador.mover()

    pygame.draw.rect(tela, COR_CORTADOR, (cortador.core.x, cortador.core.y, TAMANHO_CORTADOR, TAMANHO_CORTADOR))

    # Exibir informações da bateria
    # texto_bateria = fonte.render(f"Bateria: {cortador.core.bateria}%", True, COR_TEXTO)
    # tela.blit(texto_bateria, (10, 10))

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
