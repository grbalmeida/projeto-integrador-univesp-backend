import json

import pytest

from app import app


@pytest.fixture
def client():
    app.config['DATABASE_USER'] = 'test'
    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client

def test_nome_deve_ser_preenchido(client):
    data = {
        "nome": "",
        "cnpj": "01803408000164",
        "descricao": "Descrição Teste",
        "categoria": 6,
        "exibirEndereco": "",
    }
    response = client.post("/cadastrar", data=data)

    data = json.loads(response.data)

    assert response.status_code == 400
    assert 'Nome é obrigatório' in data['errors']

def test_nome_deve_possuir_no_maximo_255_caracteres(client):
    data = {
        "nome": 'A' * 256,
        "cnpj": "01803408000164",
        "descricao": "Descrição Teste",
        "categoria": 6,
        "exibirEndereco": "",
    }
    response = client.post("/cadastrar", data=data)

    data = json.loads(response.data)

    assert response.status_code == 400
    assert 'Nome deve possuir no máximo 255 caracteres' in data['errors']

def test_cnpj_deve_ser_preenchido(client):
    data = {
        "nome": "Instituição Teste",
        "cnpj": "",
        "descricao": "Descrição Teste",
        "categoria": 6,
        "exibirEndereco": "",
    }
    response = client.post("/cadastrar", data=data)

    data = json.loads(response.data)

    assert response.status_code == 400
    assert 'CNPJ é obrigatório' in data['errors']

def test_cnpj_deve_possuir_no_maximo_18_caracteres(client):
    data = {
        "nome": "Instituição Teste",
        "cnpj": "1" * 19,
        "descricao": "Descrição Teste",
        "categoria": 6,
        "exibirEndereco": "",
    }
    response = client.post("/cadastrar", data=data)

    data = json.loads(response.data)

    assert response.status_code == 400
    assert 'CNPJ deve possuir no máximo 18 caracteres' in data['errors']

def test_descricao_deve_ser_preenchida(client):
    data = {
        "nome": "Instituição Teste",
        "cnpj": "01803408000164",
        "descricao": "",
        "categoria": 6,
        "exibirEndereco": "",
    }
    response = client.post("/cadastrar", data=data)

    data = json.loads(response.data)

    assert response.status_code == 400
    assert 'Descrição é obrigatória' in data['errors']

def test_categoria_deve_ser_preenchida(client):
    data = {
        "nome": "Instituição Teste",
        "cnpj": "01803408000164",
        "descricao": "Descrição Teste",
        "categoria": "",
        "exibirEndereco": "",
    }
    response = client.post("/cadastrar", data=data)

    data = json.loads(response.data)

    assert response.status_code == 400
    assert 'Categoria é obrigatória' in data['errors']

def test_descricao_deve_possuir_no_maximo_1000_caracteres(client):
    data = {
        "nome": "Instituição Teste",
        "cnpj": "01803408000164",
        "descricao": "D" * 1001,
        "categoria": 6,
        "exibirEndereco": "",
    }
    response = client.post("/cadastrar", data=data)

    data = json.loads(response.data)

    assert response.status_code == 400
    assert 'Descrição deve possuir no máximo 1000 caracteres' in data['errors']