import requests
import json
from api_key import api_key, db_pwd
import mdbpy as mdb
from datetime import datetime
import time
from py2neo import Graph, Node, Relationship, NodeSelector
import sys
import os
import uuid

graph = Graph(host="localhost",port="7687", user="neo4j", password=db_pwd)
selector = NodeSelector(graph)
def unique():
    graph.schema.create_uniqueness_constraint("Movie","themoviedb_id")
def drop_unique():
    graph.schema.drop_uniqueness_constraint("Movie","themoviedb_id")


# To-do
# Classe com crud na database

class User(object):
    """Classe para registro de usuario."""
    def __init__(self, login,password, email,id_ =None):
        self.login = login
        self.password = password
        self.email = email
        self.id_ = str(uuid.uuid4()) if id_ is None else id_

    def search_db(self):
        sel = selector.select("User",login=str(self.login))
        return sel.first()

    def register(self):
        if not self.search_db():
            user = Node("User", id_=self.id_,login=self.login,password=self.password,email=self.email)
            graph.create(user)
            return True
        else:
            return False

    @classmethod
    def get_instance(cls, login, password):
        sel = selector.select("User",login=str(login)).first()
        if sel:
            return User(login, password, sel["email"])
        else:
            return None


    def log_in(self):
        search = self.search_db()
        if search:
            if self.password == search['password']:
                return True
            else:
                return False







def create_instance(response):
    # resonse is a dict object containg info for one movie

    mv = Movie(original_title= response["original_title"],themoviedb_id=response["id"])
    for key in response:
        if key in mv.__dict__:
            setattr(mv, key, response[key])
    return mv


"""
class Tag(obiect):

    def __init__(self, title)
"""
class Movie(object):
    """docstring for movie."""
    def __init__(self, themoviedb_id,original_title, in_arca=False, overview = "None",  imdb_id="None", tagline="None",  release_date="None", poster_path ="None", vote_average="None"):
        #self.id_ = id_
        self.themoviedb_id = themoviedb_id
        self.imdb_id = imdb_id
        self.tagline = tagline
        self.original_title = original_title
        self.release_date = release_date
        self.poster_path = poster_path
        self.overview = overview
        self.vote_average = vote_average
        self.in_arca = in_arca


    @classmethod
    def find_db(cls, themoviedb_id):
        " returns a node from database based on moviedatabase id"
        movie = selector.select("Movie",themoviedb_id=themoviedb_id)
        movie = movie.first()
        if movie:
            return movie
        else:
            return None

    @classmethod
    def get_instance(cls, themoviedb_id):
        " returns a node from database based on moviedatabase id"
        response = Movie.find_db(themoviedb_id)
        mv = Movie(original_title= response["original_title"],themoviedb_id=response["id"])
        for key in response:
            if key in mv.__dict__:
                setattr(mv, key, response[key])
        return mv


    def fetch_db(self):
        """ Search for this movie instance in db, returns node """

        return Movie.find_db(self.themoviedb_id)

    def insert_db(self):
        if self.fetch_db():
            return self.fetch_db()
        else:
            movie_node = Node("Movie", in_arca= self.in_arca,themoviedb_id= self.themoviedb_id, original_title= self.original_title, original_title_lower=self.original_title.lower(), overview = self.overview,  imdb_id= self.imdb_id, tagline=self.tagline,  release_date= self.release_date, poster_path = self.poster_path,vote_average= self.vote_average)
            graph.create(movie_node)
            return True


    def update_db(self):
        #iterate through all propertys, and were diferent, change on database
        node = self.fetch_db()
        for key in self.__dict__:
            if self.__dict__[key] != node[key]:
                print(self.__dict__[key],node[key])
                node[key] = self.__dict__[key]
        node.push()

    def delete_db(self):
        """ Fetch node in db, returns true if deleted, false if fail """
        try:
            movie = self.fetch_db()
            graph.delete(movie)
            return True
        except:
            return False

    def arca_on(self):
        self.in_arca = True
        self.update_db()
    def arca_off(self):
        self.in_arca = False
        self.update_db()



class Database(object):



    @staticmethod
    def search_movie(query):
        movies = []
        ql = query.lower()
        for mv in selector.select("Movie").where("_.original_title_lower CONTAINS '%s'"%(ql) ):
            movie = {}
            movie['title'] = mv['original_title']
            movie['themoviedb_id'] = mv['themoviedb_id']
            movie["in_arca"] = mv['in_arca']
        #    movie['imdb_id'] = mv['imdb_id']
            movie['overview'] = mv['overview'] + "\n da db"
            movie['tagline'] = "nenhuma"
            if mv["poster_path"]:
                movie['posterimg'] = "posters/" + mv['poster_path']
                #movie['posterimg'] = "posters/Avatar.jpg"

            movies.append(movie)
        return movies

    @staticmethod
    def show_arca():
        movies = []
        for mv in selector.select("Movie",in_arca=True):
            movie = {}
            movie['title'] = mv['original_title']
            movie['themoviedb_id'] = mv['themoviedb_id']
            movie["in_arca"] = mv['in_arca']
        #    movie['imdb_id'] = mv['imdb_id']
            movie['overview'] = mv['overview'] + "\n da db"
            movie['tagline'] = "nenhuma"
            if mv["poster_path"]:
                movie['posterimg'] = "posters/" + mv['poster_path']
                #movie['posterimg'] = "posters/Avatar.jpg"

            movies.append(movie)
        return movies




def search_display(query):
    movies = []
    if len(Database.search_movie(query)) > 0:
        return Database.search_movie(query)

    else:
        results = mdb.search(query)['results'][0:5]
        for result in results:
            create_instance(result).insert_db()
            poster_name = mdb.get_poster2(result['title'], result['poster_path'])
            movie = {}
            movie['title'] = result['original_title']
            movie['themoviedb_id'] = result['id']
        #    movie['imdb_id'] = result['imdb_id']
            movie['overview'] = result['overview']
            movie['tagline'] = "nenhuma"
            if result["poster_path"]:
                movie['posterimg'] = "posters/" + result["poster_path"]
            movies.append(movie)
        return movies
