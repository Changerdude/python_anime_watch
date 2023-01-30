from flask_app import app
from flask import session,render_template,redirect
import json, requests

animes = []

@app.route('/')
def default():
    req = requests.get("https://kitsu.io/api/edge/anime?filter[status]=current&filter[subtype]=TV&page[limit]=20")
    data = json.loads(req.content)
    session['next_pageination'] = data["links"]["next"]
    for incAnime in data["data"]:
        anime = {
            "link" : incAnime["links"]["self"],
            "title" : incAnime["attributes"]["canonicalTitle"],
            "description" : incAnime["attributes"]["description"],
            "image" : incAnime["attributes"]["posterImage"]["large"]
        }
        animes.append(anime)
    return render_template("index copy.html", animes = animes)
