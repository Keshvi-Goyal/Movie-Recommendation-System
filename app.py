import streamlit as st
import pandas as pd

from src.recommender import recommend
from src.utils import get_movie_metadata
from src.components import (
    render_header,
    render_sidebar,
    render_selected_movie,
    render_movie_card,
)

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="🎬 CineMatch AI",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================================
# LOAD CSS
# ==========================================================

with open("assets/style.css") as css:
    st.markdown(
        f"<style>{css.read()}</style>",
        unsafe_allow_html=True
    )

# ==========================================================
# SESSION STATE
# ==========================================================

if "history" not in st.session_state:
    st.session_state.history = []

if "favorites" not in st.session_state:
    st.session_state.favorites = []

# ==========================================================
# LOAD DATA
# ==========================================================

@st.cache_data
def load_movies():
    return pd.read_pickle("models/movies.pkl")

movies = load_movies()

# ==========================================================
# SIDEBAR
# ==========================================================

render_sidebar()

# ==========================================================
# HEADER
# ==========================================================

render_header()

st.markdown("---")

# ==========================================================
# SEARCH SECTION
# ==========================================================

left, right = st.columns([5, 1])

with left:

    movie_name = st.selectbox(
        "Search Movie",
        sorted(movies["title"].unique()),
        label_visibility="collapsed",
        index=None,
        placeholder="🔍 Search for a movie..."
    )

with right:

    recommend_btn = st.button(
        "🎯 Recommend",
        use_container_width=True
    )

# ==========================================================
# EMPTY PAGE
# ==========================================================

if movie_name is None:

    st.info("👈 Search for a movie and click **Recommend** to discover similar movies.")

    st.stop()

# ==========================================================
# RECOMMENDATION
# ==========================================================

if recommend_btn:

    with st.spinner("Finding similar movies..."):

        selected_id = movies.loc[
            movies["title"] == movie_name,
            "movie_id"
        ].values[0]

        selected_meta = get_movie_metadata(selected_id)

        recommendations = recommend(movie_name)

        # Save history
        if movie_name not in st.session_state.history:
            st.session_state.history.insert(0, movie_name)

    st.success(f"Found {len(recommendations)} recommendations")

    # ======================================================
    # Selected Movie
    # ======================================================

    render_selected_movie(selected_meta)

    st.markdown("<br>", unsafe_allow_html=True)

    st.subheader("🍿 Recommended Movies")

    # ======================================================
    # Recommendation Grid
    # ======================================================

    cols = st.columns(4)

    for index, movie in enumerate(recommendations):

        meta = get_movie_metadata(movie["movie_id"])

        with cols[index % 4]:

            render_movie_card(movie, meta)

# ==========================================================
# HISTORY
# ==========================================================

if len(st.session_state.history) > 0:

    st.markdown("---")

    st.subheader("🕓 Recent Searches")

    cols = st.columns(min(len(st.session_state.history), 5))

    for i, movie in enumerate(st.session_state.history[:5]):

        with cols[i]:

            st.button(
                movie,
                key=f"history_{i}",
                use_container_width=True
            )