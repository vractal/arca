from arca import app
from flask import jsonify, session, url_for
from flask_restful import Resource, Api, reqparse
from arca import models as md
from functools import wraps
import json
import os
import gzip

api = Api(app)
api.init_app(app)

parser = reqparse.RequestParser()
parser.add_argument("query", location="args")
parser.add_argument("user", location=["form","args"])
parser.add_argument("more",location=["args"])


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
        login = session["user"]
        user = md.User.get(login=login)
        user_list = []
        for mv in user.movies_saved:
            user_list.append(mv.title)

        for movie in response:
            if movie["title"] in user_list:
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
        more = args["more"]
        if query:
            if more:
                response = md.search_display(query,True)
            else:
                response = md.search_display(query)
        elif user:
            try:
                user = md.User.get(login=user)
                response = user.get_list()
            except:
                response = "no user"
        else:
            response = md.Database.show_all_movies()
        return response

    def post(self, movie_id):
        args = parser.parse_args()
        user = args["user"]
        user = md.User.get(login=user)
        user.add_movie(int(movie_id))
        return "True"

    def delete(self, movie_id):
        args = parser.parse_args()
        user = args["user"]
        user = md.User.get(login=user)
        user.del_movie(int(movie_id))
        return "True"


class UserApi(Resource):
    def get(self):
        return md.Database.show_users()



api.add_resource(Arca, '/api/arca', '/api/search',
                 '/api/arca/<string:movie_id>')

api.add_resource(UserApi,"/api/users")
