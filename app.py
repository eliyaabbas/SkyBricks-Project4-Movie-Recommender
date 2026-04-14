import streamlit as st
import pickle
import pandas as pd
import requests

# Page Config
st.set_page_config(page_title="Movie Recommender", layout="wide", initial_sidebar_state="collapsed")

# Inject Custom CSS for Premium Aesthetics
st.markdown("""
<style>
    /* Background and global styles */
    .stApp {
        background: linear-gradient(135deg, #0d0e15 0%, #1a1e29 100%);
        color: #ffffff;
        font-family: 'Inter', sans-serif;
    }
    
    /* Header Customization */
    h1 {
        text-align: center;
        background: -webkit-linear-gradient(45deg, #ff416c, #ff4b2b);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem !important;
        font-weight: 800;
        margin-bottom: 2rem !important;
    }
    
    /* Subheader customization */
    .stMarkdown h3 {
        text-align: center;
        color: #b0b4c0;
        font-weight: 400;
        margin-bottom: 2rem !important;
    }

    /* Input selectbox styling */
    .stSelectbox > div > div {
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        color: white;
    }

    /* Button styling */
    .stButton > button {
        background: linear-gradient(45deg, #ff416c, #ff4b2b);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 2rem;
        font-weight: bold;
        transition: all 0.3s ease;
        display: block;
        margin: 0 auto;
        box-shadow: 0 4px 15px rgba(255, 75, 43, 0.4);
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255, 75, 43, 0.6);
        color: white;
        border: none;
    }

    /* Movie Title Cards */
    .movie-title {
        text-align: center;
        font-size: 1.1rem;
        font-weight: 600;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
        color: #e2e8f0;
        min-height: 50px;
    }
    
    /* Image hovering effect */
    [data-testid="stImage"] img {
        border-radius: 12px;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
    }
    [data-testid="stImage"] img:hover {
        transform: scale(1.05);
        box-shadow: 0 10px 25px rgba(255, 75, 43, 0.4);
    }
</style>
""", unsafe_allow_html=True)

st.title("🎬 Movie Recommender")
st.markdown("### Discover films similar to your favorites")

# Load data
@st.cache_data
def load_data():
    try:
        movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
        movies = pd.DataFrame(movies_dict)
        similarity = pickle.load(open('similarity.pkl', 'rb'))
        return movies, similarity
    except FileNotFoundError:
        st.error("Error: Could not find 'movie_dict.pkl' or 'similarity.pkl'. Please run the Jupyter Notebook first to generate these files.")
        st.stop()

movies, similarity = load_data()

# Function to fetch poster from TMDB API
def fetch_poster(movie_id):
    api_key = "8265bd1679663a7ea12ac168da84d2e8"
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
    try:
        response = requests.get(url)
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
    except Exception as e:
        pass
    return "https://via.placeholder.com/500x750/1a1e29/ffffff?text=No+Poster"

def recommend(movie_title):
    try:
        movie_index = movies[movies['title'] == movie_title].index[0]
        distances = similarity[movie_index]
        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
        
        recommended_movies = []
        recommended_movies_posters = []
        
        for i in movies_list:
            movie_id = movies.iloc[i[0]].id
            recommended_movies.append(movies.iloc[i[0]].title)
            recommended_movies_posters.append(fetch_poster(movie_id))
            
        return recommended_movies, recommended_movies_posters
    except IndexError:
        return [], []

# Centered Input
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    selected_movie_name = st.selectbox(
        '',
        movies['title'].values,
        index=int(movies[movies['title'] == 'Avatar'].index[0]) if 'Avatar' in movies['title'].values else 0,
        placeholder="Type or select a movie..."
    )
    
    st.write("") # Spacer
    recommend_button = st.button('Recommend Movies')

st.write("---")

if recommend_button:
    with st.spinner('Curating recommendations...'):
        names, posters = recommend(selected_movie_name)
        
        if names:
            # Display recommendations in 5 beautifully padded columns
            cols = st.columns(5, gap="large")
            for i, col in enumerate(cols):
                with col:
                    st.image(posters[i], use_container_width=True)
                    st.markdown(f'<div class="movie-title">{names[i]}</div>', unsafe_allow_html=True)
        else:
            st.error("Let's try another movie. We couldn't find recommendations for this one.")

# Footer space
st.markdown("<br><br><br>", unsafe_allow_html=True)
