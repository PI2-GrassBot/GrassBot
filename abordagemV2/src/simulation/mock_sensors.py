import pygame

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

