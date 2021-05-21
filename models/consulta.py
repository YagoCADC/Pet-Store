from sql_alchemy import banco

class ConsultaModel(banco.Model):
    __tablename__ = 'consulta'

    consultaId = banco.Column(banco.Integer, primary_key=True)
    nome = banco.Column(banco.String(80))
    nomeDoPet = banco.Column(banco.String(80))
    categoria = banco.Column(banco.String(80))
    data= banco.Column(banco.String(80))
    hora= banco.Column(banco.String(80))



    def __init__(self, nome, nomeDoPet, categoria, data, hora):
        self.nome = nome
        self.nomeDoPet = nomeDoPet
        self.categoria = categoria
        self.data = data
        self.hora = hora

    def json(self):
        return {
            'consultaId': self.consultaId,
            'nome': self.nome,
            'nomeDoPet': self.nomeDoPet,
            'categoria': self.categoria,
            'data': self.data,
            'hora': self.hora
        }

    @classmethod
    def find_consulta(cls, consultaId):
        consulta = cls.query.filter_by(consultaId=consultaId).first()
        if consulta:
            return consulta
        return None

    def save_consulta(self):
        banco.session.add(self)
        banco.session.commit()

    def delete_consulta (self):
        banco.session.delete(self)
        banco.session.commit()
