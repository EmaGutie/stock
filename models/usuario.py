from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template
from config.config import db

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_usuario = db.Column(db.String(80), unique=True, nullable=False)
    contrasena = db.Column(db.String(250), nullable=False)
    confirmar_contrasena = db.Column(db.String(250), nullable=True)

    def __repr__(self):
        return f'<Usuario {self.nombre_usuario}>'