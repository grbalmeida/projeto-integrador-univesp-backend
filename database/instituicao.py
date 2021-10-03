from database.repository import Repository

class Instituicao(Repository):
    def __init__(self):
        super(Instituicao, self).__init__('instituicoes', 'inst_id')

    def obter_instituicao(self, id):
        sql = self.get_base_instituicao_sql()
        sql += f' where i.inst_id = {id}'

        self.cur.execute(sql)
        instituicao = self.cur.fetchone()

        if instituicao is None:
            return {}
        else:
            return self.get_instituicao_to_map(instituicao)
    
    def obter_instituicoes(self, nome = None, categoria_id = None):
        instituicoes = []

        sql = self.get_base_instituicao_sql()
        sql += ' where 1 = 1'

        if not nome is None:
            sql += f" and i.inst_name like '%{nome}%'"

        if not categoria_id is None:
            sql += f" and i.cat_id = {categoria_id}"

        sql += ' order by i.inst_id'

        self.cur.execute(sql)
        result = self.cur.fetchall()

        for instituicao in result:
            instituicoes.append(self.get_instituicao_to_map(instituicao))

        return instituicoes

    def get_base_instituicao_sql(self):
        sql = 'select i.inst_id, i.inst_name, i.inst_cnpj,'
        sql += ' i.logo, i.description, c.cat_id, c.nome as cat_nome,'
        sql += ' contact.contact_comercial, contact.contact_mobile,'
        sql += ' contact.contact_email, contact.contact_site,'
        sql += ' contact.contact_instagram, contact.contact_facebook,'
        sql += ' contact.contact_twitter, contact.contact_linkedin,'
        sql += ' contact.contact_youtube,'
        sql += ' address.addr_zipcode, address.addr_street,'
        sql += ' address.addr_number, address.addr_complement,'
        sql += ' address.addr_district, address.addr_city,'
        sql += ' address.addr_state, address.addr_country'
        sql += ' from instituicoes i'
        sql += ' inner join categorias c'
        sql += ' on i.cat_id = c.cat_id'
        sql += ' left join inst_contacts contact'
        sql += ' on i.inst_id = contact.inst_id'
        sql += ' left join inst_addresses address'
        sql += ' on i.inst_id = address.inst_id'

        return sql

    def get_instituicao_to_map(self, instituicao):
        return {
            'id': instituicao['inst_id'],
            'name': instituicao['inst_name'],
            'cnpj': instituicao['inst_cnpj'],
            'logo': instituicao['logo'],
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
            }
        }