from arca import app
from flask import jsonify
from flask_restful import Resource, Api, reqparse
from arca import models as md

api = Api(app)
api.init_app(app)

parser = reqparse.RequestParser()
parser.add_argument("query", location="args")


class Arca(Resource):
    def get(self):
        """ se chamada sem argumento, mostra a arca. Se chamada com argumentos,
        faz uma pesquisa"""
        args = parser.parse_args()
        query = args["query"]
        if query:
            response = md.search_display(query)
        else:
            response = md.Database.show_arca()
        return jsonify(response)

    def post(self, movie_id):
        movie = md.Movie.get_instance(movie_id)
        movie.arca_on()
        movie.update_db()
        return "True"

    def delete(self, movie_id):
        movie = md.Movie.get_instance(movie_id)
        movie.arca_off()
        movie.update_db()
        return "True"


api.add_resource(Arca, '/api/arca', '/api/search',
                 '/api/arca/<string:movie_id>')
