import os
from dotenv import load_dotenv
import requests


# Load environment variables from .env file
load_dotenv()


# Constants
API_KEY = os.getenv("API_KEY")

API_URL = f"http://www.omdbapi.com/?apikey={API_KEY}&t="
POSTER_URL = f"http://img.omdbapi.com/?apikey={API_KEY}&"


def fetch_data(movie_name):
    """
    Fetches the movie's data from OMDb API and returns only needed fields:
    "title" from data["Title"],
    "year"from data["Year"],
    "rating" from source "Internet Movie Database",
    "poster_url" from data["Poster"]
    """

    if not API_KEY:
        raise ValueError("API key not found. Please set OMDB_KEY in .env file")

    try:
        response = requests.get(f"{API_URL}{movie_name}", timeout=10)
        response.raise_for_status()
        data = response.json()

        if data.get("Response") == "False":
            return None

        filtered_data = {
            "title": data["Title"],
            "year": data["Year"],
            "rating": next(
                rating["Value"] for rating in data["Ratings"]
                if rating["Source"] == "Internet Movie Database"
            ),
            "poster_url": data["Poster"]
        }
        return filtered_data
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None