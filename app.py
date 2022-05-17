import os
import json
from flask import Flask, request, send_file
from werkzeug.exceptions import NotFound

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

    try:
        return send_file(nome_arquivo, mimetype='image/jpg')
    except FileNotFoundError:
        return NotFound()

@app.route("/imagens-home/<imagem>", methods=['GET'])
def get_imagem_home(imagem):
    diretorio = os.getcwd()
    nome_arquivo = diretorio + os.path.join(r'/app/assets/imagens-home/', imagem)

    try:
        return send_file(nome_arquivo, mimetype='image/png')
    except FileNotFoundError:
        return NotFound()

@app.route("/qrcode/<qrcode>", methods=['GET'])
def get_qrcode(qrcode):
    diretorio = os.getcwd()
    nome_arquivo = diretorio + os.path.join(r'/app/assets/qrcode/', qrcode)

    try:
        return send_file(nome_arquivo, mimetype='image/jpg')
    except FileNotFoundError:
        return NotFound()

@app.route("/imgs", methods=['GET'])
def get_images():

    diretorio_raiz = os.getcwd()
    diretorio_images = diretorio_raiz + r'/app/assets/imagens-home/'
    images = os.listdir(diretorio_images)

    imgs = []

    for index, image in enumerate(images):
        imgs.append({
            'index': index,
            'src': request.host_url + 'imagens-home/' + image,
            'name': '',
            'categoria_id': image.replace('.png', '')
        })

    return json.dumps(imgs)

@app.route("/cadastrar", methods=['POST'])
def cadastrar():
    instituicao = Instituicao()
    
    result = {'errors': []}

    if not request.form['nome']:
        result['errors'].append('Nome é obrigatório')

    if not request.form['cnpj']:
        result['errors'].append('CNPJ é obrigatório')

    if not request.form['descricao']:
        result['errors'].append('Descrição é obrigatória')

    if not request.form['categoria']:
        result['errors'].append('Categoria é obrigatória')

    if len(request.form['nome']) > 255:
        result['errors'].append('Nome deve possuir no máximo 255 caracteres')

    if len(request.form['cnpj']) > 18:
        result['errors'].append('CNPJ deve possuir no máximo 18 caracteres')

    if len(request.form['descricao']) > 1000:
        result['errors'].append('Descrição deve possuir no máximo 1000 caracteres')

    if len(result['errors']) > 0:
        return json.dumps({'success':False, 'errors': result['errors']}), 400, {'ContentType':'application/json'}

    result = instituicao.cadastrar(request.form.to_dict())

    if len(result['errors']) > 0:
        return json.dumps({'success':False, 'errors': result['errors']}), 400, {'ContentType':'application/json'}

    return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 

if __name__ == '__main__':
    app.run()