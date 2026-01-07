from flask import Flask, render_template, jsonify, Blueprint, request, session, redirect, url_for, flash
from config.config import db
from models.producto import Producto

productos_bp = Blueprint('productos', __name__)


#ruta para subir productos
@productos_bp.route('/subir_producto', methods=['GET', 'POST'])
def subir_producto():
    # Seguridad: Si no hay usuario en sesión, mandarlo al login
    if 'usuario_id' not in session:
        return redirect(url_for('login.iniciar_sesion'))

    if request.method == 'POST':
        nombre_producto = request.form.get('nombre_producto')
        cantidad = request.form.get('cantidad')
        precio = request.form.get('precio')

        nuevo_producto = Producto(
            nombre_producto=nombre_producto,
            cantidad=cantidad,
            precio=precio,
            usuario_id=session['usuario_id'] # Atamos el producto al usuario logueado
        )

        db.session.add(nuevo_producto)
        db.session.commit()
        flash('Producto cargado con éxito', 'success')
        return redirect(url_for('dashboard'))

    return render_template('subir_producto.html')

#Ruta para eliminar un producto
@productos_bp.route('/eliminar_producto/<int:id>')
def eliminar_producto(id):
    if 'usuario_id' not in session:
        return redirect(url_for('login.login'))

    # Buscamos el producto por su ID
    producto = Producto.query.get_or_404(id)

    # Seguridad: Verificamos que el producto pertenezca al usuario que intenta borrarlo
    if producto.usuario_id != session['usuario_id']:
        flash('No tienes permiso para eliminar este producto', 'danger')
        return redirect(url_for('dashboard'))

    db.session.delete(producto)
    db.session.commit()
    flash('Producto eliminado con éxito', 'warning')
    return redirect(url_for('dashboard'))


#Ruta para editar un producto
@productos_bp.route('/editar_producto/<int:id>', methods=['GET', 'POST'])
def editar_producto(id):
    if 'usuario_id' not in session:
        return redirect(url_for('login.login'))

    # Buscamos el producto que queremos editar
    producto = Producto.query.get_or_404(id)

    # Verificamos que sea del usuario logueado
    if producto.usuario_id != session['usuario_id']:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        # Tomamos los nuevos datos del formulario
        producto.nombre_producto = request.form.get('nombre_producto')
        producto.cantidad = request.form.get('cantidad')
        producto.precio = request.form.get('precio')

        db.session.commit() # Guardamos los cambios
        flash('Producto actualizado correctamente', 'success')
        return redirect(url_for('dashboard'))

    # Si es GET, mostramos la página de edición con los datos del producto
    return render_template('editar_producto.html', producto=producto)