
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
        Simula o sensor ultrassônico detectando obstáculos diretamente à frente.
        :param x: Posição atual no eixo X.
        :param y: Posição atual no eixo Y.
        :param direction: Direção para verificar ("UP", "DOWN", "LEFT", "RIGHT").
        :return: True se houver obstáculo diretamente à frente, False caso contrário.
        """
        if direction == "UP":
            target = (x , y - (self.tile_size))
        elif direction == "DOWN":
            target = (x, y + (self.tile_size))
        elif direction == "LEFT":
            target = (x - (self.tile_size), y)
        elif direction == "RIGHT":
            target = (x + (self.tile_size), y)
        else:
            raise ValueError("Direção inválida.")

        # Verifica apenas se o obstáculo está exatamente à frente
        if target in self.obstacles:
            print("Obstáculo detectado na direção", direction)
            return True

    
    def get_sensor_status(self, x, y, direction):
        """
        Retorna True se houver um obstáculo na direção especificada, False caso contrário.
        :param x: Posição atual no eixo X.
        :param y: Posição atual no eixo Y.
        :param direction: Direção para verificar ("UP", "DOWN", "LEFT", "RIGHT").
        """
        return self.sensor_ultrassonico(x, y, direction)
    
    def set_all_sensors(self, status):
        """
        Define o status de todos os sensores.
        :param status: Status a ser definido (True ou False).
        """
        pass

    def sensor_cor(self, x, y, direction):
    
        """
        Simula o sensor de cor detectando o tipo de piso diretamente à frente.
        :param x: Posição atual no eixo X.
        :param y: Posição atual no eixo Y.
        :param direction: Direção para verificar ("UP", "DOWN", "LEFT", "RIGHT").
        :return: "Grama" se o piso for grama, "Concreto" se for concreto.
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

        # Verifica apenas o piso diretamente à frente
        target_rect = pygame.Rect(target[0], target[1], self.tile_size, self.tile_size)
        for zone in self.concrete_zones:
            if zone.colliderect(target_rect):
                return "Concreto"
        return "Grama"
