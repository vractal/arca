# -*- coding: utf-8 -*-
from flask import request,g, jsonify, render_template, url_for, redirect, session, flash
from arca import app
import requests
import arca.models as md

@app.before_request
def before_request():
    try:
        md.db.connect()
    except:
        md.db.close()
        md.db.connect()

@app.after_request
def after_request(response):
    md.db.close()
    return response


@app.route("/", methods=['GET', 'POST'])
def index():
    try:
        if session["user"]:
            return render_template("home.html")
    except:
        return render_template("login.html")


@app.route("/home", methods=['GET', 'POST'])
def home():
    try:
        if session["user"]:
            return render_template("home.html")
    except:
        return render_template("login.html")


@app.route("/registrar", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
        email = request.form["email"]
        if md.User.register(login, password, email) is False:
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

        try:
            user = md.User.get(login=login)

            if user.log_in(password):
                session["user"] = user.login
                return redirect(url_for("index"))
            else:
                flash("Senha incorreta!")

        except md.DoesNotExist:
            flash("Usuário não existe!")

    return render_template("login.html")


@app.route("/logout", methods=["GET"])
def logout():
    session.pop("user", None)
    session.pop("display", None)
    return redirect(url_for("index"))


@app.route("/pessoas", methods=["GET"])
def people():
    people = md.Database.show_users()
    return render_template("pessoas.html", people=people)


@app.route("/<string:login>", methods=["GET"])
def user_page(login):
    profile = login
    return render_template("user.html", profile=profile)


@app.route("/teste", methods=["GET"])
def testing():
    return render_template("api_test.html")


@app.route("/minhalista", methods=["GET"])
def my_list():
    return render_template("minhalista.html")


@app.route("/teste2", methods=["GET"])
def test():
    return render_template("teste2.html")


@app.route("/arca", methods=["GET"])
def arca_view():
    return render_template("arca.html")
