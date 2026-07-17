import pickle
import ast
import pandas as pd

from pathlib import Path
from scipy.sparse import hstack

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ==========================================================
# Paths
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

# ==========================================================
# Load Dataset
# ==========================================================

movies = pd.read_csv(BASE_DIR / "data" / "movie_tags.csv")

# Convert string representations back to Python lists
for col in ["genres", "keywords", "cast", "crew"]:
    movies[col] = movies[col].apply(ast.literal_eval)

movies["overview"] = movies["overview"].fillna("")

print("=" * 60)
print("Loading Dataset...")
print("=" * 60)
print(f"Movies Loaded : {movies.shape[0]}")
print()

# ==========================================================
# Create TF-IDF Vectorizers
# ==========================================================

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

# ==========================================================
# Create Feature Matrices
# ==========================================================

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

# ==========================================================
# Feature Weighting
# ==========================================================

# Plot
overview_matrix *= 3

# Genres
genre_matrix *= 5

# Keywords
keyword_matrix *= 4

# Cast
cast_matrix *= 2

# Director
director_matrix *= 5

# ==========================================================
# Combine All Features
# ==========================================================

final_matrix = hstack([
    overview_matrix,
    genre_matrix,
    keyword_matrix,
    cast_matrix,
    director_matrix
])

# ==========================================================
# Cosine Similarity
# ==========================================================

similarity = cosine_similarity(
    final_matrix,
    dense_output=True
)

# ==========================================================
# Save Models
# ==========================================================

MODELS_DIR = BASE_DIR / "models"

MODELS_DIR.mkdir(exist_ok=True)

# Main files
with open(MODELS_DIR / "movies.pkl", "wb") as f:
    pickle.dump(movies, f)

with open(MODELS_DIR / "similarity.pkl", "wb") as f:
    pickle.dump(similarity, f)

with open(MODELS_DIR / "feature_matrix.pkl", "wb") as f:
    pickle.dump(final_matrix, f)

# Vectorizers
with open(MODELS_DIR / "overview_vectorizer.pkl", "wb") as f:
    pickle.dump(overview_vectorizer, f)

with open(MODELS_DIR / "genre_vectorizer.pkl", "wb") as f:
    pickle.dump(genre_vectorizer, f)

with open(MODELS_DIR / "keyword_vectorizer.pkl", "wb") as f:
    pickle.dump(keyword_vectorizer, f)

with open(MODELS_DIR / "cast_vectorizer.pkl", "wb") as f:
    pickle.dump(cast_vectorizer, f)

with open(MODELS_DIR / "director_vectorizer.pkl", "wb") as f:
    pickle.dump(director_vectorizer, f)

# ==========================================================
# Training Summary
# ==========================================================

print("=" * 60)
print("Training Summary")
print("=" * 60)

print(f"Movies               : {movies.shape}")
print(f"Overview Matrix      : {overview_matrix.shape}")
print(f"Genre Matrix         : {genre_matrix.shape}")
print(f"Keyword Matrix       : {keyword_matrix.shape}")
print(f"Cast Matrix          : {cast_matrix.shape}")
print(f"Director Matrix      : {director_matrix.shape}")
print(f"Combined Matrix      : {final_matrix.shape}")
print(f"Similarity Matrix    : {similarity.shape}")

print("=" * 60)
print("Training Completed Successfully!")
print("=" * 60)