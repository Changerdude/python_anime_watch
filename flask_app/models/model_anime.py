from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import session
import json, requests

class Anime:
    def __init__( self , data ):
        self.id = data["id"]
        self.link = data["link"]
        self.title = data["title"]
        self.description = data["description"]
        self.image = data["description"]

    @classmethod
    def get_api_animes(cls):
        req = requests.get("https://kitsu.io/api/edge/anime?filter[status]=current&filter[subtype]=TV&page[limit]=20")
        data = json.loads(req.content)
        session['next_pageination'] = data["links"]["next"]
        print(session['next_pageination'])
        result = []
        for incAnime in data["data"]:
            anime = {
                "id" : incAnime["id"],
                "link" : incAnime["links"]["self"],
                "title" : incAnime["attributes"]["canonicalTitle"],
                "description" : incAnime["attributes"]["description"],
                "image" : incAnime["attributes"]["posterImage"]["large"]
            }
            if anime["description"] == None:
                anime["description"] = "No description available"
            result.append(anime)
        return result


    @classmethod
    def get_api_animes_next(cls):
        if session['next_pageination']:
            req = requests.get(session['next_pageination'])
            data = json.loads(req.content)
            if  "next" in  data["links"]:
                session['next_pageination'] = data["links"]["next"]
            else:
                session['next_pageination'] = False
            result = []
            for incAnime in data["data"]:
                anime = {
                    "id" : incAnime["id"],
                    "link" : incAnime["links"]["self"],
                    "title" : incAnime["attributes"]["canonicalTitle"],
                    "description" : incAnime["attributes"]["description"],
                    "image" : incAnime["attributes"]["posterImage"]["large"]
                }
                result.append(anime)
            return result
        return []