from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:199535@localhost/stock'
    SQLALCHEMY_TRACK_MODIFICATIONS = False