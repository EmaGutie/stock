from config.config import db
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, jsonify

class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_producto = db.Column(db.String(100), unique=True, nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Producto {self.nombre_producto} - Cantidad: {self.cantidad}>'
    def to_dict(self):
        return {
            'id': self.id,
            'nombre_producto': self.nombre_producto,
            'cantidad': self.cantidad
        }
    