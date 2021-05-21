from flask_restful import Resource, reqparse
from models.consulta import ConsultaModel
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import jwt_required


argumentos = reqparse.RequestParser()
argumentos.add_argument('nome', type=str, required=True, help="The field 'login' cannot be left blank")
argumentos.add_argument('nomeDoPet', type=str, required=True, help="The field 'senha' cannot be left blank")
argumentos.add_argument('categoria', type=str, required=True, help="The field 'login' cannot be left blank")
argumentos.add_argument('data', type=str, required=True, help="The field 'senha' cannot be left blank")
argumentos.add_argument('hora', type=str, required=True, help="The field 'login' cannot be left blank")


class Consultas(Resource):
    @jwt_required
    def get(self):
        return {'Consultas': [consulta.json() for consulta in ConsultaModel.query.all()]}

class Consulta(Resource):
    @jwt_required
    def get(self, consultaId):
        consulta = ConsultaModel.find_consulta(consultaId)
        if consulta:
            return consulta.json()
        return {'message': 'Appointment not found.'}, 404 # Não foi encotrado

    @jwt_required
    def delete(self, consultaId):
        consulta = ConsultaModel.find_consulta(consultaId)
        if consulta:
            try:
                consulta.delete_consulta()
            except:
                return {'message': 'An internal error ocurred trying to delete Appointment.'}, 500 # Internal Server Error
            return {'message': 'Appointment deleted.'}
        return{'message': 'Appointment not found.'}, 404 # Erro


class ConsultaRegister(Resource):
    def post(self):
        dados = argumentos.parse_args()

        #if ConsultaModel.find_consulta(consultaId):
        #    return {"message": "The Appointment '{}' already exists.".format(consultaId)}, 400 #Error

        user = ConsultaModel(**dados)
        user.save_consulta()
        return {'message': 'Appointment created sucessfully!.'}, 201 #Created
