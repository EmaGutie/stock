from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.usuario import Usuario
from werkzeug.security import check_password_hash

login_bp = Blueprint('login', __name__)

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nombre = request.form.get('nombre_usuario')
        clave = request.form.get('contrasena')

        # Buscar al usuario por nombre
        usuario = Usuario.query.filter_by(nombre_usuario=nombre).first()

        # check_password_hash compara la clave escrita con la encriptada en la DB
        if usuario and check_password_hash(usuario.contrasena, clave):
            # Guardamos el ID en la sesión para saber que está logueado
            session['usuario_id'] = usuario.id
            flash('Bienvenido al sistema', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Usuario o contraseña incorrectos', 'error')
            
    return render_template('login.html')