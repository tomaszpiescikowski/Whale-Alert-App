from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
app.config['SECRET_KEY'] = 'b9ab1b3e4a3afc97921af7d3'   #potrzebne do register_page
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from market import routes