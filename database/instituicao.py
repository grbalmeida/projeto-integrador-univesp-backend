from database.repository import Repository

class Instituicao(Repository):
    def __init__(self):
        super(Instituicao, self).__init__('instituicoes', 'inst_id')

    def obter_instituicoes(self):
        instituicoes = []

        sql = 'select i.inst_id, i.inst_name, i.inst_cnpj,'
        sql += ' i.logo, i.description, c.cat_id, c.nome as cat_nome,'
        sql += ' contact.contact_comercial, contact.contact_mobile,'
        sql += ' contact.contact_email, contact.contact_site,'
        sql += ' contact.contact_instagram, contact.contact_facebook,'
        sql += ' contact.contact_twitter, contact.contact_linkedin,'
        sql += ' contact.contact_youtube'
        sql += ' from instituicoes i'
        sql += ' inner join categorias c'
        sql += ' on i.cat_id = c.cat_id'
        sql += ' left join inst_contacts contact'
        sql += ' on i.inst_id = contact.inst_id'
        sql += ' order by i.inst_id'

        self.cur.execute(sql)
        result = self.cur.fetchall()

        for instituicao in result:
            instituicoes.append(
                {
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
                    }
                }
            )

        return instituicoes