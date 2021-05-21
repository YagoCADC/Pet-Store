from flask_restful import Resource, reqparse
from models.user import UserModel
from flask_jwt_extended import create_access_token, jwt_required, get_raw_jwt
from werkzeug.security import safe_str_cmp
from blacklist import BLACKLIST


argumentos = reqparse.RequestParser()
argumentos.add_argument('login', type=str, required=True, help="The field 'login' cannot be left blank")
argumentos.add_argument('senha', type=str, required=True, help="The field 'senha' cannot be left blank")

class User(Resource):

    def get(self, userId):
        user = UserModel.find_user(userId)
        if user:
            return user.json()
        return {'message': 'User not found.'}, 404 # Não foi encotrado

    @jwt_required
    def delete(self, userId):
        user = UserModel.find_user(userId)
        if user:
            try:
                user.delete_user()
            except:
                return {'message': 'An internal error ocurred trying to delete User.'}, 500 # Internal Server Error
            return {'message': 'User deleted.'}, 200
        return{'message': 'User not found.'}, 404 # Erro


class UserRegister(Resource):
    def post(self):
        dados = argumentos.parse_args()

        if UserModel.find_by_login(dados['login']):
            return {"message": "The login '{}' already exists.".format(dados['login'])}, 401

        user = UserModel(**dados)
        user.save_user()
        return {'message': 'User created sucessfully!.'}, 200 #Created


class UserLogin(Resource):
    @classmethod
    def post(cls):
        dados = argumentos.parse_args()

        user = UserModel.find_by_login(dados['login'])

        if user and safe_str_cmp(user.senha, dados['senha']):
            token_de_acesso = create_access_token(identity=user.userId)
            return {'acess_token': token_de_acesso}, 200
        return {'message': 'The username or password is incorret!.'}, 401 #Unauthorize

class UserLogout(Resource):

    @jwt_required
    def post(self):
        jwtId = get_raw_jwt()['jti'] # JWT Token Identifier
        BLACKLIST.add(jwtId)
        return {'message': 'Logged out sucessfully!'}, 200
