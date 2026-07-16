import os
import requests
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

API_KEY = os.getenv("TMDB_API_KEY")

BASE_URL = "https://api.themoviedb.org/3"
IMAGE_BASE = "https://image.tmdb.org/t/p/w500"


def fetch_movie_details(movie_id):
    """
    Fetch all movie details from TMDB.
    Returns None if request fails.
    """

    url = f"{BASE_URL}/movie/{movie_id}"

    params = {
        "api_key": API_KEY,
        "language": "en-US"
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        print(f"TMDB Error: {e}")
        return None


def fetch_movie_credits(movie_id):
    """
    Fetch cast and crew.
    """

    url = f"{BASE_URL}/movie/{movie_id}/credits"

    params = {
        "api_key": API_KEY
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        print(f"TMDB Credits Error: {e}")
        return None


def get_movie_metadata(movie_id):
    """
    Returns everything needed by Streamlit.
    Only TWO API calls.
    """

    details = fetch_movie_details(movie_id)

    if details is None:
        return None

    credits = fetch_movie_credits(movie_id)

    director = ""

    cast = []

    if credits:

        for person in credits["crew"]:

            if person["job"] == "Director":
                director = person["name"]
                break

        cast = [
            actor["name"]
            for actor in credits["cast"][:5]
        ]

    poster = ""

    if details.get("poster_path"):
        poster = IMAGE_BASE + details["poster_path"]

    metadata = {

        "title": details.get("title"),

        "poster": poster,

        "overview": details.get("overview"),

        "rating": round(details.get("vote_average", 0), 1),

        "genres": [
            g["name"]
            for g in details.get("genres", [])
        ],

        "runtime": details.get("runtime"),

        "release_date": details.get("release_date"),

        "director": director,

        "cast": cast

    }

    return metadata


if __name__ == "__main__":

    movie = get_movie_metadata(19995)

    print(movie)