import json

class GrassBot:
    def __init__(self):
        try:
            with open("src/api/data/data.json", "r") as f:
                data = json.load(f)
                self.ligado = data["ligado"]
                self.altura_corte = data["altura_corte"]
                self.velocidade = data["velocidade"]
        except FileNotFoundError:
            print("O arquivo data.json não foi encontrado. Nenhum dado foi carregado.")
        except json.JSONDecodeError:
            print("O arquivo data.json está corrompido. Nenhum dado foi carregado.")

    def save(self):
        data = {
            "ligado": self.ligado,
            "altura_corte": self.altura_corte,
            "velocidade": self.velocidade
        }
        with open("src/api/data/data.json", "w") as f:
            json.dump(data, f, indent=4)

    def update(self, data):

        if "ligado" in data:
            self.ligado = data["ligado"]
        if "altura_corte" in data:
            self.altura_corte = data["altura_corte"]
        if "velocidade" in data:
            self.velocidade = data["velocidade"]

        self.save()

        response = {
            "message": "Cortador atualizado",
            "status": {
                "ligado": self.ligado,
                "altura_corte": self.altura_corte,
                "velocidade": self.velocidade
            }
        }

        return response
    

grassbot = GrassBot()
