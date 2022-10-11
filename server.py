from flask_app import app
from flask_app.controllers import user_cont
from flask_app.controllers import mygames_cont

if __name__=="__main__":
    app.run(debug=True)