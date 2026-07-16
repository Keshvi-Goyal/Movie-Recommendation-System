import streamlit as st
import pandas as pd

from src.recommender import recommend
from src.utils import get_movie_metadata

st.set_page_config(
    page_title="Movie Recommendation System",
    page_icon="🎬",
    layout="wide"
)

with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

movies = pd.read_pickle("models/movies.pkl")

st.title("🎬 CineMatch AI")

st.caption("Discover movies you'll love.")

movie_name = st.selectbox(
    "Search Movie",
    sorted(movies["title"].unique())
)

if st.button("Recommend Movies", use_container_width=True):

    recommendations = recommend(movie_name)

    st.success(f"Top {len(recommendations)} recommendations")

    for movie in recommendations:

        meta = get_movie_metadata(movie["movie_id"])

        col1, col2 = st.columns([1,2])

        with col1:

            if meta and meta["poster"]:
                st.image(meta["poster"], use_container_width=True)

        with col2:

            st.markdown(
                f"<div class='title'>{movie['title']}</div>",
                unsafe_allow_html=True
            )

            st.markdown(
                f"<div class='similarity'>Similarity : {movie['similarity']}%</div>",
                unsafe_allow_html=True
            )

            if meta:

                st.write("⭐", meta["rating"])
                st.write("🎭", ", ".join(meta["genres"]))
                st.write("📅", meta["release_date"][:4])
                st.write("⏱", meta["runtime"], "mins")

                st.markdown(meta["overview"])

            st.write("👨‍🎤", ", ".join(movie["cast"][:3]))
            st.write("🎬", movie["director"][0])

            st.write("### Why Recommended?")

            for reason in movie["reason"]:
                st.success(reason)

        st.divider()