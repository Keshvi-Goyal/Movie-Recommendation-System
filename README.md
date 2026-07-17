<<<<<<< HEAD
# 🎬 CineMatch AI

A basic **Content-Based Movie Recommendation System** built using **TF-IDF**, **weighted movie metadata**, and **cosine similarity**. The application provides explainable movie recommendations through an interactive **Streamlit** interface while using the **TMDB API** to fetch movie posters and additional metadata.

---

# Table of Contents

- Overview
- Features
- Tech Stack
- Project Workflow
- Project Structure
- Installation
- Usage
- Model Evaluation
- Future Scope
- Contributing
- License

---

# Overview

CineMatch AI recommends movies based on their content rather than user preferences or ratings.

The recommendation engine uses textual features extracted from movies, including genres, overview, keywords, cast, and director. These features are converted into weighted TF-IDF vectors, and cosine similarity is used to identify movies with similar content.

This project was developed to demonstrate the implementation of a content-based recommender system and provide a simple, explainable recommendation pipeline.

---

# Features

- Content-based recommendation engine
- Weighted TF-IDF feature representation
- Cosine similarity-based recommendations
- Explainable recommendations
- TMDB API integration
- Movie posters
- Ratings
- Genres
- Runtime
- Cast & Director information
- Interactive Streamlit interface
- Data preprocessing notebook
- Model evaluation notebook

---

# Tech Stack

### Programming Languages

- Python

### Machine Learning

- Scikit-learn
- TF-IDF Vectorizer
- Cosine Similarity

### Libraries

- Pandas
- NumPy
- Requests
- Pillow
- SciPy

### Web Framework

- Streamlit

### API

- TMDB API

---

# Project Workflow

The project workflow is as follows:

1. Data Collection
2. Data Cleaning & Preprocessing
3. Feature Engineering
4. TF-IDF Vectorization
5. Feature Weighting
6. Cosine Similarity Computation
7. Recommendation Generation
8. Metadata Fetching using TMDB API
9. Recommendation Visualization using Streamlit

---

# Project Structure

```text
Movie_Recommendation_System/

│── app.py
│── requirements.txt
│── README.md

├── assets/
├── data/
├── models/
├── notebooks/
├── src/
```

---

# Installation

## Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/Movie_Recommendation_System.git

cd Movie_Recommendation_System
```

---

## Create Virtual Environment

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Create Environment Variables

Create a `.env` file in the project root.

```env
TMDB_API_KEY=YOUR_API_KEY
```

---

## Train the Model (Optional)

If model files are unavailable:

```bash
python src/train.py
```

This generates

- movies.pkl
- similarity.pkl
- feature_matrix.pkl

---

## Run the Application

```bash
streamlit run app.py
```

The application will open in your browser.

If not, open

```
http://localhost:8501
```

---

# Usage

1. Launch the Streamlit application.
2. Search for a movie.
3. Click **Recommend**.
4. View recommended movies.
5. Expand any recommendation to view:
   - Overview
   - Genres
   - Director
   - Cast
   - Runtime
   - Release Date

---

# Model Evaluation

The repository also includes two notebooks.

### Data Preprocessing

- Data cleaning
- Metadata extraction
- Feature engineering

### Model Evaluation

- Dataset analysis
- Similarity score analysis
- Recommendation coverage
- Recommendation diversity
- Case studies
- Model limitations

---

# Future Scope

This project currently implements a **basic content-based recommendation system**.

Possible future improvements include:

- Hybrid recommendation system
- Collaborative filtering
- User authentication
- Personalized recommendations
- Sentence-BERT embeddings
- Approximate nearest neighbour search
- Watchlist functionality
- Movie search using live TMDB API
- Recommendation feedback system
- Real-time recommendation updates

---

# Contributing

Contributions are welcome.

Feel free to fork the repository, create a feature branch, and submit a pull request.

---

# License

This project is licensed under the MIT License.

---

# Author

**Keshvi Goyal**

B.Tech Mathematics & Computing

Interested in Machine Learning, Data Science and Quantitative Finance.
=======
# Movie-Recommendation-System
>>>>>>> 1432f9984fddd9b4098a39e99d25e37d6c951b6e
