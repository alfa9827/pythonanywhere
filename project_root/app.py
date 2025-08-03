import logging
import os
from flask import Flask, render_template, redirect, url_for, request, flash, abort
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from config import Config
from extensions import db, bcrypt
from models import Usuario, Grupo
from blueprints.admin import admin_bp
from jinja2 import ChoiceLoader, FileSystemLoader



# 🔧 Configuración inicial de la aplicación
app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
bcrypt.init_app(app)

# 🔐 Configuración de login
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = "info"

# 🧠 Cargar usuario
@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

# 🔧 Configurar logging
logging.basicConfig(level=logging.INFO)

# 📦 Registrar blueprint del admin
app.register_blueprint(admin_bp)

def get_all_tarjeta_carpetas():
    base_blueprints = os.path.join(os.path.dirname(__file__), 'blueprints')
    return [f for f in os.listdir(base_blueprints)
            if os.path.isdir(os.path.join(base_blueprints, f))]

base_path = os.path.abspath(os.path.dirname(__file__))
app.jinja_loader = ChoiceLoader([
    app.jinja_loader,
    FileSystemLoader([
        os.path.join(base_path, 'blueprints', carpeta, 'templates') for carpeta in get_all_tarjeta_carpetas()
    ])
])

# 📄 Página de error 403
@app.errorhandler(403)
def error_403(error):
    return render_template('errors/403.html'), 403

# 📄 Página de error 404
@app.errorhandler(404)
def error_404(error):
    return render_template('errors/404.html'), 404

# 📄 Página de error 500
@app.errorhandler(500)
def error_500(error):
    return render_template('errors/500.html'), 500

# 🔐 Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = Usuario.query.filter_by(username=username).first()
        if user and user.verificar_password(password):
            login_user(user)
            flash('Has iniciado sesión correctamente', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard'))
        else:
            flash('Usuario o contraseña incorrectos', 'danger')
    return render_template('login.html')

# 🔐 Logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión con éxito.', 'info')
    return redirect(url_for('login'))

# 📊 Panel de control
@app.route('/dashboard')
@login_required
def dashboard():
    tarjetas = set()
    for grupo in current_user.grupos:
        tarjetas.update(grupo.tarjetas)
    return render_template('dashboard.html', tarjetas=tarjetas)

# 🗂️ Mostrar tarjetas generadas dinámicamente
@app.route("/tarjetas/<carpeta>/<archivo_html>")
@login_required
def mostrar_tarjeta_generica(carpeta, archivo_html):
    if carpeta.lower() == 'admin':
        abort(404)

    if not archivo_html.endswith('.html') or '/' in archivo_html or '..' in carpeta or '..' in archivo_html:
        abort(404)

    base_dir = os.path.abspath(os.path.dirname(__file__))
    template_folder = os.path.join(base_dir, 'blueprints', carpeta, 'templates')
    filepath = os.path.join(template_folder, archivo_html)
    if not os.path.isfile(filepath):
        abort(404)
    try:
        return render_template(archivo_html)  # Sólo archivo, el loader busca en las carpetas ajustadas
    except Exception as e:
        app.logger.error(f'Error renderizando {archivo_html} en carpeta {carpeta}: {e}')
        abort(404)

# 🚀 Ejecutar la aplicación
if __name__ == '__main__':
    with app.app_context():
        pass  # Aquí puedes agregar inicializaciones adicionales si es necesario
    app.run(debug=True)  # En producción, debug=False
