import pickle
import streamlit as st
import requests
import os


def fetch_poster(movie_id):
    try:
        api_key = os.getenv("TMDB_API_KEY", "294b1c8fa785d2c9a6f5241bf2c72bf6")
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
        resp = requests.get(url, timeout=10)
        if not resp.ok:
            return None
        data = resp.json()

        poster_path = data.get('poster_path')

        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
        else:
            return None   # IMPORTANT
    except Exception:
        return None

def recommend(movie):
    if movie not in movies['title'].values:
        return ["Movie not found"], []

    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    
    recommended_movie_names = []
    recommended_movie_posters = []

    for i in distances[1:11]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters

st.header('Movie Recommender System')
movies = pickle.load(open('model/movie_list.pkl','rb'))
similarity = pickle.load(open('model/similarity.pkl','rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    if not recommended_movie_names:
        st.warning("No recommendations found.")
    else:
        cols = st.columns(5)
        for col, name, poster in zip(cols, recommended_movie_names[:5], recommended_movie_posters[:5]):
            with col:
                st.text(name)
                if poster:
                    st.image(poster)
                else:
                    st.caption("Poster not available")





