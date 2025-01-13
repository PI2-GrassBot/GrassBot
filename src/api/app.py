import os
import sys

from flask import Flask, render_template
from routers.height import altura_corte_bp
from routers.speed import velocidade_bp
from routers.power import power_bp

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

app = Flask(__name__, template_folder='././ui/templates')

app.register_blueprint(altura_corte_bp)
app.register_blueprint(velocidade_bp)
app.register_blueprint(power_bp)

API_URL = os.getenv("API_URL")


@app.route('/')
def home():
    return render_template('index.html', api_url=API_URL)

if __name__ == '__main__':
    app.run(debug=True)