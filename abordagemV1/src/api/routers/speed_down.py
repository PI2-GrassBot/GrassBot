from flask import Blueprint, request, jsonify
from models.grassBot import GrassBot

speed_down_bp = Blueprint('speed_down', __name__)


@speed_down_bp.route('/speed-down', methods=['GET'])
def handle_speed_down():
    try:
        database = GrassBot()
        response = database.update({"speed_down": True})

        return jsonify(response), 200

    except Exception as e:
        return jsonify({"message": "Ocorreu um erro no servidor.", "error": str(e)}), 500

