from flask import Flask
from data_manager import DataManager
import os
from models import db, Movie
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/movies.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

data_manager = DataManager()

@app.route('/')
def home():
    return "Welcome to MoviWeb App!"

if __name__ == "__main__":
    app.run()