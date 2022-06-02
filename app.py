import os
import re
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
    else:
        cnpj = re.sub('[^0-9]','', request.form['cnpj'])
        if len(cnpj) > 18:
            result['errors'].append('CNPJ deve possuir no máximo 18 caracteres')

    if not request.form['descricao']:
        result['errors'].append('Descrição é obrigatória')

    if not request.form['categoria']:
        result['errors'].append('Categoria é obrigatória')

    if len(request.form['nome']) > 255:
        result['errors'].append('Nome deve possuir no máximo 255 caracteres')

    if len(request.form['descricao']) > 1000:
        result['errors'].append('Descrição deve possuir no máximo 1000 caracteres')
    
    # Validações Endereço

    if request.form['exibirEndereco'] == 'S': # Caso o checkbox de exibir endereço esteja selecionado
        if not request.form['cep']:
            result['errors'].append('CEP é obrigatório')
        else:
            cep = re.sub('[^0-9]','', request.form['cep'])
            if len(cep) > 8:
                result['errors'].append('CEP deve possuir no máximo 8 caracteres')

        if not request.form['rua']:
            result['errors'].append('Rua/Avenida é obrigatória')

        if len(request.form['rua']) > 100:
            result['errors'].append('Rua/Avenida deve possuir no máximo 100 caracteres')

        if not request.form['numero']:
            result['errors'].append('Número é obrigatório')

        if len(request.form['numero']) > 50:
            result['errors'].append('Número deve possuir no máximo 50 caracteres')

        if len(request.form['complemento']) > 100:
            result['errors'].append('Complemento deve possuir no máximo 100 caracteres')

        if not request.form['bairro']:
            result['errors'].append('Bairro é obrigatório')

        if len(request.form['bairro']) > 100:
            result['errors'].append('Bairro deve possuir no máximo 100 caracteres')

        if not request.form['cidade']:
            result['errors'].append('Cidade é obrigatória')
        
        if len(request.form['cidade']) > 100:
            result['errors'].append('Cidade deve possuir no máximo 100 caracteres')

        if not request.form['estado']:
            result['errors'].append('Estado é obrigatório')
        
        if len(request.form['estado']) > 100:
            result['errors'].append('Estado deve possuir no máximo 100 caracteres')

        if not request.form['pais']:
            result['errors'].append('País é obrigatório')

        if len(request.form['pais']) > 100:
            result['errors'].append('País deve possuir no máximo 100 caracteres')

    # Validações Contato

    if not request.form['email']:
        result['errors'].append('E-mail é obrigatório')

    if len(request.form['email']) > 100:
        result['errors'].append('E-mail deve possuir no máximo 100 caracteres')

    if not email_e_valido(request.form['email']):
        result['errors'].append('E-mail em formato inválido')

    if not request.form['telefone_comercial'] and not request.form['telefone_celular']:
        result['errors'].append('Pelo menos um telefone deve ser informado')

    if len(request.form['telefone_comercial']) > 11:
        result['errors'].append('Telefone comercial deve possuir no máximo 11 caracteres')

    if len(request.form['telefone_celular']) > 12:
        result['errors'].append('Telefone celular deve possuir no máximo 12 caracteres')

    if len(result['errors']) > 0:
        print(result['errors'])
        return json.dumps({'success':False, 'errors': result['errors']}), 400, {'ContentType':'application/json'}

    form_dict = request.form.to_dict()
    form_dict['cnpj'] = re.sub('[^0-9]','', form_dict['cnpj'])
    form_dict['cep'] = re.sub('[^0-9]','', form_dict['cep'])
    result = instituicao.cadastrar(form_dict)

    if len(result['errors']) > 0:
        return json.dumps({'success':False, 'errors': result['errors']}), 400, {'ContentType':'application/json'}

    return json.dumps({'success':True, 'errors': []}), 200, {'ContentType':'application/json'} 

def email_e_valido(email):
   pat = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
   return re.match(pat, email)

if __name__ == '__main__':
    app.run()