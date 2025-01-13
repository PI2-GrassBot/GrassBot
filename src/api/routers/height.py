from flask import Blueprint, request, jsonify
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from flask import Blueprint, request, jsonify
from models.grassBot import GrassBot

altura_corte_bp = Blueprint('altura_corte', __name__)

ALLOWED_ALTURAS = ["baixa", "média", "alta"]

@altura_corte_bp.route('/altura_corte', methods=['POST'])
def handle_altura_corte():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"message": "Request body is missing or invalid."}), 400

        altura = data.get("altura")
        if altura not in ALLOWED_ALTURAS:
            return jsonify({
                "message": f"Altura inválida. Valores permitidos: {', '.join(ALLOWED_ALTURAS)}."
            }), 400

        database = GrassBot()
        response = database.update(data=data)

        return jsonify(response), 200

    except Exception as e:
        return jsonify({"message": "Ocorreu um erro no servidor.", "error": str(e)}), 500
