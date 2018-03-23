import requests
import json
from arca.api_key import db_pwd
import arca.mdbpy as mdb
from datetime import datetime
import time
from py2neo import Graph, Node, Relationship, NodeSelector
import uuid

graph = Graph(host="localhost", port="7687", user="neo4j", password=db_pwd)
selector = NodeSelector(graph)


def unique_movie():
    graph.schema.create_uniqueness_constraint("Movie", "themoviedb_id")


def unique_user():
    graph.schema.create_uniqueness_constraint("User", "login")
    print("foi")


def drop_unique_movie():
    graph.schema.drop_uniqueness_constraint("Movie", "themoviedb_id")


# To-do
# Classe com crud na database

class User(object):
    """Classe para registro de usuario."""

    def __init__(self, login, password, email, id_=None):
        self.login = login
        self.password = password
        self.email = email
        self.id_ = str(uuid.uuid4()) if id_ is None else id_

    def fetch_db(self):
        sel = selector.select("User", login=str(self.login))
        return sel.first()

    def register(self):
        if not self.fetch_db():
            user = Node("User", id_=self.id_, login=self.login,
                        password=self.password, email=self.email)
            graph.create(user)
            return True
        else:
            return False

    @classmethod
    def get_instance(cls, login, password):
        sel = selector.select("User", login=str(login)).first()
        if sel:
            return User(login, password, sel["email"])
        else:
            return None

    @classmethod
    def get_instance_nopwd(cls, login):
        sel = selector.select("User", login=str(login)).first()
        if sel:
            return User(login, sel["password"], sel["email"])
        else:
            return None

    def add_movie(self, id):
        """ Add movie in arc"""
        movie = Movie.get_instance(id)
        #criar relação user-[salvou]->movie
        node = movie.fetch_db()
        user_node = self.fetch_db()
        if not graph.match_one(start_node=user_node,end_node=node,rel_type='SALVOU'):
            rel = Relationship(user_node, "SALVOU", node, data=str(datetime.now()))
            graph.create(rel)
            movie.arca_on()
            arca = Database.fetch_arca()
            rel2 = graph.match_one(start_node=node,end_node=arca,rel_type='SAVED_IN')
            if rel2:
                rel2["times"]+= 1
                graph.push(rel2)
            else:
                rel2 = Relationship(node, "SAVED_IN", arca, times=1, data=str(datetime.now()))
                graph.create(rel2)


        #mudar datetime

    def del_movie(self, id):
        """ Add movie in arc"""
        movie = Movie.get_instance(id)
        #criar relação user-[salvou]->movie
        node = movie.fetch_db()
        user_node = self.fetch_db()
        rel = graph.match_one(start_node=user_node,end_node=node,rel_type="SALVOU")
        if rel:
            arca = Database.fetch_arca()
            rel2 = graph.match_one(start_node=node,end_node=arca,rel_type='SAVED_IN')
            rel2["times"] -= 1
            if rel2["times"] < 1:
                graph.separate(rel2)
                movie.arca_off()
            else:
                graph.push(rel2)
            rel2 = graph.match_one(start_node=node,end_node=arca,rel_type="IS_IN")
            graph.separate(rel)

        #mudar datetime

    def get_list(self):
        """ Returns a list with all movies added by User"""
        lista = []
        user_node = self.fetch_db()
        sel = graph.match(start_node=user_node, rel_type="SALVOU")
        for rel in sel:
            mv = rel.end_node()
            movie = {}
            movie['title'] = mv['title_br']
            movie['themoviedb_id'] = mv['themoviedb_id']
            movie["in_arca"] = mv['in_arca']
            movie["release_date"] = mv["release_date"][0:4]
        #    movie['imdb_id'] = mv['imdb_id']
            movie['overview'] = mv['overview']
            movie['tagline'] = "nenhuma"
            if mv["poster_path"]:
                movie['posterimg'] = "posters/" + mv['poster_path']
            lista.append(movie)
        return lista

    def log_in(self):
        search = self.fetch_db()
        if search:
            if self.password == search['password']:
                return True
            else:
                return False

    def avatar():

        return "avatars/avatar.png"

