# -*- coding: utf-8 -*-
from flask import request, jsonify, render_template, url_for, redirect, session, flash
from arca import app
import requests
import arca.models as md


@app.route("/", methods=['GET', 'POST'])
def index():
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
        else:
            flash("Senha incorreta ou usuário não existe!")
    return render_template("login.html")


@app.route("/logout", methods=["GET"])
def logout():
    session.pop("user", None)
    session.pop("display", None)
    return redirect(url_for("index"))


@app.route("/teste", methods=["GET"])
def testing():
    return render_template("api_test.html")

@app.route("/teste2", methods=["GET"])
def test():
    return render_template("teste2.html")

@app.route("/arca", methods=["GET"])
def arca_view():
    return render_template("arca.html")