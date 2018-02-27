# -*- coding: utf-8 -*-
from flask import Flask, request, render_template, url_for,redirect, session, flash
import requests
from api_key import api_key
import mdbpy as mdb
import models as md

SECRET_KEY = 'batata'
app = Flask(__name__)
app.config.from_object(__name__)


@app.route("/", methods=['GET','POST'])
def index():
    if request.method == "POST":
        query = request.form['query']
        session['display'] = md.search_display(query)
        return redirect(url_for('index'))

    return render_template("index.html")




@app.route("/registrar",methods=['GET', 'POST'])
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

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        login = request.form["login"]
        password = request.form["password"]

        user = md.User.get_instance(login,password)
        if user:
            if user.log_in():
                session["user"] = user.login
                return redirect(url_for("index"))
        else:
            flash("Senha incorreta ou usuário não existe!")
    return render_template("login.html")

@app.route("/logout", methods=["GET"])
def logout():
    session.pop("user",None)
    session.pop("display", None)
    return redirect(url_for("index"))











@app.route("/arca", methods=["GET"])
def arca():
    session['display'] = md.Database.show_arca()
    return redirect(url_for('index'))


@app.route("/clean", methods=["GET"])
def clean():
    session['display'] = []
    return redirect(url_for('index'))


@app.route("/id/<id>/add", methods=["GET"])
def movie_add(id):
    movie = md.Movie.get_instance(int(id))
    movie.arca_on()
    return redirect(url_for('index'))

""" procurar num filme, mostrar opcoes com miniaturas pequenas.
    botao para clicar, possibilitando adicionar a arca.
    (Salvar tudo na db como procurados, caso aconteça a procura de novo.futro)

    colocar bootstrap, fazer um negocinho bonitinho.
    (input, area embaixo onde vao aparecer os filmes)
    api para pesquisa, passando todos os dados dos filmes pro template."""


if __name__ == "__main__":
    app.run(debug=True)
