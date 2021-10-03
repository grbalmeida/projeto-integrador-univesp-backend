import os
import json
from flask import Flask, request, send_file

from database.categoria import Categoria
from database.instituicao import Instituicao

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])

@app.route("/")
def index():
    return f'Hub Solidário Araraquara API'

@app.route("/categorias", methods=['GET'])
def get_categorias():
    categoria = Categoria()
    categorias = categoria.obter_todos()

    results = [
        {
            "id": cat['cat_id'],
            "nome": cat['nome']
        } for cat in categorias
    ]

    return json.dumps(results, ensure_ascii=False)

@app.route("/categorias/<categoria_id>", methods=['GET'])
def get_categoria(categoria_id):
    categoria = Categoria()
    cat = categoria.obter(categoria_id)

    if cat is None:
        return json.dumps({})
    else:
        result = {'id': cat['cat_id'], 'nome': cat['nome']}
        return json.dumps(result, ensure_ascii=False)

@app.route("/instituicoes", methods=['GET'])
def get_instituicoes():
    nome = request.args.get('nome')
    categoria_id = request.args.get('categoria_id')

    instituicao = Instituicao()
    instituicoes = instituicao.obter_instituicoes(nome, categoria_id)

    return json.dumps(instituicoes, ensure_ascii=False)

@app.route("/instituicoes/<instituicao_id>", methods=['GET'])
def get_instituicao(instituicao_id):
    instituicao = Instituicao()
    inst = instituicao.obter_instituicao(instituicao_id)

    return json.dumps(inst, ensure_ascii=False)

@app.route("/imagens/<imagem>", methods=['GET'])
def get_imagem(imagem):
    diretorio = os.getcwd()
    nome_arquivo = diretorio + os.path.join(r'/app/assets/imagens/', imagem)

    return send_file(nome_arquivo, mimetype='image/jpg')

if __name__ == '__main__':
    app.run()