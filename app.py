import streamlit as st
import pickle
import pandas as pd
import requests

API_KEY = "a60fc577a0639898a64611483c79321f"

def fetch_poster(movie_id):
    response = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US")
    data = response.json()

    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

movies_dict = pickle.load(open('movie_list.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

# Custom CSS styles
st.markdown(
    """
    <style>
    .main {
        background-color: #222;
        padding: 2rem;
        border-radius: 10px;
    }
    .movie-title {
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .movie-poster {
        margin-bottom: 1rem;
        transition: transform 0.2s ease-in-out;
    }
    .movie-poster:hover {
        transform: scale(1.05);
    }
    .recommend-button {
        background-color: #0088cc;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        font-size: 18px;
        border-radius: 5px;
        cursor: pointer;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title('Movie Recommender System')

# Add a background color to the main section
st.markdown('<div class="main">', unsafe_allow_html=True)

selected_movie_name = st.selectbox(
    'Select a movie:',
    movies['title'].values
)

if st.button('Recommend', key='recommend-button'):
    if selected_movie_name:
        with st.spinner('Fetching recommendations...'):
            recommended_movie_names, recommended_movie_posters = recommend(selected_movie_name)

        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.text(recommended_movie_names[0])
            st.image(recommended_movie_posters[0], use_column_width=True, caption=recommended_movie_names[0])
        with col2:
            st.text(recommended_movie_names[1])
            st.image(recommended_movie_posters[1], use_column_width=True, caption=recommended_movie_names[1])
        with col3:
            st.text(recommended_movie_names[2])
            st.image(recommended_movie_posters[2], use_column_width=True, caption=recommended_movie_names[2])
        with col4:
            st.text(recommended_movie_names[3])
            st.image(recommended_movie_posters[3], use_column_width=True, caption=recommended_movie_names[3])
        with col5:
            st.text(recommended_movie_names[4])
            st.image(recommended_movie_posters[4], use_column_width=True, caption=recommended_movie_names[4])
    else:
        st.error("Please select a movie.")

# Close the main section
st.markdown('</div>', unsafe_allow_html=True)
