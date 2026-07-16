import pandas as pd
import ast
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

movies = pd.read_csv(BASE_DIR / "data" / "tmdb_5000_movies.csv")
credits = pd.read_csv(BASE_DIR / "data" / "tmdb_5000_credits.csv")

# Merge datasets
movies = movies.merge(credits, on="title")

# Keep required columns
movies = movies[
    [
        "movie_id",
        "title",
        "overview",
        "genres",
        "keywords",
        "cast",
        "crew",
    ]
]

movies.dropna(inplace=True)


def extract_names(obj):
    obj = ast.literal_eval(obj)
    return [i["name"].replace(" ", "") for i in obj]


def extract_top_cast(obj):
    obj = ast.literal_eval(obj)
    return [i["name"].replace(" ", "") for i in obj[:5]]


def extract_director(obj):
    obj = ast.literal_eval(obj)
    directors = []
    for i in obj:
        if i["job"] == "Director":
            directors.append(i["name"].replace(" ", ""))
    return directors


movies["genres"] = movies["genres"].apply(extract_names)
movies["keywords"] = movies["keywords"].apply(extract_names)
movies["cast"] = movies["cast"].apply(extract_top_cast)
movies["crew"] = movies["crew"].apply(extract_director)

movies["overview"] = movies["overview"].apply(
    lambda x: x.lower().split()
)

# Create combined tags
movies["tags"] = (
    movies["overview"]
    + movies["genres"]
    + movies["keywords"]
    + movies["cast"]
    + movies["crew"]
)

movies["overview"] = movies["overview"].apply(lambda x: " ".join(x))
movies["tags"] = movies["tags"].apply(lambda x: " ".join(x))

movies.to_csv(
    BASE_DIR / "data" / "movie_tags.csv",
    index=False
)

print("movie_tags.csv created successfully!")
print(movies.head())