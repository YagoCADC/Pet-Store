from flask import Flask, jsonify
from flask_restful import Api
from resources.pet  import Pets, Pet, PetRegister
from resources.produto  import Produtos, Produto, ProdutoRegister
from resources.order  import Orders, Order, OrderRegister
from resources.consulta  import Consulta, Consultas, ConsultaRegister
from resources.user  import User, UserRegister, UserLogin, UserLogout
from flask_jwt_extended import JWTManager
from blacklist import BLACKLIST

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'PAÇOCA'
app.config['JWT_BLACKLIST_ENABLED'] = True
api = Api(app)
jwt = JWTManager(app)

@app.before_first_request
def cria_banco():
    banco.create_all()

@jwt.token_in_blacklist_loader
def verifica_blacklist(token):
    return token['jti'] in BLACKLIST

@jwt.revoked_token_loader
def token_de_acesso_invalidado():
    return jsonify({'message': 'You have been logged out.'}), 401 #Unauthorized

#Pets
api.add_resource(Pets, '/pets')
api.add_resource(Pet, '/pets/<int:petId>')
api.add_resource(PetRegister, '/pet')

#Produto
api.add_resource(Produtos, '/store/inventory')
api.add_resource(Produto, '/store/produto/<int:produtoId>')
api.add_resource(ProdutoRegister, '/store/produto/cadastro')

#Order
api.add_resource(Orders, '/store/orders')
api.add_resource(Order, '/store/orders/<int:orderId>')
api.add_resource(OrderRegister, '/store/orders/cadastro')

#Consulta
api.add_resource(Consultas, '/consultas')
api.add_resource(Consulta, '/consulta/<int:consultaId>')
api.add_resource(ConsultaRegister, '/marcarConsulta')

#User
api.add_resource(User, '/user/<int:userId>')
api.add_resource(UserRegister, '/cadastro')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')

if __name__ == '__main__':
    from sql_alchemy import banco
    banco.init_app(app)
    app.run(debug=True)



# http://127.0.0.1:5000/pets
