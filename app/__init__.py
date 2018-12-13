from flask import Flask
from config import Config

app = Flask(__name__)  # in from app import app, this is the second app. First is the folder in which this file is stored
app.config.from_object(Config)

from app import routes