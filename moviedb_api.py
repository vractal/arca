import requests
import json
from api_key import api_key

class movie(object):
    """docstring formovie."""
    def __init__(self, id_):
        self.id_ = id_
        self.themoviedb_id = themoviedb_id
        self.imdb_id = imdb = imdb_id
        self.tagline = tagline
        self.original_title = original_title
        self.release_date = release_date
        self.poster_path = poster_path
        self.overview = overview



def fetch_one(id):
    base_one = "https://api.themoviedb.org/3/movie/"
    query = str(id)y
    params = {"api_key": api_key}
    response = requests.get(base_one+query,params=params ).json()
    return response

def search(scope="movie", query):
    #search for movie, tb, people, or all(multi)
    scope = scope
    base = "https://api.themoviedb.org/3/search/movie"
    movies = []
    query = query
    params = {"api_key": api_key, "page":"1","include_adult":"true", "query": query}
    response = requests.get(base,params=params ).json()
    response = json.dumps(response)
    for movie in response['results']:
        movies.append((movie['title'],get_poster2(movie['title'],movie['poster_path'])))

    return movies

def get_poster(obj):
    obj = obj #response object from fetch_one
    base_url = 'http://image.tmdb.org/t/p/'
    size =  "w500"
    poster = requests.get(base_url+ size+ str(obj['poster_path']))
    filename = "posters/" + obj['title'] + ".jpg"
    with open(filename, 'wb') as f:
            f.write(poster.content)

def get_poster2(name,path):
    path = path #response object from fetch_one
    base_url = 'http://image.tmdb.org/t/p/'
    size =  "w500"
    poster = requests.get(base_url+ size+ str(path))
    filename = "posters/" + str(name) + ".jpg"
    with open(filename, 'wb') as f:
            f.write(poster.content)
