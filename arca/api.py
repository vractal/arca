from arca import app
from flask import jsonify, session
from flask_restful import Resource, Api, reqparse
from arca import models as md
from functools import wraps
import json
api = Api(app)
api.init_app(app)

parser = reqparse.RequestParser()
parser.add_argument("query", location="args")
parser.add_argument("user", location=["form","args"])


# idealmente, um decorador?
#metodo para ppegar um resultado, comparar com a lista de um usuario, e retornar com a adição
#pega usuario
#pega lista do usuario
#muda o campo = in_arca de acordo.


#
def check_user_list(func):
    """ Decorator to change movie status in response acording to user list"""
    @wraps(func)
    def check_list(self,*args):
        response = func(self,*args)
        print(type(response))
        login = session["user"]
        user = md.User.get_instance_nopwd(login)
        user_list = user.get_list()

        for movie in response:
            if movie in user_list:
                movie["in_arca"] = True
            else:
                movie["in_arca"] = False
        return response

    return check_list


class Arca(Resource):

    @check_user_list
    def get(self):
        """ se chamada sem argumento, mostra a arca. Se chamada com argumentos,
        faz uma pesquisa"""
        args = parser.parse_args()
        user = args["user"]
        query = args["query"]
        if query:
            response = md.search_display(query)
        elif user:
            try:
                obj = md.User.get_instance_nopwd(user)
                response = obj.get_list()
            except:
                response =  "no user"
        else:
            response = md.Database.show_arca()
        return response

    def post(self, movie_id):
        args = parser.parse_args()
        user = args["user"]
        user = md.User.get_instance_nopwd(user)
        user.add_movie(movie_id)
        return "True"

    def delete(self, movie_id):
        args = parser.parse_args()
        user = args["user"]
        user = md.User.get_instance_nopwd(user)
        user.del_movie(movie_id)
        return "True"


class UserApi(Resource):
    def get(self):
        return md.Database.show_users()



api.add_resource(Arca, '/api/arca', '/api/search',
                 '/api/arca/<string:movie_id>')

api.add_resource(UserApi,"/api/users")
