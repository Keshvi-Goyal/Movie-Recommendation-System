import streamlit as st


# ==========================================================
# HEADER
# ==========================================================

def render_header():

    st.markdown(
        """
        <div style='text-align:center;padding:20px 0 10px 0'>
            <h1 style='font-size:3rem;margin-bottom:0;'>
                🎬 MOVIE RECOMMENDATION SYSTEM
            </h1>

            <p style='font-size:18px;color:#9ca3af;'>
                Discover movies you'll love using AI-powered
                content-based recommendations.
            </p>

        </div>
        """,
        unsafe_allow_html=True,
    )


# ==========================================================
# SIDEBAR
# ==========================================================

def render_sidebar():

    with st.sidebar:

        st.title("🎬 CineMatch AI")

        st.markdown("---")

        st.subheader("About")

        st.info(
            """
Hybrid Recommendation Engine

✅ TF-IDF

✅ Cosine Similarity

✅ Explainable AI

✅ TMDB API
"""
        )

        st.markdown("---")

        st.subheader("Tech Stack")

        st.write(
            """
- Python
- Streamlit
- Scikit-learn
- Pandas
- TMDB API
"""
        )

        st.markdown("---")

        st.subheader("Developer")

        st.write("**Keshvi Goyal**")

        st.caption("B.Tech Mathematics & Computing")


# ==========================================================
# SELECTED MOVIE
# ==========================================================

def render_selected_movie(meta):

    if meta is None:
        return

    st.subheader("🎥 Selected Movie")

    left, right = st.columns([1, 2])

    with left:

        if meta.get("poster"):
            st.image(
                meta["poster"],
                use_container_width=True,
            )

    with right:

        st.markdown(f"# {meta['title']}")

        c1, c2, c3 = st.columns(3)

        c1.metric("⭐ Rating", meta["rating"])

        c2.metric(
            "📅 Year",
            meta["release_date"][:4]
            if meta["release_date"] else "-"
        )

        c3.metric(
            "⏱ Runtime",
            f"{meta['runtime']} min"
            if meta["runtime"] else "-"
        )

        st.markdown("### 🎭 Genres")

        genre_html = ""

        for genre in meta["genres"][:5]:

            genre_html += (
                f"<span class='genre-chip'>{genre}</span>"
            )

        st.markdown(
            genre_html,
            unsafe_allow_html=True
        )

        with st.expander(
            "📖 Overview",
            expanded=True
        ):

            st.write(meta["overview"])

        if meta["director"]:

            st.write(
                f"**🎬 Director:** {meta['director']}"
            )

        if meta["cast"]:

            st.write(
                "**👨‍🎤 Cast:** "
                + ", ".join(meta["cast"][:5])
            )


# ==========================================================
# MOVIE CARD
# ==========================================================

def render_movie_card(movie, meta):

    st.markdown(
        "<div class='movie-card'>",
        unsafe_allow_html=True,
    )

    # ------------------------------------------------------

    if meta and meta.get("poster"):

        st.image(
            meta["poster"],
            use_container_width=True
        )

    # ------------------------------------------------------

    st.markdown(
        f"<div class='title'>{movie['title']}</div>",
        unsafe_allow_html=True
    )

    # ------------------------------------------------------

    if meta:

        left, right = st.columns(2)

        with left:

            st.markdown(
                f"⭐ **{meta['rating']}**"
            )

        with right:

            st.markdown(
                f"🎯 **{movie['similarity']}%**"
            )

    # ------------------------------------------------------

    st.progress(movie["similarity_raw"])

    # ------------------------------------------------------

    st.markdown(
        f"""
<div style="
font-weight:600;
color:#58A6FF;
margin-bottom:10px;">
{movie['match_label']}
</div>
""",
        unsafe_allow_html=True,
    )

    # ------------------------------------------------------

    if meta:

        chips = ""

        for genre in meta["genres"][:3]:

            chips += (
                f"<span class='genre-chip'>{genre}</span>"
            )

        st.markdown(
            chips,
            unsafe_allow_html=True,
        )

    st.markdown("")

    # ------------------------------------------------------

    for reason in movie["reason"]:

        st.markdown(
            f"""
<div class="reason">
{reason}
</div>
""",
            unsafe_allow_html=True,
        )

    # ------------------------------------------------------

    with st.expander("🔍 View Details"):

        if meta:

            st.write("### Overview")

            st.write(meta["overview"])

            st.write(
                f"**🎬 Director:** {meta['director']}"
            )

            st.write(
                f"**📅 Release:** {meta['release_date']}"
            )

            st.write(
                f"**⏱ Runtime:** {meta['runtime']} min"
            )

            st.write(
                "**👨‍🎤 Cast:** "
                + ", ".join(meta["cast"][:5])
            )

    st.markdown(
        "</div>",
        unsafe_allow_html=True,
    )