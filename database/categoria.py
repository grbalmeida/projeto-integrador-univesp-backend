from database.repository import Repository

class Categoria(Repository):
    def __init__(self):
        super(Categoria, self).__init__('categorias')