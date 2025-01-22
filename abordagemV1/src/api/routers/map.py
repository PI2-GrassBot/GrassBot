from flask import Blueprint, request, jsonify
from models.grassBot import GrassBot

map_bp = Blueprint('map', __name__)


@map_bp.route('/map', methods=['GET'])
def handle_speed_up():
    try:
        database = GrassBot()
        response = database.update({"map": True})

        return jsonify(response), 200

    except Exception as e:
        return jsonify({"message": "Ocorreu um erro no servidor.", "error": str(e)}), 500

