import streamlit as st
import pickle
import pandas as pd
import requests as req


movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))
data = pd.DataFrame(movies_dict)

st.title('Movie Recommender System')

TMDB_API_KEY = "7e01a10e9ea8632050a0f0ce03356240"  


def fetch_poster(movie_id):
    
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=en-US"

    try:
        response = req.get(url)
        response.raise_for_status()
        movie_data = response.json()

        poster_path = movie_data.get("poster_path")
        if poster_path:
            return "https://image.tmdb.org/t/p/w500" + poster_path
        else:
            return "https://via.placeholder.com/500x750?text=No+Image"

    except:
        return "https://via.placeholder.com/500x750?text=Error"


def recommend(movie):
    movie_index = data[data["title"] == movie].index[0]
    distance = similarity[movie_index]
    movies_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:20]

    recommended_movies = []
    recommended_movies_posters = []

    for idx, score in movies_list:
        movie_id = data.iloc[idx].movie_id   
        recommended_movies.append(data.iloc[idx].title)
        recommended_movies_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movies_posters


selected_movie_name = st.selectbox("Select a movie", data['title'].values)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    cols = st.columns(3)

    for i in range(len(names)):
        with cols[i % 3]:
            st.text(names[i])
            st.image(posters[i], use_container_width=True)
