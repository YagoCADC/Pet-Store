from flask_restful import Resource, reqparse
from models.order import OrderModel
from flask_jwt_extended import jwt_required


class Orders(Resource):
    def get(self):
        return {'Orders': [order.json() for order in OrderModel.query.all()]}

class Order(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('quantidade', required=True, help="The field 'nome' cannot be left blank")
    argumentos.add_argument('preco', required=True, help="The field 'categoria' cannot be left blank")
    argumentos.add_argument('status', required=True, help="The field 'status' cannot be left blank")
    argumentos.add_argument('date', required=True, help="The field 'date' cannot be left blank")

    def get(self, orderId):
        order = OrderModel.find_order(orderId)
        if order:
            return order.json()
        return {'message': 'Order not found.'}, 404 # Não foi encotrado


    @jwt_required
    def put(self, orderId):
        dados = Order.argumentos.parse_args()
        order_encontrado = OrderModel.find_order(orderId)

        if order_encontrado:
            order_encontrado.update_order(**dados)
            order_encontrado.save_order()
            return order_encontrado.json(), 200 # Order atualizado com sucesso
        return{'message': 'Order not found.'}, 404 # Não foi encotrado

    @jwt_required
    def delete(self, orderId):
        order = OrderModel.find_order(orderId)
        if order:
            try:
                order.delete_order()
            except:
                return {'message': 'An internal error ocurred trying to delete Order.'}, 500 # Internal Server Error
            return {'message': 'Order deleted.'}
        return{'message': 'Order not found.'}, 404 # Erro


class OrderRegister(Resource):
    @jwt_required
    def post(self):
#        if OrderModel.find_order(orderId):
#            return {"message": "Order Id '{}' already exists.".format(orderId)}, 400 #Error

        dados = Order.argumentos.parse_args()
        order = OrderModel(**dados)
        try:
            order.save_order()
        except:
            return {'message': 'An internal error ocurred trying to save Order.'}, 500 # Internal Server Error
        return order.json()
