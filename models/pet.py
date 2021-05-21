from sql_alchemy import banco

class PetModel(banco.Model):
    __tablename__ = 'pets'

    petId = banco.Column(banco.Integer, primary_key=True)
    nome = banco.Column(banco.String(80))
    categoria = banco.Column(banco.String(80))
    sexo= banco.Column(banco.String(80))
    raça= banco.Column(banco.String(80))


    def __init__(self, nome, categoria, sexo, raça):
        self.nome = nome
        self.categoria = categoria
        self.sexo = sexo
        self.raça = raça

    def json(self):
        return {
            'petId': self.petId,
            'nome': self.nome,
            'categoria': self.categoria,
            'sexo': self.sexo,
            'raça': self.raça
        }

    @classmethod
    def find_pet(cls, petId):
        pet = cls.query.filter_by(petId=petId).first()
        if pet:
            return pet
        return None

    def save_pet(self):
        banco.session.add(self)
        banco.session.commit()

    def update_pet(self, nome, categoria, sexo, raça):
        self.nome = nome
        self.categoria = categoria
        self.sexo = sexo
        self.raça = raça

    def delete_pet (self):
        banco.session.delete(self)
        banco.session.commit()
