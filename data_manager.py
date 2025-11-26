
from sqlalchemy.exc import SQLAlchemyError
from models import db, Movie, User


class DataManager():
    def create_user(self, name):
        """Add a new user to the database"""
        if not name or not name.strip():
            return None

        try:
            user = User(name=name.strip())
            db.session.add(user)
            db.session.commit()
            return user
        except SQLAlchemyError:
            db.session.rollback()
            return None


    def get_users(self):
        """Return a list of all users in the database"""
        return User.query.all()


    def get_movies(self, user_id):
        """Return a list of all movies for a specific user"""
        return Movie.query.filter_by(user_id=user_id).all()


    def add_movie(self, user_id, movie_data):
        """Add a new movie for a user"""
        if not movie_data or not movie_data.get('Title'):
            return None

        try:
            movie = Movie(
                name=movie_data.get('Title', ''),
                year=movie_data.get('Year', ''),
                director=movie_data.get('Director', ''),
                poster_url=movie_data.get('Poster', ''),
                imdb_id=movie_data.get('imdbID', ''),
                user_id=user_id
            )
            db.session.add(movie)
            db.session.commit()
            return movie
        except SQLAlchemyError:
            db.session.rollback()
            return None


    def update_movie(self, movie_id, new_name):
        """Update the name of a specific movie"""
        try:
            movie = Movie.query.get(movie_id)
            if movie:
                movie.name = new_name
                db.session.commit()
                return True
            return False
        except SQLAlchemyError:
            db.session.rollback()
            return False


    def delete_movie(self, movie_id):
        """Delete a movie"""
        try:
            movie = Movie.query.get(movie_id)
            if not movie:
                return False

            db.session.delete(movie)
            db.session.commit()
            return True
        except SQLAlchemyError:
            db.session.rollback()
            return False