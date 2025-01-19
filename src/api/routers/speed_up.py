from flask import Blueprint, request, jsonify
from models.grassBot import GrassBot

speed_up_bp = Blueprint('speed_up', __name__)


@speed_up_bp.route('/speed-up', methods=['GET'])
def handle_speed_up():
    try:
        database = GrassBot()
        response = database.update({"speed_up": True})

        return jsonify(response), 200

    except Exception as e:
        return jsonify({"message": "Ocorreu um erro no servidor.", "error": str(e)}), 500

