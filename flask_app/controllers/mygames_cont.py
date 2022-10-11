from flask_app import app
from flask_app.models.game import Game
from flask import render_template, redirect, session, request, flash, jsonify
import json
from igdb.wrapper import IGDBWrapper

wrapper = IGDBWrapper("j26xyns10sdlrmc9r3skgger81p228", "x0u61ezqiv7wljpc5v0ii8ye53zhrc")

# Opens a search page to find a game
@app.route('/search')
def search():
    user_data = {
        'id' : session['logged_user_id']
    }
    return render_template('/search.html')

# Returns a list of games matching the search
@app.route('/search/results', methods=['POST'])
def searchProcess():
    user_data = {
        'id' : session['logged_user_id']
    }
    if not Game.validateGame(request.form):
        return redirect('/search')

    search_data = {
        "title": request.form["title"]
    }
    
    r = wrapper.api_request('games', 'fields name; search "' + search_data["title"] + '"; limit 50;')
    decode = r.decode('utf-8')
    data = json.loads(decode)

    return render_template('/search.html', games = data)

# Opens the page for user input
@app.route('/new/<string:title>')
def create(title):
    user_data = {
        'id' : session['logged_user_id']
    }

    game = {
        'title' : title
    }

    r = wrapper.api_request('games', 'fields name, platforms.name, genres.name, release_dates.human; where name = "' + game['title'] + '";')
    decode = r.decode('utf-8')
    data = json.loads(decode)

    return render_template("/new.html", game = data)

# Processes the newly input game to be inserted into the database
@app.route('/new/process', methods=['POST'])
def gameProcess():
    data = {
        "title": request.form["title"],
        "platform": request.form["platform"],
        "score": request.form["score"],
        "genre": request.form["genre"],
        "release_date": request.form["release_date"],
        "review": request.form["review"],
        "user_id": session['logged_user_id']
    }
    Game.save(data)
    return redirect('/dashboard')

# View the review of a game
@app.route('/review/<int:id>')
def viewReview(id):
    user_data = {
        'id' : session['logged_user_id']
    }

    game_data = {
        "id": id
    }
    game = Game.getOneGame(game_data)
    return render_template("/review.html", game=game)

# Renders the page to edit a played game
@app.route('/edit/<int:id>')
def editGame(id):
    user_data = {
        'id' : session['logged_user_id']
    }
    game_data = {
        'id' : id
    }
    cur_game = Game.getOneGame(game_data)
    return render_template("/edit.html", cur_game=cur_game)

# Processes edits to existing games
@app.route('/edit/update', methods=['POST'])
def processGameUpdate():
    data = {
        "score": request.form["score"],
        "review": request.form["review"],
        "id": request.form["id"]
    }

    Game.update(data)
    return redirect('/dashboard')

# Removes a game
@app.route('/delete/<int:id>')
def deleteGame(id):
    game_data = {
        "id": id
    }
    Game.delete(game_data)
    return redirect('/dashboard')