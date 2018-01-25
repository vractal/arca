# -*- coding: utf-8 -*-
from flask import Flask, request, render_template, url_for,redirect, session
import requests
from api_key import api_key
import moviedb_api as mdb

SECRET_KEY = 'batata'
app = Flask(__name__)
app.config.from_object(__name__)


@app.route("/", methods=['GET','POST'])
def index():

    return render_template("boot.html")





""" procurar num filme, mostrar opcoes com miniaturas pequenas.
    botao para clicar, possibilitando adicionar a arca.
    (Salvar tudo na db como procurados, caso aconteça a procura de novo.futro)

    colocar bootstrap, fazer um negocinho bonitinho.
    (input, area embaixo onde vao aparecer os filmes)
    api para pesquisa, passando todos os dados dos filmes pro template."""


if __name__ == "__main__":
    app.run(debug=True)
