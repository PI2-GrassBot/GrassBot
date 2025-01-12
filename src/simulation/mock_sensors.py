class MockSensors:
    def __init__(self, sensorUp: bool = False, sensorDown: bool = False, sensorLeft: bool = False, sensorRight: bool = False):
        """
        Classe responsável por simular os sensores do cortador de grama.
        :param sensorA: Estado do sensor A.
        :param sensorB: Estado do sensor B.
        :param sensorC: Estado do sensor C.
        :param sensorD: Estado do sensor D.
        """
        self.sensorUP = sensorUp
        self.sensorDown = sensorDown
        self.sensorLeft = sensorLeft
        self.sensorRight = sensorRight

    def set_sensor(self, sensor: str, estado: bool):
        """
        Define o estado de um sensor.
        :param sensor: Sensor a ser alterado ("A", "B", "C" ou "D").
        :param estado: Novo estado do sensor.
        """
        if sensor == "UP":
            self.sensorUP = estado
        elif sensor == "DOWN":
            self.sensorDown = estado
        elif sensor == "LEFT":
            self.sensorLeft = estado
        elif sensor == "RIGHT":
            self.sensorRight = estado

    def avalia_ambiente(self):
        """
        Retorna lista de sensores ativados.
        """
        return [self.sensorUP, self.sensorDown, self.sensorLeft, self.sensorRight]

    def set_all_sensors(self, estado: bool):
        """
        Define o estado de todos os sensores.
        :param estado: Novo estado dos sensores.
        """
        self.sensorUP = estado
        self.sensorDown = estado
        self.sensorLeft = estado
        self.sensorRight = estado