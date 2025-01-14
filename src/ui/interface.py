import os
from flask import Flask, render_template
from dotenv import load_dotenv

# Carregar as variáveis do arquivo .env
load_dotenv()

app = Flask(__name__)


# Obtém a URL da API do .env
API_URL = os.getenv("API_URL")

@app.route('/')
def home():
    return render_template('index.html', api_url=API_URL)

if __name__ == '__main__':
    app.run(debug=True)
