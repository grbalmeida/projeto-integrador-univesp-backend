import os
import json
from flask import Flask

from database.categoria import Categoria

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])

@app.route("/")
def index():
    return f'Hello World!'

@app.route("/categorias", methods=['GET'])
def get_categorias():
    categoria = Categoria()
    categorias = categoria.obter_todos()

    results = [
        {
            "id": cat_id,
            "nome": nome
        } for cat_id, nome in categorias
    ]

    return json.dumps(results)

if __name__ == '__main__':
    app.run()