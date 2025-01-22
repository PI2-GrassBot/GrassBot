import json

class GrassBot:
    def __init__(self):
        try:
            with open("src/api/data/data.json", "r") as f:
                data = json.load(f)
                self.ligado = data["ligado"]
                self.altura_corte = data["altura_corte"]
                self.velocidade = data["velocidade"]
                self.speed_up = data["speed_up"]
                self.speed_down = data["speed_down"]
                self.map = data["map"]
        except FileNotFoundError:
            print("O arquivo data.json não foi encontrado. Nenhum dado foi carregado.")
        except json.JSONDecodeError:
            print("O arquivo data.json está corrompido. Nenhum dado foi carregado.")

    def save(self):
        data = {
            "ligado": self.ligado,
            "altura_corte": self.altura_corte,
            "velocidade": self.velocidade,
            "speed_up": self.speed_up,
            "speed_down": self.speed_down,
            "map": self.map
        }
        with open("src/api/data/data.json", "w") as f:
            json.dump(data, f, indent=4)

    def update(self, data):

        if "ligado" in data:
            self.ligado = data["ligado"]
        if "altura" in data:
            self.altura_corte = data["altura"]
        if "velocidade" in data:
            self.velocidade = data["velocidade"]
        if "speed_up" in data:
            self.speed_up = data["speed_up"]
        if "speed_down" in data:
            self.speed_down = data["speed_down"]
        if "map" in data:
            self.map = data["map"]

        self.save()

        response = {
            "message": "Cortador atualizado",
            "status": {
                "ligado": self.ligado,
                "altura_corte": self.altura_corte,
                "velocidade": self.velocidade,
                "speed_up": self.speed_up,
                "speed_down": self.speed_down,
                "map": self.map
            }
        }

        return response
    

grassbot = GrassBot()
