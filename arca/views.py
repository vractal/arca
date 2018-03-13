# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify, render_template, url_for,redirect, session, flash
from arca import app
import requests
from arca.api_key import api_key
import arca.models as md


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        query = request.form['query']
        session['display'] = md.search_display(query)
        return redirect(url_for('index'))

    return render_template("index.html")


@app.route("/registrar", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
        email = request.form["email"]
        user = md.User(login, password, email)
        if not user.register():
            flash("Usuário já existe!")
        else:
            flash("Usuário criado com sucesso")
            return redirect(url_for("index"))

    return render_template("registrar.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        login = request.form["login"]
        password = request.form["password"]

        user = md.User.get_instance(login, password)
        if user:
            if user.log_in():
                session["user"] = user.login
                return redirect(url_for("index"))
        else:
            flash("Senha incorreta ou usuário não existe!")
    return render_template("login.html")


@app.route("/logout", methods=["GET"])
def logout():
    session.pop("user", None)
    session.pop("display", None)
    return redirect(url_for("index"))

#api endpoints

#Busca
@app.route("/api/search", methods=["GET"])
def api_search():
    query = request.args["query"]
    response = md.search_display(query)
    return jsonify(response)

#busca mais

#Editar info


#Adicionar
@app.route("/api/movie/add", methods=["GET"])
def api_add():
    movie_id = request.args["id"]
    movie = md.Movie.get_instance(movie_id)
    movie.arca_on()
    movie.update_db()
    return "True"


#Remover
@app.route("/api/movie/del", methods=["GET"])
def api_del():
    movie_id = request.args["id"]
    movie = md.Movie.get_instance(movie_id)
    movie.arca_off()
    movie.update_db()
    return "True"

@app.route("/api/arca", methods=["GET"])
def api_arca():
    response = md.Database.show_arca()
    return jsonify(response)



@app.route("/api-teste", methods=["GET"])
def testing():
    return render_template("api_test.html")
