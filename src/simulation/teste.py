import json
import os
import sys

def event_handle_by_api():
    path = "../GrassBot/src/api/data/data.json"
    try:
        with open(path, "r") as file:
            data = json.load(file)
            return data
    except Exception as e:
        print(e)
        return
    
    pass

def map_speed(value, min_speed=2, max_speed=1000):
    """
    Mapeia um valor de 0 a 100 para o intervalo de cut_speed.

    Args:
        value (int): O valor de entrada (de 0 a 100).
        min_speed (int): O valor mínimo para cut_speed.
        max_speed (int): O valor máximo para cut_speed.

    Returns:
        int: O valor mapeado para cut_speed.
    """
    # Garantir que o valor esteja entre 0 e 100
    value = max(0, min(100, value))
    
    # Mapear o valor para o intervalo de cut_speed
    mapped_speed = int(min_speed + (value / 100) * (max_speed - min_speed))
    return mapped_speed

def adjust_cut_speed(value, min_speed=2, max_speed=95):
    cut_speed = 15
    value = max(0, min(100, value))
    value = 100 - value

    if value < 50:  # Aumentar a velocidade (reduzir cut_speed)
        value = value//10
        value = value//2
        for _ in range(value):
            cut_speed = int(cut_speed * 0.5) + 1
            if cut_speed <= min_speed:
                return min_speed
    else:  # Diminuir a velocidade (aumentar cut_speed)
        value = value//10
        value = value//2
        for _ in range(value):
            cut_speed = int(cut_speed * 2) + 1
            if cut_speed >= max_speed:
                return max_speed
    return cut_speed



print(adjust_cut_speed(100))
