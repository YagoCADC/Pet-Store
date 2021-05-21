from sql_alchemy import banco

class ProdutoModel(banco.Model):
    __tablename__ = 'produto'

    produtoId = banco.Column(banco.Integer, primary_key=True)
    nome = banco.Column(banco.String(80))
    categoria = banco.Column(banco.String(80))
    preco= banco.Column(banco.Float(precision=2))
    status= banco.Column(banco.String(80))


    def __init__(self, nome, categoria, preco, status):
        self.nome = nome
        self.categoria = categoria
        self.preco = preco
        self.status = status

    def json(self):
        return {
            'produtoId': self.produtoId,
            'nome': self.nome,
            'categoria': self.categoria,
            'preco': self.preco,
            'status': self.status
        }

    @classmethod
    def find_produto(cls, produtoId):
        produto = cls.query.filter_by(produtoId=produtoId).first()
        if produto:
            return produto
        return None

    def save_produto(self):
        banco.session.add(self)
        banco.session.commit()

    def update_produto(self, nome, categoria, preco, status):
        self.nome = nome
        self.categoria = categoria
        self.preco = preco
        self.status = status

    def delete_produto (self):
        banco.session.delete(self)
        banco.session.commit()