def create_instance(response):
    # resonse is a dict object containg info for one movie

    mv = Movie(
        title_br=response["title"], themoviedb_id=response["id"])
    for key in response:
        if key in mv.__dict__:
            setattr(mv, key, response[key])
    return mv


class Movie(object):
    """docstring for movie."""

    def __init__(self, themoviedb_id,title_br, original_title="none", saved=0, in_arca=False,
                 overview="None", imdb_id="None", release_date="None",
                 poster_path="None",):

        self.themoviedb_id = themoviedb_id
        self.imdb_id = imdb_id
        self.title_br = title_br
        self.original_title = original_title
        self.release_date = release_date
        self.poster_path = poster_path
        self.overview = overview
        self.saved = saved
        self.in_arca = in_arca

    @classmethod
    def find_db(cls, themoviedb_id):
        " returns a node from database based on moviedatabase id"
        movie = selector.select("Movie", themoviedb_id=int(themoviedb_id))
        movie = movie.first()
        if movie:
            return movie
        else:
            return None

    @classmethod
    def get_instance(cls, themoviedb_id):
        " returns a node from database based on moviedatabase id"
        response = Movie.find_db(themoviedb_id)
        mv = Movie(title_br=response["title_br"],
                   themoviedb_id=response["id"])
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
            movie_node = Node(
                "Movie", in_arca=self.in_arca, themoviedb_id=self.themoviedb_id,
                title_br=self.title_br, title_br_lower=self.title_br.lower(),
                original_title=self.original_title, original_title_lower=self.original_title.lower(),
                overview=self.overview, imdb_id=self.imdb_id, release_date=self.release_date,
                poster_path=self.poster_path)
            graph.create(movie_node)
            return True

    def update_db(self):
        # iterate through all propertys, and were diferent, change on database
        node = self.fetch_db()
        for key in self.__dict__:
            if self.__dict__[key] != node[key]:
                print(self.__dict__[key], node[key])
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

    def in_arc(self):
        """ method to say if a movie is in the ark"""
        mv = self.fetch_db()
        sel = graph.match(start_node=mv, rel_type="IS_IN")




class Database(object):

    @staticmethod
    def create_arca():
        if not Database.fetch_arca():
            arca = Node("Arca")
            graph.create(arca)

    @staticmethod
    def fetch_arca():
        return selector.select("Arca").first()
    @staticmethod
    def search_movie(query):
        movies = []
        ql = query.lower()
        for mv in selector.select("Movie").where("_.title_br_lower CONTAINS '%s'" % (ql)):
            movie = {}
            movie['original_title'] = mv['original_title']
            movie["title"] = mv["title_br"]
            movie['themoviedb_id'] = mv['themoviedb_id']
            movie["in_arca"] = mv['in_arca']
            movie["release_date"] = mv["release_date"][0:4]
        #    movie['imdb_id'] = mv['imdb_id']
            movie['overview'] = mv['overview']
            movie['tagline'] = "nenhuma"
            if mv["poster_path"]:
                movie['posterimg'] = "posters/" + mv['poster_path']
                #movie['posterimg'] = "posters/Avatar.jpg"

            movies.append(movie)
        return movies

    @staticmethod
    def show_arca():
        movies = []
        for mv in selector.select("Movie", in_arca=True):
            movie = {}
            movie['title'] = mv['title_br']
            movie['themoviedb_id'] = mv['themoviedb_id']
            movie["in_arca"] = mv['in_arca']
            movie["release_date"] = mv["release_date"][0:4]
        #    movie['imdb_id'] = mv['imdb_id']
            movie['overview'] = mv['overview']
            movie['tagline'] = "nenhuma"
            if mv["poster_path"]:
                movie['posterimg'] = "posters/" + mv['poster_path']
                #movie['posterimg'] = "posters/Avatar.jpg"

            movies.append(movie)
        return movies
    @staticmethod
    def show_users():
        users = []
        sel = selector.select("User")
        for us in sel:
            user = {}
            user["login"] = us["login"]
            users.append(user)
        return users


def search_display(query):
    movies = []
    if len(Database.search_movie(query)) < 1:
        results = mdb.search(query)['results'][0:5]
        for result in results:
            create_instance(result).insert_db()
            mdb.get_poster2(
                result['title'], result['poster_path'])

    return Database.search_movie(query)
