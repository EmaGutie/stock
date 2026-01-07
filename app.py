from flask import Flask, render_template, session, redirect, url_for
from config.config import db
from models.producto import Producto
from models.usuario import Usuario
from routes.crear_usuario import crear_usuario_bp
from routes.login import login_bp
from routes.productos import productos_bp

app = Flask(__name__)
app.secret_key = 'mi_clave_secreta_pizzas_123'

app.register_blueprint(crear_usuario_bp)
app.register_blueprint(login_bp)
app.register_blueprint(productos_bp)

app.config.from_object('config.config.Config')
db.init_app(app)

@app.route('/')
def home():
    return render_template('inicio.html')

@app.route('/')
def index():
    # Si el usuario tiene un ID en la sesión, significa que entró
    if 'usuario_id' in session:
        return render_template('pagina_central.html') # La página del sistema
    
    # Si no, lo mandamos al login
    return redirect(url_for('login.iniciar_sesion'))


@app.route('/central')
def dashboard():
    if 'usuario_id' not in session:
        return redirect(url_for('login.login'))
    
    # Buscamos solo los productos que pertenecen al usuario logueado
    mis_productos = Producto.query.filter_by(usuario_id=session['usuario_id']).all()

    return render_template('pagina_central.html', productos=mis_productos)




if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
