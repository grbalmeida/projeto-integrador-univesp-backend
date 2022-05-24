import json

import pytest

from app import app


@pytest.fixture
def client():
    app.config['DATABASE_HOST'] = 'localhost'
    app.config['DATABASE_NAME'] = 'hub_solidario_desenvolvimento_tests'
    app.config['DATABASE_USER'] = 'postgres'
    app.config['DATABASE_PASSWORD'] = 'default_123'
    app.config['APP_SETTINGS'] = 'config.TestsConfig'
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

def test_cep_deve_ser_preenchido(client):
    data = {
        "nome": "Instituição Teste",
        "cnpj": "01803408000164",
        "descricao": "Descrição Teste",
        "categoria": 6,
        "exibirEndereco": "S",
        "cep": "",
        "rua": "",
        "numero": "",
        "complemento": "",
        "bairro": "",
        "cidade": "",
        "estado": "",
        "pais": "",
    }
    response = client.post("/cadastrar", data=data)

    data = json.loads(response.data)

    assert response.status_code == 400
    assert 'CEP é obrigatório' in data['errors']

def test_cep_deve_possuir_no_maximo_8_caracteres(client):
    data = {
        "nome": "Instituição Teste",
        "cnpj": "01803408000164",
        "descricao": "Descrição Teste",
        "categoria": 6,
        "exibirEndereco": "S",
        "cep": "010010001",
        "rua": "",
        "numero": "",
        "complemento": "",
        "bairro": "",
        "cidade": "",
        "estado": "",
        "pais": "",
    }
    response = client.post("/cadastrar", data=data)

    data = json.loads(response.data)

    assert response.status_code == 400
    assert 'CEP deve possuir no máximo 8 caracteres' in data['errors']

def test_rua_deve_ser_preenchida(client):
    data = {
        "nome": "Instituição Teste",
        "cnpj": "01803408000164",
        "descricao": "Descrição Teste",
        "categoria": 6,
        "exibirEndereco": "S",
        "cep": "010010001",
        "rua": "",
        "numero": "",
        "complemento": "",
        "bairro": "",
        "cidade": "",
        "estado": "",
        "pais": "",
    }
    response = client.post("/cadastrar", data=data)

    data = json.loads(response.data)

    assert response.status_code == 400
    assert 'Rua/Avenida é obrigatória' in data['errors']

def test_rua_deve_possuir_no_maximo_100_caracteres(client):
    data = {
        "nome": "Instituição Teste",
        "cnpj": "01803408000164",
        "descricao": "Descrição Teste",
        "categoria": 6,
        "exibirEndereco": "S",
        "cep": "010010001",
        "rua": "R" * 101,
        "numero": "",
        "complemento": "",
        "bairro": "",
        "cidade": "",
        "estado": "",
        "pais": "",
    }
    response = client.post("/cadastrar", data=data)

    data = json.loads(response.data)

    assert response.status_code == 400
    assert 'Rua/Avenida deve possuir no máximo 100 caracteres' in data['errors']

def test_numero_deve_ser_preenchido(client):
    data = {
        "nome": "Instituição Teste",
        "cnpj": "01803408000164",
        "descricao": "Descrição Teste",
        "categoria": 6,
        "exibirEndereco": "S",
        "cep": "010010001",
        "rua": "",
        "numero": "",
        "complemento": "",
        "bairro": "",
        "cidade": "",
        "estado": "",
        "pais": "",
    }
    response = client.post("/cadastrar", data=data)

    data = json.loads(response.data)

    assert response.status_code == 400
    assert 'Número é obrigatório' in data['errors']

def test_numero_deve_possuir_no_maximo_50_caracteres(client):
    data = {
        "nome": "Instituição Teste",
        "cnpj": "01803408000164",
        "descricao": "Descrição Teste",
        "categoria": 6,
        "exibirEndereco": "S",
        "cep": "010010001",
        "rua": "Rua Teste",
        "numero": "1" * 51,
        "complemento": "",
        "bairro": "",
        "cidade": "",
        "estado": "",
        "pais": "",
    }
    response = client.post("/cadastrar", data=data)

    data = json.loads(response.data)

    assert response.status_code == 400
    assert 'Número deve possuir no máximo 50 caracteres' in data['errors']

def test_complemento_deve_possuir_no_maximo_100_caracteres(client):
    data = {
        "nome": "Instituição Teste",
        "cnpj": "01803408000164",
        "descricao": "Descrição Teste",
        "categoria": 6,
        "exibirEndereco": "S",
        "cep": "010010001",
        "rua": "Rua Teste",
        "numero": "123",
        "complemento": "C" * 101,
        "bairro": "",
        "cidade": "",
        "estado": "",
        "pais": "",
    }
    response = client.post("/cadastrar", data=data)

    data = json.loads(response.data)

    assert response.status_code == 400
    assert 'Complemento deve possuir no máximo 100 caracteres' in data['errors']

