import pickle
import pandas as pd
import ast

from pathlib import Path
from scipy.sparse import hstack

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

BASE_DIR = Path(__file__).resolve().parent.parent

# -----------------------------
# Load Data
# -----------------------------

movies = pd.read_csv(BASE_DIR / "data" / "movie_tags.csv")

# Convert list-like strings back to Python lists
for col in ["genres", "keywords", "cast", "crew"]:
    movies[col] = movies[col].apply(ast.literal_eval)

movies["overview"] = movies["overview"].fillna("")

# -----------------------------
# Create TF-IDF Vectorizers
# -----------------------------

overview_vectorizer = TfidfVectorizer(
    stop_words="english",
    max_features=5000
)

genre_vectorizer = TfidfVectorizer(
    token_pattern=r"[^ ]+"
)

keyword_vectorizer = TfidfVectorizer(
    token_pattern=r"[^ ]+"
)

cast_vectorizer = TfidfVectorizer(
    token_pattern=r"[^ ]+"
)

director_vectorizer = TfidfVectorizer(
    token_pattern=r"[^ ]+"
)

# -----------------------------
# Create Feature Matrices
# -----------------------------

overview_matrix = overview_vectorizer.fit_transform(
    movies["overview"]
)

genre_matrix = genre_vectorizer.fit_transform(
    movies["genres"].apply(lambda x: " ".join(x))
)

keyword_matrix = keyword_vectorizer.fit_transform(
    movies["keywords"].apply(lambda x: " ".join(x))
)

cast_matrix = cast_vectorizer.fit_transform(
    movies["cast"].apply(lambda x: " ".join(x))
)

director_matrix = director_vectorizer.fit_transform(
    movies["crew"].apply(lambda x: " ".join(x))
)

# -----------------------------
# Apply Weights
# -----------------------------

overview_matrix *= 3
genre_matrix *= 5
keyword_matrix *= 4
cast_matrix *= 2
director_matrix *= 5

# -----------------------------
# Combine All Features
# -----------------------------

final_matrix = hstack([
    overview_matrix,
    genre_matrix,
    keyword_matrix,
    cast_matrix,
    director_matrix
])

print("Combined Matrix Shape:", final_matrix.shape)

# -----------------------------
# Similarity Matrix
# -----------------------------

similarity = cosine_similarity(final_matrix)

print("Similarity Shape:", similarity.shape)

# -----------------------------
# Save Models
# -----------------------------

with open(BASE_DIR / "models" / "movies.pkl", "wb") as f:
    pickle.dump(movies, f)

with open(BASE_DIR / "models" / "similarity.pkl", "wb") as f:
    pickle.dump(similarity, f)

with open(BASE_DIR / "models" / "overview_vectorizer.pkl", "wb") as f:
    pickle.dump(overview_vectorizer, f)

print("\nTraining completed successfully!")