import data_fetch
from flask import Flask, render_template, request, redirect, url_for, flash
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
    users = data_manager.get_users()
    return render_template('index.html', users=users)


@app.route('/users', methods=['POST'])
def add_user():
    name = request.form.get('name')
    if name and len(name.strip()) > 0:
        data_manager.create_user(name=name.strip())
    return redirect(url_for('home'))


@app.route('/users/<int:user_id>/movies', methods=['GET'])
def show_user_movies(user_id):
    user = data_manager.get_user(user_id)
    movies = data_manager.get_movies(user_id)
    return render_template('movies.html', user=user, movies=movies)


@app.route('/users/<int:user_id>/movies', methods=['POST'])
def add_user_movie(user_id):
    movie_data = {
        'Title': request.form.get('title'),
        'Director': request.form.get('director'),
        'Year': request.form.get('year'),
        'imdbID': request.form.get('imdb_id'),
        'Poster': request.form.get('poster_url')
    }

    data_manager.add_movie(user_id, movie_data)
    return redirect(url_for('show_user_movies', user_id=user_id))


@app.route('/users/<int:user_id>/movies/<int:movie_id>/update', methods=['POST'])
def update_movie_title(user_id, movie_id):
    new_title = request.form.get('new_title')

    if new_title and new_title.strip():
        success = data_manager.update_movie(movie_id, new_title.strip())

        if not success:
            flash('Movie not found', 'error')

    return redirect(url_for('show_user_movies', user_id=user_id))


@app.route('/users/<int:user_id>/movies/<int:movie_id>/delete', methods=['POST'])
def delete_movie(user_id, movie_id):
    success = data_manager.delete_movie(movie_id)

    if not success:
        flash('Movie not found', 'error')

    return redirect(url_for('show_user_movies', user_id=user_id))




if __name__ == '__main__':
  with app.app_context():
    db.create_all()

  app.run()