from flask_app import app
from flask import session,render_template,redirect
from flask_app.models.model_anime import Anime
from flask_app.models.model_user import User

animes = []

@app.route('/')
def default():
    global animes
    if len(animes) == 0:
        animes = Anime.get_api_animes()
    your_list = []
    user = {}
    public_users = User.get_public_users()
    if 'uuid' in session:
        user = User.get_user({'id' : session["uuid"]})
        your_list = user.anime_list
    return render_template("index.html", animes = animes, your_list = your_list, user = user , public_users = public_users )

@app.route('/next_page')
def next_page():
    global animes
    animes = animes + Anime.get_api_animes_next()
    return redirect('/')