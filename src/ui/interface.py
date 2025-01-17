import os
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html', api_url='localhost:5000')

if __name__ == '__main__':
    app.run(debug=True)
