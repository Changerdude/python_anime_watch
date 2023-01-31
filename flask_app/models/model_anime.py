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
        self.image = data["image"]


    @classmethod
    def create(cls,data):
        query = "INSERT INTO animes ( id , link , title , description , image ) VALUES ( %(id)s , %(link)s , %(title)s , %(description)s , %(image)s );"
        return connectToMySQL(DATABASE).query_db( query, data )

    @classmethod
    def check_is_in_db_add_if_not(cls,data):
        query = "SELECT * FROM animes WHERE id = %(id)s"
        result = connectToMySQL(DATABASE).query_db( query, data)
        if not result:
            cls.create(data)
        return True


    @classmethod
    def get_api_animes(cls):
        req = requests.get("https://kitsu.io/api/edge/anime?filter[status]=current&filter[subtype]=TV&page[limit]=20")
        data = json.loads(req.content)
        session['next_pageination'] = data["links"]["next"]
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
            result.append(cls(anime))
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
                result.append(cls(anime))
            return result
        return []