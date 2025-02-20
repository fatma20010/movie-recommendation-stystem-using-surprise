import streamlit as st
import pickle
import pandas as pd

# Load the pre-trained model
with open('svd_model.pkl', 'rb') as f:
    model_svd = pickle.load(f)

# Load movie data
movies = pd.read_csv("movies.csv")
ratings = pd.read_csv("ratings.csv")

# Recommendation function
def recommend_svd(user_id, n=5):
    user_rated = ratings[ratings['userId'] == user_id]['movieId']
    user_unrated = movies[~movies['movieId'].isin(user_rated)]
    
    predictions = []
    for movie_id in user_unrated['movieId']:
        pred = model_svd.predict(user_id, movie_id)
        predictions.append((movie_id, pred.est))
    
    top = sorted(predictions, key=lambda x: x[1], reverse=True)[:n]
    return [movies[movies['movieId'] == movie_id]['title'].values[0] for movie_id, _ in top]

# Streamlit UI with enhanced design
st.markdown(
    """
    <style>
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-20px); }
        100% { transform: translateY(0px); }
    }
    
    .stApp {
        background: linear-gradient(135deg, #2a2356 0%, #4b3f72 100%);
        color: white;
        font-family: 'Comic Sans MS', cursive;
    }
    .title {
        text-align: center;
        font-size: 2.5em;
        color: #ffb3d9;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
        padding: 20px;
        animation: float 4s ease-in-out infinite;
    }
    .movie-card {
        background: rgba(255, 255, 255, 0.1);
        padding: 15px;
        border-radius: 20px;
        margin: 10px;
        border: 2px solid #ffb3d9;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        transition: transform 0.3s ease;
    }
    .movie-card:hover {
        transform: scale(1.02);
    }
    .movie-title {
        font-size: 1.1em;
        color: #ffffff;
        margin: 0;
    }
    .recommend-btn {
        background: linear-gradient(145deg, #ff99cc, #ff66a3) !important;
        color: white !important;
        border: none !important;
        border-radius: 15px !important;
        padding: 12px 25px !important;
        font-size: 1.1em !important;
        box-shadow: 0 4px 15px rgba(255, 153, 204, 0.4) !important;
        transition: all 0.3s ease !important;
    }
    .recommend-btn:hover {
        transform: scale(1.05);
        box-shadow: 0 6px 20px rgba(255, 153, 204, 0.6) !important;
    }
    .stNumberInput input {
        border-radius: 15px !important;
        border: 2px solid #ff99cc !important;
        color: #333333 !important; /* Dark text color for input */
        background-color: rgba(255, 255, 255, 0.9) !important; /* Light background for input */
    }
    .stNumberInput label {
        color: #ffb3d9 !important; /* Label color */
        font-size: 1.1em !important;
    }
    .floating-emoji {
        position: fixed;
        font-size: 24px;
        animation: float 3s ease-in-out infinite;
        opacity: 0.15;
        z-index: 0;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Add floating background elements
st.markdown("""
    <div class="floating-emoji" style="top: 15%; left: 10%;">🎈</div>
    <div class="floating-emoji" style="top: 25%; right: 15%;">🍿</div>
    <div class="floating-emoji" style="top: 60%; left: 5%;">🎬</div>
    <div class="floating-emoji" style="top: 70%; right: 10%;">🐾</div>
    <div class="floating-emoji" style="top: 45%; left: 20%;">🌟</div>
""", unsafe_allow_html=True)

# Title with animated emojis
st.markdown('<h1 class="title">🎀🍥 Movie Magic Recommender 🍿🐇</h1>', unsafe_allow_html=True)

# User input section
user_id = st.number_input("✨ Enter Your User ID:", min_value=1, step=1, help="Enter a number between 1 and 610")

# Recommendation button
if st.button("🌸 Get Cute Recommendations!", key="recommend_btn"):
    recommendations = recommend_svd(user_id)
    
    if recommendations:
        st.write("## 🎉 Your Special Picks:")
        
        # Display recommendations in a grid
        cols = st.columns(2)
        for i, movie in enumerate(recommendations):
            with cols[i % 2]:
                st.markdown(
                    f'<div class="movie-card">'
                    f'<p class="movie-title">🍀 {movie}</p>'
                    f'</div>',
                    unsafe_allow_html=True
                )
    else:
        st.error("🌈 Oopsie! No recommendations found. Try another magical number!")