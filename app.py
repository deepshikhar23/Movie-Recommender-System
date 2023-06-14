from flask import Flask, render_template, request
import pickle
import requests

app = Flask(__name__)

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=9085ea9f11d4fc5abc311586390effe1&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_listed = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    for i in movies_listed:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append((movies.iloc[i[0]].title, fetch_poster(movie_id)))
    return recommended_movies

movies = pickle.load(open('movies.pkl', 'rb'))
movies_list = movies['title'].values

similarity = pickle.load(open('similarity.pkl', 'rb'))

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', movies_list=movies_list)

@app.route('/recommend', methods=['POST'])
def get_recommendations():
    selected_movie = request.form['movie']
    recommendations = recommend(selected_movie)
    return render_template('recommendations.html', recommendations=recommendations)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8501)
