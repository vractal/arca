import requests
import json
from arca.api_key import api_key
from datetime import datetime
import time
import sys
import os
import uuid


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
    for movie in response['results']:
        movies.append((movie['title'],movie['id']))

    return response

def get_poster(obj):
    obj = obj #response object from fetch_one
    base_url = 'http://image.tmdb.org/t/p/'
    size =  "w500"
    poster = requests.get(base_url+ size+ str(obj['poster_path']))
    filename = "arca/static/posters/" + obj['poster_path']
    with open(filename, 'wb') as f:
            f.write(poster.content)

def get_poster2(name,path):
    path = path #response object from fetch_one
    base_url = 'http://image.tmdb.org/t/p/'
    size =  "w342"
    name = name
    poster = requests.get(base_url+ size+ str(path))
    filename = config['poster_folder_path'] + str(path)
    print(poster)
    with open(filename, 'wb') as f:
            f.write(poster.content)
    return str(name) + ".jpg"


def search_display(query):
    movies = []
    results = search(query)['results'][0:5]
    for result in results:
        poster_name = get_poster2(result['title'], result['poster_path'])
        movie = {}
        movie['title'] = result['title']
        movie['overview'] = result['overview']
        movie['tagline'] = "nenhuma"
        movie['posterimg'] = "posters/" + poster_name
        movies.append(movie)
    return movies
