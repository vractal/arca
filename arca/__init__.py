from flask import Flask
from flask_compress import Compress

app = Flask(__name__)
app.config.from_object("config")

Compress(app)
from arca import views
from arca import api
