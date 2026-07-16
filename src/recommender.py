import pickle
import pandas as pd
import ast
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Load trained files
movies = pickle.load(open(BASE_DIR / "models" / "movies.pkl", "rb"))
similarity = pickle.load(open(BASE_DIR / "models" / "similarity.pkl", "rb"))

# Convert string representations back to lists
for col in ["genres", "keywords", "cast", "crew"]:
    movies[col] = movies[col].apply(ast.literal_eval)


def explain_recommendation(source_movie, recommended_movie):
    """
    Explain why a movie was recommended.
    """

    source = movies[
        movies["title"].str.lower() == source_movie.lower()
    ].iloc[0]

    reasons = []

    # Common genres
    common_genres = set(source["genres"]).intersection(
        set(recommended_movie["genres"])
    )

    if common_genres:
        reasons.append(
            "Similar genres: " +
            ", ".join(sorted(common_genres)[:3])
        )

    # Common keywords
    common_keywords = set(source["keywords"]).intersection(
        set(recommended_movie["keywords"])
    )

    if common_keywords:
        reasons.append(
            "Shared themes: " +
            ", ".join(sorted(common_keywords)[:3])
        )

    # Same director
    if len(set(source["crew"]).intersection(set(recommended_movie["director"]))) > 0:
        reasons.append("Same Director")

    if not reasons:
        reasons.append("High overall content similarity")

    return reasons


def recommend(movie_name, top_n=10):
    """
    Returns top_n similar movies.
    """

    movie_index = movies[
        movies["title"].str.lower() == movie_name.lower()
    ].index

    if len(movie_index) == 0:
        return []

    movie_index = movie_index[0]

    similarity_scores = similarity[movie_index]

    movie_list = sorted(
        enumerate(similarity_scores),
        key=lambda x: x[1],
        reverse=True
    )[1:top_n + 1]

    recommendations = []

    for idx, score in movie_list:

        movie = movies.iloc[idx]

        movie_dict = {
            "movie_id": int(movie["movie_id"]),
            "title": movie["title"],
            "genres": movie["genres"],
            "keywords": movie["keywords"],
            "cast": movie["cast"],
            "director": movie["crew"],
            "similarity": round(float(score) * 100, 2)
        }

        # Add explanation
        movie_dict["reason"] = explain_recommendation(
            movie_name,
            movie_dict
        )

        recommendations.append(movie_dict)

    return recommendations


if __name__ == "__main__":

    recommendations = recommend("Avatar")

    for movie in recommendations:

        print("=" * 60)

        print(movie["title"])

        print(f"Similarity : {movie['similarity']}%")

        print(f"Genres     : {', '.join(movie['genres'])}")

        print(f"Director   : {', '.join(movie['director'])}")

        print(f"Cast       : {', '.join(movie['cast'][:3])}")

        print("Why Recommended?")

        for reason in movie["reason"]:
            print(f"• {reason}")

        print()