from arca import app
from flask import jsonify
from flask_restful import Resource, Api, reqparse
from arca import models as md

api = Api(app)
api.init_app(app)

parser = reqparse.RequestParser()
parser.add_argument("query", location="args")
parser.add_argument("user", location=["form","args"])

class Arca(Resource):
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
        return jsonify(response)

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
