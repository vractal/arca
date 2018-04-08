import requests
import json
from arca.api_key import api_key



config = {
    "language": "pt-BR",
    "poster_folder_path": "arca/static/posters/"
}


def fetch_one(id):
    base_one = "https://api.themoviedb.org/3/movie/"
    query = str(id)
    params = {"api_key": api_key,"language":config["language"]}
    response = requests.get(base_one+query,params=params ).json()
    return response


def search(query, scope="movie"):
    #search for movie, tb, people, or all(multi)
    scope = scope
    base = "https://api.themoviedb.org/3/search/movie"
    movies = []
    query = query
    params = {"api_key": api_key, "language":config["language"],"page":"1","include_adult":"true", "query": query}
    response = requests.get(base,params=params ).json()
    return response


def get_poster(path):
    path = path #response object from fetch_one
    base_url = 'http://image.tmdb.org/t/p/'
    size =  "w342"

    poster = requests.get(base_url+ size+ str(path))
    filename = config['poster_folder_path'] + str(path)
    with open(filename, 'wb') as f:
            f.write(poster.content)
    return str(path)
