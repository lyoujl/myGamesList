from flask_app import app
from flask_app.models.user import User
from flask import render_template, redirect, session, request, flash
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

#Renders the login page
@app.route('/') 
def default():
    return render_template("/login.html")

#Processes new user data
@app.route('/user/register', methods=['POST'])
def newUser():
    if not User.validateReg(request.form):
        return redirect('/')

    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        "username": request.form["username"],
        "email": request.form["email"],
        "password": pw_hash
    }
    user_id = User.save(data)
    session['logged_user_id'] = user_id

    return redirect('/dashboard')

#Processes returning users to log them in
@app.route('/user/login', methods=['POST'])
def returningUser():
    if not User.validateLogin(request.form):
        return redirect('/')

    data = {
        "email": request.form["email"],
    }
    user = User.getUserByEmail(data)
    if user:
        if not bcrypt.check_password_hash(user.password, request.form['password']):
            flash("Account's password and inputted password do not match")
            return redirect('/')
            
        session['logged_user_id'] = user.id
        return redirect('/dashboard')

    return redirect('/')

#Renders the dashboard
@app.route('/dashboard')
def dashboard():
    user_data = {
        'id' : session['logged_user_id']
    }
    user = User.getUserByID(user_data)
    dashboard_games = User.dashboardGames()
    
    return render_template("/dashboard.html", cur_user=user, dash_games=dashboard_games)

#Logs out the current user
@app.route('/logout')
def logOut():
    session.clear()
    return redirect('/')