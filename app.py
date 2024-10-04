'''
Author: Kousik Naskar
Email: kousik23naskar@gmail.com
Date: 2024-May-20
'''

import pickle
import streamlit as st
import requests

# Function to fetch movie poster
def fetch_poster(movie_id, api_key):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
    data = requests.get(url).json()
    poster_path = data.get('poster_path', '')
    full_path = f"https://image.tmdb.org/t/p/original/{poster_path}" if poster_path else ""
    return full_path

# Read the API key from a file
with open('api_key_tmdb.txt', 'r') as file:
    api_key = file.read().strip()

# Function to recommend movies
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:11]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_names.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id, api_key))

    return recommended_movie_names, recommended_movie_posters

# Load movie list and similarity data
movies = pickle.load(open('artifacts/model_trainer/movie_list.pkl', 'rb'))
similarity = pickle.load(open('artifacts/model_trainer/similarity.pkl', 'rb'))

# Streamlit app layout
st.set_page_config(page_title="Movie Recommender System", layout="wide")
st.title('🎬 Movie Recommender System')
st.write("Find your next favorite movie! Select a movie from the dropdown below and get recommendations based on it.")

# Movie selection dropdown
movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

# Show recommendations button
if st.button('Show Recommendation'):
    try:
        recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
        
        if recommended_movie_names:
            st.subheader(f"Movies recommended based on '{selected_movie}':")
            cols = st.columns(5)
            for idx, col in enumerate(cols):
                with col:
                    st.image(recommended_movie_posters[idx], width=150)
                    st.markdown(f"<div style='width: 150px; text-align: center;'>{recommended_movie_names[idx]}</div>", unsafe_allow_html=True)
                    #st.caption(recommended_movie_names[idx])
        else:
            st.error("Sorry, no recommendations found for the selected movie.")
    except Exception as e:
        st.error(f"An error occurred: {e}")

# Footer
st.markdown(
    """
    <style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #f1f1f1;
        color: black;
        text-align: center;
        padding: 10px;
    }
    </style>
    <div class="footer">
        <p>Developed by Kousik Naskar | Email: <a href="mailto:kousik23naskar@gmail.com">kousik23naskar@gmail.com</a></p>
    </div>
    """,
    unsafe_allow_html=True
)
