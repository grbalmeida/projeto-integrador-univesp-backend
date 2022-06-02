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
        "email": "", "telefone_celular": "", "telefone_comercial": "",
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
        "email": "", "telefone_celular": "", "telefone_comercial": "",
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
        "email": "", "telefone_celular": "", "telefone_comercial": "",
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
        "email": "", "telefone_celular": "", "telefone_comercial": "",
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
        "email": "", "telefone_celular": "", "telefone_comercial": "",
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
        "email": "", "telefone_celular": "", "telefone_comercial": "",
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
        "email": "", "telefone_celular": "", "telefone_comercial": "",
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
        "email": "", "telefone_celular": "", "telefone_comercial": "",
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
        "email": "", "telefone_celular": "", "telefone_comercial": "",
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
        "email": "", "telefone_celular": "", "telefone_comercial": "",
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
        "email": "", "telefone_celular": "", "telefone_comercial": "",
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
        "email": "", "telefone_celular": "", "telefone_comercial": "",
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
        "email": "", "telefone_celular": "", "telefone_comercial": "",
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
        "email": "", "telefone_celular": "", "telefone_comercial": "",
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
        "email": "", "telefone_celular": "", "telefone_comercial": "",
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
        "email": "", "telefone_celular": "", "telefone_comercial": "",
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
        "email": "", "telefone_celular": "", "telefone_comercial": "",
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
        "email": "", "telefone_celular": "", "telefone_comercial": "",
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
        "email": "", "telefone_celular": "", "telefone_comercial": "",
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
        "email": "", "telefone_celular": "", "telefone_comercial": "",
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
        "email": "", "telefone_celular": "", "telefone_comercial": "",
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
        "email": "", "telefone_celular": "", "telefone_comercial": "",
    }
    response = client.post("/cadastrar", data=data)

    data = json.loads(response.data)

    assert response.status_code == 400
    assert 'País deve possuir no máximo 100 caracteres' in data['errors']

def test_email_deve_ser_preenchido(client):
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
        "email": "", "telefone_celular": "", "telefone_comercial": "",
    }
    response = client.post("/cadastrar", data=data)

    data = json.loads(response.data)

    assert response.status_code == 400
    assert 'E-mail é obrigatório' in data['errors']

def test_email_deve_possuir_no_maximo_100_caracteres(client):
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
        "email": "@" * 101,
        "telefone_celular": "",
        "telefone_comercial": "",
    }
    response = client.post("/cadastrar", data=data)

    data = json.loads(response.data)

    assert response.status_code == 400
    assert 'E-mail deve possuir no máximo 100 caracteres' in data['errors']

def test_email_deve_ser_valido(client):
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
        "email": "AAAaaaa.com.br",
        "telefone_celular": "16991929192",
        "telefone_comercial": "",
    }
    response = client.post("/cadastrar", data=data)

    data = json.loads(response.data)

    assert response.status_code == 400
    assert 'E-mail em formato inválido' in data['errors']

def test_se_email_for_valido_nao_deve_exibir_erro(client):
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
        "email": "instituicao@email.com",
        "telefone_celular": "16991929192",
        "telefone_comercial": "",
    }
    response = client.post("/cadastrar", data=data)

    data = json.loads(response.data)

    assert response.status_code == 400
    assert 'E-mail em formato inválido' not in data['errors']

def test_pelo_menos_um_telefone_deve_ser_preenchido(client):
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
        "email": "@" * 101,
        "telefone_celular": "",
        "telefone_comercial": "",
    }
    response = client.post("/cadastrar", data=data)

    data = json.loads(response.data)

    assert response.status_code == 400
    assert 'Pelo menos um telefone deve ser informado' in data['errors']

def test_se_telefone_celular_informado_nao_exibir_mensagem_de_erro(client):
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
        "email": "@" * 101,
        "telefone_celular": "16991929192",
        "telefone_comercial": "",
    }
    response = client.post("/cadastrar", data=data)

    data = json.loads(response.data)

    assert response.status_code == 400
    assert 'Pelo menos um telefone deve ser informado' not in data['errors']

def test_se_telefone_comercial_informado_nao_exibir_mensagem_de_erro(client):
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
        "email": "@" * 101,
        "telefone_celular": "",
        "telefone_comercial": "1631323132",
    }
    response = client.post("/cadastrar", data=data)

    data = json.loads(response.data)

    assert response.status_code == 400
    assert 'Pelo menos um telefone deve ser informado' not in data['errors']

def test_telefone_comercial_deve_possuir_no_maximo_11_caracteres(client):
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
        "email": "@" * 101,
        "telefone_celular": "",
        "telefone_comercial": "1" * 12,
    }
    response = client.post("/cadastrar", data=data)

    data = json.loads(response.data)

    assert response.status_code == 400
    assert 'Telefone comercial deve possuir no máximo 11 caracteres' in data['errors']

def test_telefone_celular_deve_possuir_no_maximo_12_caracteres(client):
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
        "email": "@" * 101,
        "telefone_celular": "1" * 13,
        "telefone_comercial": "",
    }
    response = client.post("/cadastrar", data=data)

    data = json.loads(response.data)

    assert response.status_code == 400
    assert 'Telefone celular deve possuir no máximo 12 caracteres' in data['errors']