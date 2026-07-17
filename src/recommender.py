import ast
import pickle
from pathlib import Path
from typing import List, Dict

# ==========================================================
# Paths
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

# ==========================================================
# Load Models
# ==========================================================

with open(BASE_DIR / "models" / "movies.pkl", "rb") as f:
    movies = pickle.load(f)

with open(BASE_DIR / "models" / "similarity.pkl", "rb") as f:
    similarity = pickle.load(f)

# ==========================================================
# Convert String Columns to Lists
# ==========================================================

LIST_COLUMNS = ["genres", "keywords", "cast", "crew"]

for col in LIST_COLUMNS:
    movies[col] = movies[col].apply(
        lambda x: ast.literal_eval(x) if isinstance(x, str) else x
    )

# ==========================================================
# Match Label
# ==========================================================

def get_match_label(score: float) -> str:
    """
    Convert cosine similarity into a user-friendly label.
    """

    percentage = score * 100

    if percentage >= 35:
        return "⭐⭐ Excellent Match"

    elif percentage >= 25:
        return "⭐ Very Good Match"

    elif percentage >= 18:
        return "👍 Good Match"

    elif percentage >= 10:
        return "🎬 Worth Watching"

    return "🔍 Explore"

# ==========================================================
# Recommendation Explanation
# ==========================================================

def explain_recommendation(
    source_movie: str,
    recommended_movie: Dict
) -> List[str]:

    source = movies[
        movies["title"].str.lower() == source_movie.lower()
    ].iloc[0]

    reasons = []

    # ------------------------------------------------------

    common_genres = list(
        set(source["genres"]).intersection(
            set(recommended_movie["genres"])
        )
    )

    if common_genres:
        reasons.append("✓ Similar Genres")

    # ------------------------------------------------------

    common_keywords = list(
        set(source["keywords"]).intersection(
            set(recommended_movie["keywords"])
        )
    )

    if common_keywords:
        reasons.append("✓ Shared Themes")

    # ------------------------------------------------------

    common_cast = list(
        set(source["cast"]).intersection(
            set(recommended_movie["cast"])
        )
    )

    if common_cast:
        reasons.append("✓ Common Cast")

    # ------------------------------------------------------

    common_director = list(
        set(source["crew"]).intersection(
            set(recommended_movie["director"])
        )
    )

    if common_director:
        reasons.append("✓ Same Director")

    # ------------------------------------------------------

    if not reasons:
        reasons.append("✓ High Content Similarity")

    return reasons

# ==========================================================
# Recommendation Engine
# ==========================================================

def recommend(
    movie_name: str,
    top_n: int = 10
) -> List[Dict]:

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
    )[1: top_n + 1]

    recommendations = []

    for idx, score in movie_list:

        movie = movies.iloc[idx]

        recommendation = {

            "movie_id": int(movie["movie_id"]),

            "title": movie["title"],

            "genres": movie["genres"],

            "keywords": movie["keywords"],

            "cast": movie["cast"],

            "director": movie["crew"],

            "similarity_raw": float(score),

            "similarity": round(score * 100, 2),

            "match_label": get_match_label(score)
        }

        recommendation["reason"] = explain_recommendation(
            movie_name,
            recommendation
        )

        recommendations.append(recommendation)

    return recommendations

# ==========================================================
# Testing
# ==========================================================

if __name__ == "__main__":

    recommendations = recommend("Avatar")

    for movie in recommendations:

        print("=" * 70)

        print(movie["title"])

        print(f"Similarity : {movie['similarity']}%")

        print(movie["match_label"])

        print("Genres :", ", ".join(movie["genres"]))

        print("Director :", ", ".join(movie["director"]))

        print("Cast :", ", ".join(movie["cast"][:3]))

        print()

        print("Why Recommended?")

        for reason in movie["reason"]:
            print("•", reason)

        print()