def test_bairro_deve_ser_preenchido(client):
    data = {
        "nome": "Instituição Teste",
        "cnpj": "01803408000164",
        "descricao": "Descrição Teste",
        "categoria": 6,
        "exibirEndereco": "S",
        "cep": "010010001",
        "rua": "Rua Teste",
        "numero": "123",
        "complemento": "Complemento Teste",
        "bairro": "",
        "cidade": "",
        "estado": "",
        "pais": "",
    }
    response = client.post("/cadastrar", data=data)

    data = json.loads(response.data)

    assert response.status_code == 400
    assert 'Bairro é obrigatório' in data['errors']

def test_bairro_deve_possuir_no_maximo_100_caracteres(client):
    data = {
        "nome": "Instituição Teste",
        "cnpj": "01803408000164",
        "descricao": "Descrição Teste",
        "categoria": 6,
        "exibirEndereco": "S",
        "cep": "010010001",
        "rua": "Rua Teste",
        "numero": "123",
        "complemento": "Complemento Teste",
        "bairro": "B" * 101,
        "cidade": "",
        "estado": "",
        "pais": "",
    }
    response = client.post("/cadastrar", data=data)

    data = json.loads(response.data)

    assert response.status_code == 400
    assert 'Bairro deve possuir no máximo 100 caracteres' in data['errors']

def test_cidade_deve_ser_preenchida(client):
    data = {
        "nome": "Instituição Teste",
        "cnpj": "01803408000164",
        "descricao": "Descrição Teste",
        "categoria": 6,
        "exibirEndereco": "S",
        "cep": "010010001",
        "rua": "Rua Teste",
        "numero": "123",
        "complemento": "Complemento Teste",
        "bairro": "Bairro Teste",
        "cidade": "",
        "estado": "",
        "pais": "",
    }
    response = client.post("/cadastrar", data=data)

    data = json.loads(response.data)

    assert response.status_code == 400
    assert 'Cidade é obrigatória' in data['errors']

def test_cidade_deve_possuir_no_maximo_100_caracteres(client):
    data = {
        "nome": "Instituição Teste",
        "cnpj": "01803408000164",
        "descricao": "Descrição Teste",
        "categoria": 6,
        "exibirEndereco": "S",
        "cep": "010010001",
        "rua": "Rua Teste",
        "numero": "123",
        "complemento": "Complemento Teste",
        "bairro": "Bairro Teste",
        "cidade": "C" * 101,
        "estado": "",
        "pais": "",
    }
    response = client.post("/cadastrar", data=data)

    data = json.loads(response.data)

    assert response.status_code == 400
    assert 'Cidade deve possuir no máximo 100 caracteres' in data['errors']

def test_estado_deve_ser_preenchido(client):
    data = {
        "nome": "Instituição Teste",
        "cnpj": "01803408000164",
        "descricao": "Descrição Teste",
        "categoria": 6,
        "exibirEndereco": "S",
        "cep": "010010001",
        "rua": "Rua Teste",
        "numero": "123",
        "complemento": "Complemento Teste",
        "bairro": "Bairro Teste",
        "cidade": "Cidade Teste",
        "estado": "",
        "pais": "",
    }
    response = client.post("/cadastrar", data=data)

    data = json.loads(response.data)

    assert response.status_code == 400
    assert 'Estado é obrigatório' in data['errors']

def test_estado_deve_possuir_no_maximo_100_caracteres(client):
    data = {
        "nome": "Instituição Teste",
        "cnpj": "01803408000164",
        "descricao": "Descrição Teste",
        "categoria": 6,
        "exibirEndereco": "S",
        "cep": "010010001",
        "rua": "Rua Teste",
        "numero": "123",
        "complemento": "Complemento Teste",
        "bairro": "Bairro Teste",
        "cidade": "Cidade Teste",
        "estado": "E" * 101,
        "pais": "",
    }
    response = client.post("/cadastrar", data=data)

    data = json.loads(response.data)

    assert response.status_code == 400
    assert 'Estado deve possuir no máximo 100 caracteres' in data['errors']

def test_pais_deve_ser_preenchido(client):
    data = {
        "nome": "Instituição Teste",
        "cnpj": "01803408000164",
        "descricao": "Descrição Teste",
        "categoria": 6,
        "exibirEndereco": "S",
        "cep": "010010001",
        "rua": "Rua Teste",
        "numero": "123",
        "complemento": "Complemento Teste",
        "bairro": "Bairro Teste",
        "cidade": "Cidade Teste",
        "estado": "Estado Teste",
        "pais": "",
    }
    response = client.post("/cadastrar", data=data)

    data = json.loads(response.data)

    assert response.status_code == 400
    assert 'País é obrigatório' in data['errors']

def test_pais_deve_possuir_no_maximo_100_caracteres(client):
    data = {
        "nome": "Instituição Teste",
        "cnpj": "01803408000164",
        "descricao": "Descrição Teste",
        "categoria": 6,
        "exibirEndereco": "S",
        "cep": "010010001",
        "rua": "Rua Teste",
        "numero": "123",
        "complemento": "Complemento Teste",
        "bairro": "Bairro Teste",
        "cidade": "Cidade Teste",
        "estado": "Estado Teste",
        "pais": "P" * 101,
    }
    response = client.post("/cadastrar", data=data)

    data = json.loads(response.data)

    assert response.status_code == 400
    assert 'País deve possuir no máximo 100 caracteres' in data['errors']