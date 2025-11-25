from models import db, User, Movie

class DataManager():

    def create_user(self, name):
        """Add a new user to the database"""
        new_user = User(name=name)
        db.session.add(new_user)
        db.session.commit()
        return new_user

    def get_users(self):
        """Return a list of all users in the database"""
        return User.query.all()

    def get_movies(self, user_id):
        """Return a list of all movies for a specific user"""
        return Movie.query.filter_by(user_id=user_id).all()

    def add_movie(self, user_id, movie_data):
        """
        Add a new movie to a user's favorites.
        movie_data can be either:
        - a dictionary with movie details (if fetching from OMDB first)
        - or a Movie object (if creating in app.py first)
        """
        if isinstance(movie_data, Movie):
            # If it's already a Movie object, just add it
            movie_data.user_id = user_id
            db.session.add(movie_data)
        else:
            # If it's a dictionary, create a new Movie object
            new_movie = Movie(
                title=movie_data.get('Title'),
                year=movie_data.get('Year'),
                imdb_id=movie_data.get('imdbID'),
                poster_url=movie_data.get('Poster'),
                user_id=user_id
            )
            db.session.add(new_movie)

        db.session.commit()

    def update_movie(self, movie_id, new_title):
        """Update the title of a specific movie"""
        movie = Movie.query.get(movie_id)
        if movie:
            movie.title = new_title
            db.session.commit()
            return True
        return False

    def delete_movie(self, movie_id):
        """Delete a movie from the database"""
        movie = Movie.query.get(movie_id)
        if movie:
            db.session.delete(movie)
            db.session.commit()
            return True
        return False