from database.repository import Repository
from flask import request
from psycopg2.errors import UniqueViolation

class Instituicao(Repository):
    NOME_MAX_LENGTH = 255
    DESCRICAO_MAX_LENGTH = 1000

    def __init__(self):
        super(Instituicao, self).__init__('instituicoes', 'inst_id')

    def cadastrar(self, data):
        sql = """
            INSERT INTO instituicoes (inst_id, inst_name, inst_cnpj, description, cat_id)
            VALUES ((select max(i.inst_id) + 1 from instituicoes i), %s, %s, %s, %s)
        """
    
        result = {'errors': []}

        persistiu_instituicao = False

        try:
            self.cur.execute(sql, (data['nome'], data['cnpj'], data['descricao'], data['categoria']))
            self.connection.commit()
            persistiu_instituicao = True
        except UniqueViolation:
            result['errors'].append('CNPJ informado já está cadastrado')
            persistiu_instituicao = False
        except:
            result['errors'].append('Erro ao salvar a instituição')

        if persistiu_instituicao:
            if data['exibirEndereco']:
                try:
                    sql = """
                        INSERT INTO inst_addresses (inst_id, addr_zipcode, addr_street, addr_number,
                        addr_complement, addr_district, addr_city, addr_state, addr_country, is_active)
                        VALUES ((select max(i.inst_id) from instituicoes i), %s, %s, %s, %s, %s, %s, %s, %s, FALSE)
                    """

                    self.cur.execute(sql, (data['cep'], data['rua'], data['numero'], data['complemento'], data['bairro'], data['cidade'], data['estado'], data['pais']))
                    self.connection.commit()
                except:
                    result['errors'].append('Erro ao salvar o endereço da instituição')

            try:
                sql = """
                    INSERT INTO inst_contacts (inst_id, contact_email, contact_comercial, contact_mobile,
                    contact_site, contact_instagram, contact_facebook, is_active)
                    VALUES
                    ((select max(i.inst_id) from instituicoes i), %s, %s, %s, %s, %s, %s, FALSE)
                """

                self.cur.execute(sql, (data['email'], data['telefone_comercial'], data['telefone_celular'], data['site'], data['instagram'], data['facebook']))
                self.connection.commit()
            except:
                result['errors'].append('Erro ao salvar o contato da instituição')

        return result

    def obter_instituicao(self, id):
        sql = self.get_base_instituicao_sql()
        sql += f' where i.inst_id = {id}'
        sql += ' group by (i.inst_id, c.cat_id, contact.contact_id, address.addr_id)'

        self.cur.execute(sql)
        instituicao = self.cur.fetchone()

        if instituicao is None:
            return {}
        else:
            return self.get_instituicao_to_map(instituicao)
    
    def obter_instituicoes(self, nome = None, categoria_id = None):
        instituicoes = []
        categoria = None

        sql = self.get_base_instituicao_sql()
        sql += ' where 1 = 1 and i.is_active = true '

        if not nome is None:
            sql += f" and LOWER(i.inst_name) like '%{nome.lower()}%'"

        if not categoria_id is None:
            self.cur.execute("select nome from categorias where cat_id = " + categoria_id)
            result_categoria = self.cur.fetchone()

            if result_categoria:
                categoria = {}
                categoria['categoria_id'] = categoria_id
                categoria['nome'] = result_categoria['nome']

            sql += f" and i.cat_id = {categoria_id}"

        sql += ' group by (i.inst_id, c.cat_id, contact.contact_id, address.addr_id)'
        sql += ' order by i.inst_id'

        self.cur.execute(sql)
        result = self.cur.fetchall()

        for instituicao in result:
            instituicoes.append(self.get_instituicao_to_map(instituicao))

        result = {}
        result['instituicoes'] = instituicoes
        result['categoria'] = categoria

        return result

    def get_base_instituicao_sql(self):
        sql = 'select i.inst_id, i.inst_name, i.inst_cnpj,'
        sql += ' i.logo, i.alt_logo, i.description, c.cat_id, c.nome as cat_nome,'
        sql += ' contact.contact_comercial, contact.contact_mobile,'
        sql += ' contact.contact_email, contact.contact_site,'
        sql += ' contact.contact_instagram, contact.contact_facebook,'
        sql += ' contact.contact_twitter, contact.contact_linkedin,'
        sql += ' contact.contact_youtube,'
        sql += ' address.addr_zipcode, address.addr_street,'
        sql += ' address.addr_number, address.addr_complement,'
        sql += ' address.addr_district, address.addr_city,'
        sql += ' address.addr_state, address.addr_country,'
        sql += ' array_agg(account.bank_name) as account_banks,'
        sql += ' array_agg(account.bank_account_ag) account_ag,'
        sql += ' array_agg(account.bank_account_conta) account_accounts,'
        sql += ' array_agg('
        sql += "   CASE WHEN account.bank_account_type = 'Corrente'"
        sql += "    THEN 'Conta Corrente'"
        sql += "    WHEN account.bank_account_type = 'Poupanca'"
        sql += "    THEN 'Conta Poupança'"
        sql += "    ELSE null"
        sql += '    END) account_types,'
        sql += ' array_agg(pix.pix_key) as pix_keys,'
        sql += ' array_agg(pix.qrcode_file) as qrcodes'
        sql += ' from instituicoes i'
        sql += ' inner join categorias c'
        sql += ' on i.cat_id = c.cat_id'
        sql += ' left join inst_contacts contact'
        sql += ' on i.inst_id = contact.inst_id'
        sql += ' left join inst_addresses address'
        sql += ' on i.inst_id = address.inst_id'
        sql += ' left join inst_bank_accounts account'
        sql += ' on i.inst_id = account.inst_id'
        sql += ' left join inst_bank_pix pix'
        sql += ' on account.account_id = pix.account_id'

        return sql

    def get_instituicao_to_map(self, instituicao):

        accounts = []
        pixs = []

        for index, account in enumerate(instituicao['account_banks']):
            accounts.append({
                'bank_name': account,
                'account_ag': instituicao['account_ag'][index],
                'account_conta': instituicao['account_accounts'][index],
                'account_type': instituicao['account_types'][index]
            })

        for index, pix in enumerate(instituicao['pix_keys']):
            pix_key = instituicao['pix_keys'][index]
            qrcode = instituicao['qrcodes'][index]

            if not pix_key is None and not qrcode is None:
                pixs.append({
                    'pix_key': pix_key,
                    'qrcode_file': request.host_url + 'qrcode/' + qrcode
                })

        logo = instituicao['logo']

        if not logo:
            logo = None
        else:
            logo = request.host_url + 'imagens/' + logo

        return {
            'id': instituicao['inst_id'],
            'name': instituicao['inst_name'],
            'cnpj': instituicao['inst_cnpj'],
            'logo': logo,
            'alt_logo': instituicao['alt_logo'],
            'description': instituicao['description'],
            'categoria_id': instituicao['cat_id'],
            'categoria': {
                'id': instituicao['cat_id'],
                'nome': instituicao['cat_nome']
            },
            'contact': {
                'comercial': instituicao['contact_comercial'],
                'mobile': instituicao['contact_mobile'],
                'email': instituicao['contact_email'],
                'site': instituicao['contact_site'],
                'instagram': instituicao['contact_instagram'],
                'facebook': instituicao['contact_facebook'],
                'twitter': instituicao['contact_twitter'],
                'linkedin': instituicao['contact_linkedin'],
                'youtube': instituicao['contact_youtube']
            },
            'address': {
                'zipcode': instituicao['addr_zipcode'],
                'street': instituicao['addr_street'],
                'number': instituicao['addr_number'],
                'complement': instituicao['addr_complement'],
                'district': instituicao['addr_district'],
                'city': instituicao['addr_city'],
                'state': instituicao['addr_state'],
                'country': instituicao['addr_country']
            },
            'accounts': accounts,
            'pix': pixs
        }