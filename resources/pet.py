from flask_restful import Resource, reqparse
from models.pet import PetModel
from flask_jwt_extended import jwt_required


class Pets(Resource):
    def get(self):
        return {'pets': [pet.json() for pet in PetModel.query.all()]}, 200 # Pet encontrado com sucesso

class Pet(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome', type =str, required=True, help="The field 'nome' cannot be left blank")
    argumentos.add_argument('categoria', type =str, required=True, help="The field 'categoria' cannot be left blank")
    argumentos.add_argument('sexo', type =str, required=True, help="The field 'sexo' cannot be left blank")
    argumentos.add_argument('raça', type =str, required=True, help="The field 'raça' cannot be left blank")

    def get(self, petId):
        pet = PetModel.find_pet(petId)
        if pet:
            return pet.json(), 200 # Pet encontrado com sucesso
        return {'message': 'Pet não encontrado.'}, 404 # Não foi encotrado


    #@jwt_required
    def put(self, petId):
        dados = Pet.argumentos.parse_args()
        pet_encontrado = PetModel.find_pet(petId)

        if pet_encontrado:
            pet_encontrado.update_pet(**dados)
            pet_encontrado.save_pet()
            return pet_encontrado.json(), 200 # Pet atualizado com sucesso
        return{'message': 'Pet not found.'}, 404 # Não foi encotrado

    @jwt_required
    def delete(self, petId):
        pet = PetModel.find_pet(petId)
        if pet:
            try:
                pet.delete_pet()
            except:
                return {'message': 'An internal error ocurred trying to delete Pet.'}, 500 # Internal Server Error
            return {'message': 'Pet deleted.'}, 200 # Sucesso
        return{'message': 'Pet not found.'}, 404 # Erro


class PetRegister(Resource):
    @jwt_required
    def post(self):
#        if PetModel.find_pet(petId):
#            return {"message": "Pet Id '{}' already exists.".format(petId)}, 400 #Error

        dados = Pet.argumentos.parse_args()
        pet = PetModel(**dados)
        try:
            pet.save_pet()
        except:
            return {'message': 'An internal error ocurred trying to save Pet.'}, 500 # Internal Server Error
        return pet.json(), 200 # Sucesso
