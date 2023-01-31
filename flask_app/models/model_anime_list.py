from flask import flash
from flask_app import DATABASE
from flask_app.models import model_anime
from flask_app.config.mysqlconnection import connectToMySQL

class Anime_List:
    def __init__( self , data ):
        self.id = data['id']
        self.anime_id = data["anime_id"]
        self.user_id = data["user_id"]

    @classmethod
    def create(cls,data):
        model_anime.Anime.check_is_in_db_add_if_not(data)
        query = "INSERT INTO anime_lists ( anime_id , user_id ) VALUES ( %(id)s , %(user_id)s );"
        return connectToMySQL(DATABASE).query_db( query, data )

    @classmethod
    def already_saved(cls,data):
        query = "SELECT * FROM anime_lists WHERE anime_id = %(id)s AND user_id = %(user_id)s;"
        results = connectToMySQL(DATABASE).query_db( query, data )
        return results

    @classmethod
    def delete(cls,data):
        query = "DELETE FROM anime_lists WHERE anime_id = %(anime_id)s AND user_id = %(user_id)s;"
        return connectToMySQL(DATABASE).query_db( query, data )