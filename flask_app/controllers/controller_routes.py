from flask_app import app
from flask import session,render_template,redirect
from flask_app.models.model_anime import Anime

animes = []

@app.route('/')
def default():
    global animes
    print(session['next_pageination'])
    if len(animes) == 0:
        animes = Anime.get_api_animes()
    return render_template("index.html", animes = animes)

@app.route('/next_page')
def next_page():
    global animes
    animes = animes + Anime.get_api_animes_next()
    return redirect('/')