import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from flask import Blueprint, request, jsonify
from models.grassBot import GrassBot

velocidade_bp = Blueprint('velocidade', __name__)


@velocidade_bp.route('/velocidade', methods=['POST'])
def handle_velocidade():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"message": "Request body is missing or invalid."}), 400

        velocidade = data.get("velocidade")
        if type(velocidade) != int or velocidade < 0 or velocidade > 100:
            return jsonify({"message": "Velocidade inválida. O valor deve ser um número entre 0 e 100."}), 400

        database = GrassBot()
        response = database.update(data=data)

        return jsonify(response), 200

    except Exception as e:
        return jsonify({"message": "Ocorreu um erro no servidor.", "error": str(e)}), 500
