from flask import Flask
from flask_bcrypt import Bcrypt
DATABASE = "anime_schema"
app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = "No dont do it"