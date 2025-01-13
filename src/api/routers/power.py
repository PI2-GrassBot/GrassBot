import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from flask import Blueprint, request, jsonify
from models.grassBot import GrassBot

power_bp = Blueprint('power', __name__)


@power_bp.route('/power', methods=['POST'])
def handle_power():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"message": "Request body is missing or invalid."}), 400

        power = data.get("ligado")
        if type(power) != bool:
            return jsonify({"message": "Valor inválido. O valor deve ser true ou false."}), 400
        
        database = GrassBot()
        response = database.update(data=data)

        return jsonify(response), 200

    except Exception as e:
        return jsonify({"message": "Ocorreu um erro no servidor.", "error": str(e)}), 500
