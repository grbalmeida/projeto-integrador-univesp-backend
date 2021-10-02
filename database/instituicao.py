from database.repository import Repository

class Instituicao(Repository):
    def __init__(self):
        super(Instituicao, self).__init__('instituicoes', 'inst_id')

    def obter_instituicoes(self):
        instituicoes = []

        sql = 'select i.inst_id, i.inst_name, i.inst_cnpj,'
        sql += ' i.logo, i.description, c.cat_id, c.nome as cat_nome'
        sql += ' from instituicoes i'
        sql += ' inner join categorias c'
        sql += ' on i.cat_id = c.cat_id'
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
                    }
                }
            )

        return instituicoes