from flask_app import app
from flask_app.models import model_anime_list
from flask import session,redirect,request,flash

@app.route('/list/watch/add', methods=['POST'])
def add_to_list():
    data ={
        **request.form,
        "id" : int(request.form["id"]),
        "user_id" : session["uuid"]
    }
    if not model_anime_list.Anime_List.already_saved(data):
        model_anime_list.Anime_List.create(data)
    return redirect('/')

@app.route('/list/watch/remove/<int:id>')
def remove_from_list(id):
    data = {
        "user_id" : session["uuid"],
        "anime_id" : id
    }
    model_anime_list.Anime_List.delete(data)
    return redirect('/')

