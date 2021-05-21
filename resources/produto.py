from flask_restful import Resource, reqparse
from models.produto import ProdutoModel
from flask_jwt_extended import jwt_required


class Produtos(Resource):
    def get(self):
        return {'Produtos': [produto.json() for produto in ProdutoModel.query.all()]}

class Produto(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome', type =str, required=True, help="The field 'nome' cannot be left blank")
    argumentos.add_argument('categoria', type =str, required=True, help="The field 'categoria' cannot be left blank")
    argumentos.add_argument('preco', type =str, required=True, help="The field 'preco' cannot be left blank")
    argumentos.add_argument('status', type =str, required=True, help="The field 'status' cannot be left blank")

    def get(self, produtoId):
        produto = ProdutoModel.find_produto(produtoId)
        if produto:
            return produto.json()
        return {'message': 'Product not found.'}, 404 # Não foi encotrado


    @jwt_required
    def put(self, produtoId):
        dados = Produto.argumentos.parse_args()
        produto_encontrado = ProdutoModel.find_produto(produtoId)

        if produto_encontrado:
            produto_encontrado.update_produto(**dados)
            produto_encontrado.save_produto()
            return produto_encontrado.json(), 200 # Produto atualizado com sucesso
        return{'message': 'Product not found.'}, 404 # Não foi encotrado

    @jwt_required
    def delete(self, produtoId):
        produto = ProdutoModel.find_produto(produtoId)
        if produto:
            try:
                produto.delete_produto()
            except:
                return {'message': 'An internal error ocurred trying to delete Product.'}, 500 # Internal Server Error
            return {'message': 'Product deleted.'}
        return{'message': 'Product not found.'}, 404 # Erro


class ProdutoRegister(Resource):
    @jwt_required
    def post(self):
#        if ProdutoModel.find_produto(produtoId):
#            return {"message": "Produto Id '{}' already exists.".format(produtoId)}, 400 #Error

        dados = Produto.argumentos.parse_args()
        produto = ProdutoModel(**dados)
        try:
            produto.save_produto()
        except:
            return {'message': 'An internal error ocurred trying to save Product.'}, 500 # Internal Server Error
        return produto.json()
