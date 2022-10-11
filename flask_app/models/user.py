from flask_app.config.mysqlconn import connectToMySQL
from flask import flash
from flask_app import app
import re

email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    db = 'MPG'
    def __init__(self, data):
        self.id = data['id']
        self.username = data['username']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def getUserByID(cls, data):
        query = 'SELECT * from users WHERE id = %(id)s;'
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def getUserByEmail(cls, data):
        query = 'SELECT * from users WHERE email = %(email)s;'
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def dashboardGames(cls):
        query = 'SELECT users.id, users.username, games.id AS games_id, games.user_id AS player_id, games.title, games.platform, games.genre, games.release_date, games.score from users join games ON users.id = games.user_id;'
        results = connectToMySQL(cls.db).query_db(query)
        games = []
        for row in results:
            game_data = {
                'id' : row['id'],
                'username' : row['username'],
                'games_id' : row['games_id'],
                'player_id' : row['player_id'],
                'title' : row['title'],
                'platform' : row['platform'],
                'genre' : row['genre'],
                'release_date' : row['release_date'],
                'score' : row['score']
            }
            games.append(game_data)
        return games

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (username, email, password, created_at, updated_at) VALUES (%(username)s, %(email)s, %(password)s, NOW(), NOW());"
        return connectToMySQL(cls.db).query_db(query, data)

    @staticmethod
    def validateReg(data):
        is_valid = True
        user_exist = User.getUserByEmail(data)

        if user_exist:
            flash("Email already in use")
            is_valid = False

        if len(data['username']) < 2:
            flash("Username must be be at least 2 characters")
            is_valid = False

        if not email_regex.match(data['email']):
            flash("Invalid email address")
            is_valid = False

        if len(data['password']) < 8:
            flash("Password must be at least 8 characters")
            is_valid = False

        if data['password'] != data['confirm']:
            flash("Passwords do not match")
            is_valid = False

        return is_valid

    @staticmethod
    def validateLogin(data):
        is_valid = True
        user_exist = User.getUserByEmail(data)

        if not user_exist:
            flash("Account with that email does not exist")
            is_valid = False

        if not email_regex.match(data['email']):
            flash("Invalid email address")  
            is_valid = False   
        
        return is_valid


