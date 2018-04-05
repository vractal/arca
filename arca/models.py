import requests
import json
from arca.api_key import db_pwd
import arca.mdbpy as mdb
from datetime import datetime
import time
from peewee import *
from playhouse.shortcuts import model_to_dict
import uuid


config = {
    "language": "pt-BR"
}


# To-do
# Classe com crud na database


db = SqliteDatabase('production.db')



class BaseModel(Model):
    class Meta:
        database = db



def create_instance(response):
    # resonse is a dict object containg info for one movie

        mv = Movie(
            title_br=response["title"], themoviedb_id=response["id"])
        for key in response:
            if key in mv.__dict__:
                setattr(mv, key, response[key])
        return mv





class Movie(BaseModel):
    """docstring for movie."""

    id_ = IntegerField(primary_key=True) #Use external movie database as id
    imdb_id = CharField(default="Not Fetched")  # Not implemented.
    title = CharField()
    overview = TextField()
    entry_language = CharField(default=config["language"])
    # translations
    release_date = DateTimeField()
    poster_path = CharField(default="1iDlfTz7x2AP9T3oms9b6Ji0I1R.jpg")
    times_saved = IntegerField(default=0)
    in_arca = BooleanField(default=False)


    def get_translated(self, language):
        if language == self.translations.language:
            pass



    @classmethod
    def get_instance(cls, themoviedb_id):
        " returns a node from database based on moviedatabase id"
        try:
            return Movie.get(id_=movie_id)
        except:
            return None

    def arca_up(self):
        if self.arca_entry:
            entry = self.arca_entry[0]
            entry.times += 1
            entry.save()
            self.arca_status()
        else:
            Arca.create(movie=self,times=1)

    def arca_down(self):
        if self.arca_entry[0]:
            entry = self.arca_entry[0]
            entry.times -= 1
            entry.save()
            self.arca_status()


    def arca_status(self,):
        try:
            entry = self.arca_entry[0]
            if entry.times > 0:
               if self.in_arca == False:
                    self.in_arca = True
                    self.update()
                    return True
            else:
                self.in_arca = False
                self.update()
                return False
        except:
            self.in_arca = False
            return False


class Movie_Translations(BaseModel):

    id_ = AutoField()
    movie_id = ForeignKeyField(Movie, backref="translations") # o que mais?
    language = CharField()
    title = CharField()
    overview = TextField()
    others = TextField()

class User(BaseModel):
    """Classe para registro de usuario."""

    id_ = AutoField(primary_key=True)
    login = CharField(unique=True)
    password = CharField()
    email = CharField(unique=True)
    movies_saved = ManyToManyField(Movie, backref="saved_by")



    @classmethod
    def register(cls,login,password,email):

        """ Returns True if created entry in DB, False if already existed"""

        try:
            register = cls.get_or_create(login=login,password=password,email=email)
            return register[1]
        except:
            return False


    def add_movie(self, id):
        """ Add movie in arc"""

        movie = Movie.get(id_=id)
        movie.arca_up()
        self.movies_saved.add(movie)

        #mudar datetime

    def del_movie(self, id):
        """ Add movie in arc"""
        movie = Movie.get(id_=id)
        movie.arca_down()
        self.movies_saved.remove(movie)

        # mudar datetime

    def get_list(self):
        """ Returns a list with all movies added by User"""

        list = []
        for movie in self.movies_saved:
            movie = model_to_dict(movie,backrefs=False)
            movie["release_date"] = str(movie['release_date'])[:4]
            list.append(movie)

        return list

    def log_in(self, password):
        if self.password == password:
            return True
        else:
            return False

    def avatar():

        return "avatars/avatar.png"



class Box(BaseModel):

    id_ = UUIDField(default=uuid.uuid4)
    name = CharField()
    user = ForeignKeyField(User,backref="box")

class Arca(BaseModel):

    """ arca entry in database"""

    movie = ForeignKeyField(Movie, backref="arca_entry")
    times = IntegerField()
    box = ManyToManyField(Box,backref="movies")
    status = CharField(default="not implemented")

    @classmethod
    def get_list(cls):
        list = []
        for movie in cls.select().where(cls.times > 0):
            movie = model_to_dict(movie,backrefs=False)["movie"]
            movie["release_date"] = str(movie['release_date'])[:4]
            list.append(movie)
        return list


class Database(object):

    @staticmethod
    def initdb():
        user_saved = User.movies_saved.get_through_model()
        db.create_tables([User,Movie,Movie_Translations,Arca,Box,
                      User.movies_saved.get_through_model(),
                        Arca.box.get_through_model()])

    @staticmethod
    def search_movie(query):
        list = []
        for movie in Movie.select().where(Movie.title.contains(query.lower())).dicts():
            movie['release_date'] = str(movie['release_date'])[:4]
            list.append(movie)
        return list

    @staticmethod
    def show_arca():
        return Arca.get_list()

    @staticmethod
    def show_all_movies():
        list = []
        for movie in Movie.select(Movie):
            movie = model_to_dict(movie,backrefs=False)
            movie["release_date"] = str(movie['release_date'])[:4]
            list.append(movie)
        return list

    @staticmethod
    def show_users():
        return User.select(User.login)
     #   return [entry["login"] for entry in User.select(User.login).dicts()]


def search_display(query, more=False):


    if more == True:
        results = mdb.search(query)["results"]
        for movie in results:
            try:
                Movie.get(id_=movie["id"])
            except:
                if not movie["poster_path"]:
                        movie["poster_path"] = "1iDlfTz7x2AP9T3oms9b6Ji0I1R.jpg"
                Movie.get_or_create(id_=movie['id'],
                                    title=movie['title'],
                                    overview=movie['overview'],
                                    poster_path=movie["poster_path"],
                                    release_date=movie['release_date'])
                mdb.get_poster(movie['poster_path'])



    elif more == False & len(Database.search_movie(query)) < 1:
        results = mdb.search(query)['results'][:5]
        for movie in results:
            if not movie["poster_path"]:
                movie["poster_path"] = "1iDlfTz7x2AP9T3oms9b6Ji0I1R.jpg"
            Movie.get_or_create(id_=movie['id'],
                                title=movie['title'],
                                overview=movie['overview'],
                                poster_path=movie["poster_path"],
                                release_date=movie['release_date'])
            mdb.get_poster(movie['poster_path'])


    return Database.search_movie(query)
