from flask import Flask, jsonify,render_template,request,redirect,url_for,flash, Blueprint
from config.config import db
from models.usuario import Usuario
from werkzeug.security import generate_password_hash

crear_usuario_bp = Blueprint('crear_usuario', __name__)

@crear_usuario_bp.route('/crear_usuario', methods=['GET', 'POST'])
def crear_usuario():
    if request.method == 'POST':
        nombre_usuario = request.form['nombre_usuario']
        contrasena = request.form['contrasena']
        confirmar_contrasena = request.form['confirmar_contrasena']

        # Verificar si las contraseñas coinciden
        if contrasena != confirmar_contrasena:
            flash('Las contraseñas no coinciden. Por favor, inténtalo de nuevo.', 'error')
            return redirect(url_for('crear_usuario.crear_usuario'))

        # Verificar si el nombre de usuario ya existe
        usuario_existente = Usuario.query.filter_by(nombre_usuario=nombre_usuario).first()
        if usuario_existente:
            flash('El nombre de usuario ya existe. Por favor, elige otro.', 'error')
            return redirect(url_for('crear_usuario.crear_usuario'))

        # Crear un nuevo usuario con la contraseña hasheada
        nuevo_usuario = Usuario(
            nombre_usuario=nombre_usuario,
            contrasena=generate_password_hash(contrasena)
        )
        db.session.add(nuevo_usuario)
        db.session.commit()

        flash('Usuario creado exitosamente.', 'success')
        return redirect(url_for('home'))

    return render_template('crear_usuario.html')