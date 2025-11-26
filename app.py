import os
from dotenv import load_dotenv
import data_fetch
from flask import Flask, render_template, request, redirect, url_for, flash
from data_manager import DataManager
from models import db, User

app = Flask(__name__)

load_dotenv()
app.secret_key = os.getenv('SECRET_KEY')

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{basedir}/data/movies.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
data_manager = DataManager()


@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404


@app.errorhandler(403)
def forbidden(e):
    return render_template('errors/403.html'), 403


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('errors/500.html'), 500


@app.route('/')
def home():
    users = data_manager.get_users()
    return render_template('index.html', users=users)


@app.route('/users', methods=['POST'])
def add_user():
    name = request.form.get('name')
    if name and name.strip():
        if data_manager.create_user(name=name.strip()):
            flash('User added successfully!', 'success')
        else:
            flash('Failed to add user', 'error')
    else:
        flash('Username cannot be empty!', 'error')
    return redirect(url_for('home'))


@app.route('/users/<int:user_id>/movies', methods=['GET'])
def show_user_movies(user_id):
    user = User.query.get_or_404(user_id)
    movies = data_manager.get_movies(user_id)
    return render_template('user_movies.html', user=user, movies=movies)


@app.route('/users/<int:user_id>/movies', methods=['POST'])
def add_user_movie(user_id):
    movie_title = request.form.get('title')
    if not movie_title:
        flash('Movie title is required', 'error')
        return redirect(url_for('show_user_movies', user_id=user_id))

    movie_data = data_fetch.fetch_data(movie_title) if movie_title else None

    movie_obj = {
        'Title': movie_data['title'] if movie_data else movie_title,
        'Year': movie_data['year'] if movie_data else request.form.get('year', ''),
        'Director': movie_data.get('director', '') if movie_data else request.form.get('director', ''),
        'imdbID': movie_data.get('imdb_id', '') if movie_data else request.form.get('imdb_id', ''),
        'Poster': movie_data['poster_url'] if movie_data else request.form.get('poster_url', '')
    }

    if data_manager.add_movie(user_id, movie_obj):
        flash('Movie added successfully!', 'success')
    else:
        flash('Failed to add movie', 'error')

    return redirect(url_for('show_user_movies', user_id=user_id))


@app.route('/users/<int:user_id>/movies/<int:movie_id>/update', methods=['POST'])
def update_movie_title(user_id, movie_id):
    new_title = request.form.get('new_title')
    if new_title and new_title.strip():
        if data_manager.update_movie(movie_id, new_title.strip()):
            flash('Movie updated successfully!', 'success')
        else:
            flash('Failed to update movie', 'error')
    else:
        flash('New title cannot be empty', 'error')
    return redirect(url_for('show_user_movies', user_id=user_id))


@app.route('/users/<int:user_id>/movies/<int:movie_id>/delete', methods=['POST'])
def delete_movie(user_id, movie_id):
    if data_manager.delete_movie(movie_id):
        flash('Movie deleted successfully!', 'success')
    else:
        flash('Failed to delete movie', 'error')
    return redirect(url_for('show_user_movies', user_id=user_id))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)