from flask_app.config.mysqlconn import connectToMySQL
from flask import flash
from flask_app import app

class Game:
    db = 'MPG'
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.platform = data['platform']
        self.score = data['score']
        self.genre = data['genre']
        self.release_date = data['release_date']
        self.review = data['review']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def getOneGame(cls, data):
        query = 'SELECT * FROM games WHERE id = %(id)s;'
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def getGamePlayer(cls, data):
        query = 'SELECT users.username from users join games ON users.id = games.user_id where games.id = %(id)s;'
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return results[0]

    @classmethod
    def save(cls, data):
        query = "INSERT INTO games (title, platform, score, genre, release_date, review, created_at, updated_at, user_id) VALUES (%(title)s, %(platform)s, %(score)s, %(genre)s, %(release_date)s, %(review)s, NOW(), NOW(), %(user_id)s);"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def update(cls, data):
        query = "UPDATE games SET score = %(score)s, review = %(review)s WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def delete(cls, data):
        query = 'DELETE FROM games WHERE id = %(id)s;'
        return connectToMySQL(cls.db).query_db(query, data)


    @staticmethod
    def validateGame(data):
        is_valid = True

        if len(data['title']) < 1:
            flash("Please input game title")
            is_valid = False

        return is_valid
