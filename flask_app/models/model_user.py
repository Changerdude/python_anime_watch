from flask import flash
from flask_app import DATABASE
from flask_app.models import model_anime
from flask_app.config.mysqlconnection import connectToMySQL
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]')
PW_REGEX = re.compile(r'^(.*[A-Z].*)')

class User:
    def __init__( self , data ):
        self.id = data['id']
        self.user_name = data["user_name"]
        self.user_icon = data["user_icon"]
        self.anime_list = []
        self.is_private = data["is_private"]
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.pw_hash = data['pw_hash']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        if not 'user_icon' in data:
            self.user_icon = "p6.jpg"
    
    @classmethod
    def create(cls,data):
        query = "INSERT INTO users ( user_name , user_icon , first_name , last_name , email , pw_hash , is_private ) VALUES ( %(user_name)s , %(user_icon)s , %(first_name)s , %(last_name)s , %(email)s , %(pw_hash)s , %(is_private)s );"
        return connectToMySQL(DATABASE).query_db( query, data )

    @classmethod
    def get_users(cls):
        query = "SELECT * FROM users"
        results = connectToMySQL(DATABASE).query_db( query )
        users = []
        for user in results:
            data = {
                "id" : user.id
            }
            anime_query = "SELECT * FROM animes WHERE id IN( SELECT anime_id FROM anime_lists WHERE user_id = %(id)s) ORDER BY title"
            anime_results = connectToMySQL(DATABASE).query_db( anime_query , data )
            for anime in anime_results:
                user["anime_list"].append(model_anime.Anime( anime ))
            users.append( cls(user) )
        return users
    
    @classmethod
    def get_public_users(cls):
        query = "SELECT * FROM users WHERE NOT is_private ORDER BY user_name"
        results = connectToMySQL(DATABASE).query_db( query )
        users = []
        for user in results:
            user = cls(user)
            data = {
                "id" : user.id
            }
            anime_query = "SELECT * FROM animes WHERE id IN( SELECT anime_id FROM anime_lists WHERE user_id = %(id)s) ORDER BY title"
            anime_results = connectToMySQL(DATABASE).query_db( anime_query , data )
            for anime in anime_results:
                user.anime_list.append(model_anime.Anime( anime ))
            users.append( user )
        return users

    @classmethod
    def get_user(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s"
        result = connectToMySQL(DATABASE).query_db( query, data )
        user = cls(result[0])
        if user.user_icon == None:
            user.user_icon = "p6.jpg"
        anime_query = "SELECT * FROM animes WHERE id IN( SELECT anime_id FROM anime_lists WHERE user_id = %(id)s) ORDER BY title"
        anime_results = connectToMySQL(DATABASE).query_db( anime_query , data )
        for anime in anime_results:
            user.anime_list.append(model_anime.Anime( anime ))
        return user

    @classmethod
    def get_user_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s"
        result = connectToMySQL(DATABASE).query_db( query, data)
        if result:
            return cls(result[0])
        return False
    
    @classmethod
    def get_user_by_user_name(cls,data):
        query = "SELECT * FROM users WHERE user_name = %(user_name)s"
        result = connectToMySQL(DATABASE).query_db( query, data)
        if result:
            return cls(result[0])
        return False
    
    @classmethod
    def user_update(cls,data):
        query = "UPDATE users SET user_name = %(user_name)s, first_name = %(first_name)s, last_name = %(last_name)s, user_icon = %(user_icon)s, email = %(email)s , is_private = %(is_private)s WHERE id = %(id)s"
        connectToMySQL(DATABASE).query_db( query, data )

    @classmethod
    def user_update_pw(cls,data):
        query = "UPDATE users SET pw_hash = %(pw_hash)s WHERE id = %(id)s"
        connectToMySQL(DATABASE).query_db( query, data )

    @classmethod
    def user_delete(cls,data):
        query = "DELETE FROM users WHERE id = %(id)s"
        return connectToMySQL(DATABASE).query_db( query, data )

    @classmethod
    def validate_pw(cls,pw):
        is_valid = True
        if len(pw) < 8:
            flash("Need a password at least 8 characters long", "err_pw_change")
            is_valid = False
        elif not PW_REGEX.match(pw):
            flash("Password needs at least one capitol and one number", "err_pw_change")
            is_valid = False
        return is_valid

    @classmethod
    def validate_registration(cls,data):
        is_valid = True
        if len(data['user_name']) < 1:
            flash("Needs a user name", "err_user_name_create")
            is_valid = False
        elif cls.get_user_by_user_name({"user_name":data["user_name"]}):
            flash("User name already exists", "err_user_name_create")
            is_valid = False
        if len(data['first_name']) < 2:
            flash("Needs a first name", "err_first_name_create")
            is_valid = False
        elif not NAME_REGEX.match(data['first_name']):
            flash("First name should only have letters", "err_first_name_create")
            is_valid = False
        if len(data['last_name']) < 2:
            flash("Needs a last name", "err_last_name_create")
            is_valid = False
        elif not NAME_REGEX.match(data['last_name']):
            flash("Last name should have only letters", "err_last_name_create")
            is_valid = False
        if len(data['email']) < 1:
            flash("Needs a email", "err_email_create")
            is_valid = False
        elif not EMAIL_REGEX.match(data["email"]):
            flash("Needs a valid email", "err_email_create")
            is_valid = False
        elif cls.get_user_by_email({"email":data["email"]}):
            flash("Email already exists", "err_email_create")
            is_valid = False
        if len(data['pw']) < 8:
            flash("Need a password at least 8 characters long", "err_pw_create")
            is_valid = False
        elif not PW_REGEX.match(data['pw']):
            flash("Password needs at least one capitol and one number", "err_pw_create")
            is_valid = False
        if len(data['pw_confirm']) < 1:
            flash("Need to confirm password", "err_pw_confirm_create")
            is_valid = False
        elif data['pw'] != data['pw_confirm']:
            flash("Passwords do not match", "err_pw_confirm_create")
            is_valid = False
        return is_valid