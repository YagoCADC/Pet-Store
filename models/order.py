from sql_alchemy import banco

class OrderModel(banco.Model):
    __tablename__ = 'order'

    orderId = banco.Column(banco.Integer, primary_key=True)
    quantidade = banco.Column(banco.Float(precision=1))
    preco= banco.Column(banco.Float(precision=2))
    status= banco.Column(banco.String(80))
    date= banco.Column(banco.String(80))


    def __init__(self, quantidade, preco, status, date):
        self.quantidade = quantidade
        self.preco = preco
        self.status = status
        self.date = date

    def json(self):
        return {
            'orderId': self.orderId,
            'quantidade': self.quantidade,
            'preco': self.preco,
            'status': self.status,
            'date': self.date
        }

    @classmethod
    def find_order(cls, orderId):
        order = cls.query.filter_by(orderId=orderId).first()
        if order:
            return order
        return None

    def save_order(self):
        banco.session.add(self)
        banco.session.commit()

    def update_order(self, quantidade, preco, status, date):
        self.quantidade = quantidade
        self.preco = preco
        self.status = status
        self.date = date

    def delete_order (self):
        banco.session.delete(self)
        banco.session.commit()
