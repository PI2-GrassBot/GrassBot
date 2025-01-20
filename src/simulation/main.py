import pygame
import random
import sys
import os
import json

from time import sleep

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))


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
                pygame.Rect(200, 100, 100, 300),  # Um bloco retangular de concreto
                pygame.Rect(400, 200, 200, 100),  # Outro bloco retangular
            ]
        )
        self.direcao = "RIGHT"
        self.mapa = {}
        self.visitados = set()

    
    def velocidade(self):
        sleep(1 - self.core.velocidade / 100)
        return self.core.velocidade
    
    
    def mover(self):
        """
        Controla o movimento do cortador e garante que ele explore todas as áreas,
        evitando obstáculos e concreto sempre que possível.
        """
        # Verifica se toda a grama foi cortada
        if all(all(cortada for cortada in linha) for linha in grama_cortada):
            print("Toda a grama foi cortada! Parando o cortador...")
            self.core.velocidade = 0
            return

        # Ajusta a velocidade do cortador
        self.velocidade()
        self.core.atualiza_comando()

        # Aguarda até que o cortador esteja ligado e com velocidade
        while self.core.velocidade == 0 or not self.core.power:
            self.core.atualiza_comando()
            sleep(0.5)

        # Detecta obstáculos ou áreas de concreto usando os sensores
        dados_sensores = self.sensores.get_data(self.core.x, self.core.y)

        for dado in dados_sensores:
            pos = dado["posicao"]
            if dado["direcao"] == self.direcao and \
            (dado["tipo"] == "Obstáculo" or 
                not (0 <= pos[1] // TAMANHO_CORTADOR < len(grama_cortada) and \
                    0 <= pos[0] // TAMANHO_CORTADOR < len(grama_cortada[0])) or
                grama_cortada[pos[1] // TAMANHO_CORTADOR][pos[0] // TAMANHO_CORTADOR]):
                self.direcao = self.recaucular_rota()
                break

        # Movimenta o cortador na direção atual
        if self.direcao == "UP":
            self.core.y -= TAMANHO_CORTADOR
        elif self.direcao == "DOWN":
            self.core.y += TAMANHO_CORTADOR
        elif self.direcao == "LEFT":
            self.core.x -= TAMANHO_CORTADOR
        elif self.direcao == "RIGHT":
            self.core.x += TAMANHO_CORTADOR

        # Garante que o cortador não ultrapasse os limites do mapa
        self.core.x = max(0, min(self.core.x, LARGURA - TAMANHO_CORTADOR))
        self.core.y = max(0, min(self.core.y, ALTURA - TAMANHO_CORTADOR))

        # Marca a nova área como cortada
        if 0 <= self.core.y // TAMANHO_CORTADOR < len(grama_cortada) and \
        0 <= self.core.x // TAMANHO_CORTADOR < len(grama_cortada[0]):
            grama_cortada[self.core.y // TAMANHO_CORTADOR][self.core.x // TAMANHO_CORTADOR] = True


        # Adiciona a nova posição aos visitados
        self.visitados.add((self.core.x, self.core.y))








    def recaucular_rota(self):
        """
        Recalcula a rota com base nos sensores, priorizando grama não cortada
        e evitando concreto ao máximo, sem revisitar células.
        """
        # Obtenha dados dos sensores
        dados_sensores = self.sensores.get_data(self.core.x, self.core.y)

        # Separar direções por prioridade
        direcoes_grama = []  # Prioridade 1: grama não cortada
        direcoes_concreto = []  # Prioridade 2: concreto
        for dado in dados_sensores:
            direcao = dado["direcao"]
            tipo = dado["tipo"]
            pos = dado["posicao"]

            # Verifica se a posição está dentro dos limites do mapa e não foi visitada
            if 0 <= pos[1] // TAMANHO_CORTADOR < len(grama_cortada) and \
            0 <= pos[0] // TAMANHO_CORTADOR < len(grama_cortada[0]) and \
            pos not in self.visitados:
                if tipo == "Grama" and not grama_cortada[pos[1] // TAMANHO_CORTADOR][pos[0] // TAMANHO_CORTADOR]:
                    direcoes_grama.append((direcao, pos))
                elif tipo == "Concreto":
                    direcoes_concreto.append((direcao, pos))

        # Prioridade 1: Direções com grama não cortada
        if direcoes_grama:
            direcao, pos = direcoes_grama[0]
            self.visitados.add(pos)  # Marca a posição como visitada
            return direcao

        # Prioridade 2: Direções com concreto (último recurso)
        if direcoes_concreto:
            direcao, pos = direcoes_concreto[0]
            self.visitados.add(pos)  # Marca a posição como visitada
            return direcao

        # Caso nenhuma direção válida seja encontrada, busca a célula de grama mais próxima
        return self.buscar_grama_mais_proxima()



    def buscar_grama_mais_proxima(self):
        """
        Busca a célula de grama mais próxima que ainda não foi cortada utilizando BFS,
        evitando obstáculos e concreto sempre que possível.
        """
        movimentos = {
            "UP": (0, -TAMANHO_CORTADOR),
            "DOWN": (0, TAMANHO_CORTADOR),
            "LEFT": (-TAMANHO_CORTADOR, 0),
            "RIGHT": (TAMANHO_CORTADOR, 0),
        }

        visitados = set()
        fila = [(self.core.x, self.core.y, None)]  # (x, y, direção inicial)

        while fila:
            x, y, direcao_inicial = fila.pop(0)

            # Evita visitar a mesma célula várias vezes
            if (x, y) in visitados:
                continue
            visitados.add((x, y))

            # Verifica se a célula atual é de grama não cortada
            if 0 <= y // TAMANHO_CORTADOR < len(grama_cortada) and \
            0 <= x // TAMANHO_CORTADOR < len(grama_cortada[0]) and \
            not grama_cortada[y // TAMANHO_CORTADOR][x // TAMANHO_CORTADOR]:
                return direcao_inicial

            # Adiciona os vizinhos à fila
            for direcao, (dx, dy) in movimentos.items():
                novo_x, novo_y = x + dx, y + dy

                # Garante que a nova posição está dentro dos limites do mapa e evita obstáculos
                if 0 <= novo_y // TAMANHO_CORTADOR < len(grama_cortada) and \
                0 <= novo_x // TAMANHO_CORTADOR < len(grama_cortada[0]) and \
                not self.sensores.sensor_ultrassonico(x, y, direcao):  # Ignora obstáculos
                    fila.append((novo_x, novo_y, direcao if direcao_inicial is None else direcao_inicial))

        # Caso nenhuma célula válida seja encontrada, escolha uma direção aleatória (fallback)
        return random.choice(["UP", "DOWN", "LEFT", "RIGHT"])




class Painel:
    def __init__(self, cortador, largura=PANEL_WIDTH, altura=ALTURA):
        self.largura = largura
        self.altura = altura  # Use diretamente o parâmetro ALTURA
        self.cortador = cortador
        self.velocidade = cortador.core.velocidade
        self.altura_cortador = cortador.core.altura  # Use um nome separado
        self.power = cortador.core.power

        # self.sensor_ultrassonico = cortador.sensores.sensor_ultrassonico(cortador.core.x, cortador.core.y, cortador.direcao)
        # self.sensor_cor = cortador.sensores.sensor_cor(cortador.core.x, cortador.core.y)

    def desenhar(self):
        if not isinstance(self.largura, (int, float)) or not isinstance(self.altura, (int, float)):
            raise ValueError("A largura e a altura do painel devem ser números.")

        pygame.draw.rect(tela, (0, 0, 0), (LARGURA, 0, self.largura, self.altura))

        texto_posicao = fonte.render(f"Posição: ({self.cortador.core.x // TAMANHO_CORTADOR}, {self.cortador.core.y // TAMANHO_CORTADOR})", True, COR_TEXTO)
        tela.blit(texto_posicao, (LARGURA + 10, 10))

        texto_velocidade = fonte.render(f"Velocidade: {self.velocidade}", True, COR_TEXTO)
        tela.blit(texto_velocidade, (LARGURA + 10, 40))

        texto_altura = fonte.render(f"Altura: {self.altura_cortador}", True, COR_TEXTO)
        tela.blit(texto_altura, (LARGURA + 10, 70))

        texto_power = fonte.render(f"Power: {self.power}", True, COR_TEXTO)
        tela.blit(texto_power, (LARGURA + 10, 100))

        # texto_sensor_ultrassonico = fonte.render(f"Sensor Ultrassônico: {self.sensor_ultrassonico}", True, COR_TEXTO)
        # tela.blit(texto_sensor_ultrassonico, (LARGURA + 10, 130))

        # texto_sensor_cor = fonte.render(f"Sensor de Cor: {self.sensor_cor}", True, COR_TEXTO)
        # tela.blit(texto_sensor_cor, (LARGURA + 10, 160))

    def atualizar(self):
        self.power, self.velocidade, self.altura_cortador = self.cortador.core.atualiza_comando()        

        # self.sensor_ultrassonico = self.cortador.sensores.sensor_ultrassonico(self.cortador.core.x, self.cortador.core.y, self.cortador.direcao)
        # self.sensor_cor = self.cortador.sensores.sensor_cor(self.cortador.core.x, self.cortador.core.y)


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

class MockSensors:
    def __init__(self, screen, tile_size, obstacles, concrete_zones):
        """
        Classe responsável por simular os sensores do cortador de grama.
        :param screen: Tela do pygame para verificar cores em tempo real.
        :param tile_size: Tamanho dos quadrados no mapa.
        :param obstacles: Lista de coordenadas dos obstáculos.
        :param concrete_zones: Lista de retângulos de zonas de concreto.
        """
        self.screen = screen
        self.tile_size = tile_size
        self.obstacles = obstacles
        self.concrete_zones = concrete_zones

    def sensor_ultrassonico(self, x, y, direction):
        """
        Simula o sensor ultrassônico detectando obstáculos na direção especificada.
        :param x: Posição atual no eixo X.
        :param y: Posição atual no eixo Y.
        :param direction: Direção para verificar ("UP", "DOWN", "LEFT", "RIGHT").
        :return: True se houver obstáculo diretamente à frente, False caso contrário.
        """
        if direction == "UP":
            target = (x, y - self.tile_size)
        elif direction == "DOWN":
            target = (x, y + self.tile_size)
        elif direction == "LEFT":
            target = (x - self.tile_size, y)
        elif direction == "RIGHT":
            target = (x + self.tile_size, y)
        else:
            raise ValueError("Direção inválida.")

        # Verifica se o obstáculo está na direção especificada
        return target in self.obstacles

    def sensor_cor(self, x, y, direction):
        """
        Simula o sensor de cor detectando o tipo de piso na direção especificada.
        :param x: Posição atual no eixo X.
        :param y: Posição atual no eixo Y.
        :param direction: Direção para verificar ("UP", "DOWN", "LEFT", "RIGHT").
        :return: "Grama" se o piso for grama, "Concreto" se for concreto.
        """
        direcoes_validas = ["UP", "DOWN", "LEFT", "RIGHT"]
        if direction not in direcoes_validas:
            raise ValueError(f"Direção inválida: {direction}")

        if direction == "UP":
            target = (x, y - self.tile_size)
        elif direction == "DOWN":
            target = (x, y + self.tile_size)
        elif direction == "LEFT":
            target = (x - self.tile_size, y)
        elif direction == "RIGHT":
            target = (x + self.tile_size, y)
        else:
            raise ValueError("Direção inválida.")

        target_rect = pygame.Rect(target[0], target[1], self.tile_size, self.tile_size)
        for zone in self.concrete_zones:
            if zone.colliderect(target_rect):
                return "Concreto"
        return "Grama"

    def get_data(self, x, y):
        """
        Retorna dados dos sensores, incluindo posição e tipo de cada célula adjacente.
        :param x: Posição atual no eixo X.
        :param y: Posição atual no eixo Y.
        :return: Lista de dicionários com informações de cada célula adjacente.
        """
        directions = ["UP", "DOWN", "LEFT", "RIGHT"]
        data = []

        for direction in directions:
            if direction == "UP":
                pos = (x, y - self.tile_size)
            elif direction == "DOWN":
                pos = (x, y + self.tile_size)
            elif direction == "LEFT":
                pos = (x - self.tile_size, y)
            elif direction == "RIGHT":
                pos = (x + self.tile_size, y)

            tipo = "Obstáculo" if self.sensor_ultrassonico(x, y, direction) else self.sensor_cor(x, y, direction)
            data.append({"direcao": direction, "posicao": pos, "tipo": tipo})

        return data

# Lista de obstáculos
obstaculos = []

# Estação de carga
estacao_carga = (0, 0)

# Inicializar o cortador
cortador = Cortador()
painel = Painel(cortador)

# Loop principal
rodando = True
clock = pygame.time.Clock()

while rodando:
    # Verifica se toda a grama foi cortada
    if all(all(cortada for cortada in linha) for linha in grama_cortada):
        print("Toda a grama foi cortada! O simulador será encerrado em 3 segundos.")
        sleep(3)
        rodando = False
        break

    # Desenhar o mapa ao lado direito do painel
    tela.fill(COR_GRAMA)

    # Desenhar o painel
    painel.desenhar()
    painel.atualizar()

    # Áreas de pisos de concreto no mapa
    pisos_concreto = [
        (200, 100, 100, 300),  # Um bloco retangular de concreto
        (400, 200, 200, 100),  # Outro bloco retangular
    ]
    
    # Desenhar os blocos de concreto
    for piso in pisos_concreto:
        x, y, largura, altura = piso
        pygame.draw.rect(tela, COR_CONCRETO, (x, y, largura, altura))
    
    # Cria obstáculos ao redor do mapa
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

    cortador.mover()

    pygame.draw.rect(tela, COR_CORTADOR, (cortador.core.x, cortador.core.y, TAMANHO_CORTADOR, TAMANHO_CORTADOR))

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
