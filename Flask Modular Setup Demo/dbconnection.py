from flask_sqlalchemy import SQLAlchemy
from app import myapp

db = SQLAlchemy()

myapp.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://zaid:0000@localhost/mytest'
myapp.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(myapp)