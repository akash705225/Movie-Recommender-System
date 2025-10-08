import streamlit as st
import pickle
import pandas as pd
import requests

# 🔒 Store your API key safely (best practice: use secrets.toml or env vars in production)
API_KEY = "8265bd1679663a7ea12ac168da84d2e8"

# ⬇️ Fetch poster and overview using TMDB
def fetch_poster_and_overview(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    response = requests.get(url)
    data = response.json()
    poster_url = "https://image.tmdb.org/t/p/w500" + data.get("poster_path", "")
    overview = data.get("overview", "No overview available.")
    return poster_url, overview

# 🎯 Recommendation Function 1
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    
    recommended_titles = []
    recommended_posters = []
    recommended_overviews = []

    for i in distances[1:8]:
        movie_id = movies.iloc[i[0]].movie_id
        poster, overview = fetch_poster_and_overview(movie_id)
        recommended_titles.append(movies.iloc[i[0]].title)
        recommended_posters.append(poster)
        recommended_overviews.append(overview)

    return recommended_titles, recommended_posters, recommended_overviews

# 🎯 Recommendation Function 2
def recommend_simple(movie):
    index = movie3[movie3['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity1[index])), reverse=True, key=lambda x: x[1])
    
    recommended_titles = []
    recommended_posters = []

    for i in distances[1:8]:
        recommended_titles.append(movie3.iloc[i[0]].title)
        recommended_posters.append(movie3.iloc[i[0]].poster_path)

    return recommended_titles, recommended_posters

# 📦 Load Data
movies = pd.DataFrame(pickle.load(open("movie_d (1).pkl", "rb")))
movie3 = pd.DataFrame(pickle.load(open("movie_d2 (1).pkl", "rb")))

similarity = pickle.load(open("similarity3.pkl", "rb"))
similarity1 = pickle.load(open("similarity5.pkl", "rb"))

# 🖼️ UI
st.title("🎬 Movie Recommender System")

# Section 1: Content-Based Filtering (with overview)
st.subheader("🔍 Discover Movies Like Your Favorite (With Overview)")
selected_movie = st.selectbox("Choose a movie:", movies["title"].values)

if st.button('Recommend'):
    names, posters, overviews = recommend(selected_movie)
    cols = st.columns(7)
    for i in range(7):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])
            st.caption(overviews[i][:150] + "..." if len(overviews[i]) > 150 else overviews[i])

# Section 2: Simple Recommendation (with saved posters)
st.subheader("🧠 Discover More Movies (Quick Poster-Based)")
selected_movie2 = st.selectbox("Choose another movie:", movie3["title"].values)

if st.button('Recommend Simple'):
    names, posters = recommend_simple(selected_movie2)
    cols = st.columns(7)
    for i in range(7):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])
