import os
import sys

from flask import Flask
from routers.height import altura_corte_bp
from routers.speed import velocidade_bp
from routers.ligar import power_bp
from flask_cors import CORS

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

app = Flask(__name__)
CORS(app)

app.register_blueprint(altura_corte_bp)
app.register_blueprint(velocidade_bp)
app.register_blueprint(power_bp)

API_URL = os.getenv("API_URL")


@app.route('/')
def home():
    return ('<h1>Grassbot API</h1>')

if __name__ == '__main__':
    app.run(debug=True, port=5001)