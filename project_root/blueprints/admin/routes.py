from flask import render_template, request, redirect, url_for, flash, abort, current_app
from flask_login import login_required, current_user
from extensions import db
from models import Usuario, Grupo, Tarjeta
from . import admin_bp
import os
from werkzeug.utils import secure_filename
from extensions import bcrypt

def es_administrador():
    return current_user.is_authenticated and current_user.username == 'admin'

@admin_bp.before_request
@login_required
def verificar_admin():
    if not es_administrador():
        abort(403)

@admin_bp.route('/', methods=['GET'])
def index():
    usuarios = Usuario.query.order_by(Usuario.id).all()
    grupos = Grupo.query.order_by(Grupo.id).all()
    tarjetas = Tarjeta.query.order_by(Tarjeta.id).all()
    return render_template('admin.html', usuarios=usuarios, grupos=grupos, tarjetas=tarjetas)

@admin_bp.route('/test')
def test():
    return "Ruta de prueba en admin"

@admin_bp.route('/tarjetas/crear', methods=['POST'])
def crear_tarjeta():
    import textwrap

    nombre = request.form.get('nombre', '').strip()

    # Bloquear uso de carpeta 'admin'
    if nombre.lower() == 'admin':
        flash("No es permitido usar 'admin' como nombre de carpeta para una tarjeta.", "danger")
        return redirect(url_for('admin.index'))

    imagen = request.files.get('imagen')
    html_file = request.files.get('archivo_html')
    video_file = request.files.get('video')
    grupo_ids = request.form.getlist('grupo_ids')

    if not nombre or not imagen or not html_file:
        flash('Debes ingresar todos los campos y archivos requeridos', 'warning')
        return redirect(url_for('admin.index'))

    # Guardar Imagen en /static/images
    image_filename = secure_filename(imagen.filename)
    image_path = os.path.join(current_app.static_folder, 'images', image_filename)
    imagen.save(image_path)
    imagen_url = f'images/{image_filename}'

    # Crear carpeta de blueprint y guardar HTML
    blueprint_folder = os.path.join('blueprints', nombre)
    template_folder = os.path.join(blueprint_folder, 'templates')
    os.makedirs(template_folder, exist_ok=True)

    html_filename = secure_filename(html_file.filename)
    html_path = os.path.join(template_folder, html_filename)
    html_file.save(html_path)

    if not html_filename.endswith('.html'):
        flash('El archivo HTML debe terminar en .html', 'danger')
        return redirect(url_for('admin.index'))

    # Guardar video
    if video_file:
        video_filename = secure_filename(video_file.filename)
        videos_folder = os.path.join(current_app.static_folder, 'videos')
        os.makedirs(videos_folder, exist_ok=True)  # Asegura que exista la carpeta
        video_path = os.path.join(videos_folder, video_filename)
        video_file.save(video_path)
        video_url = f'videos/{video_filename}'
    else:
        video_url = None  # O un valor por defecto si es necesario

    # Crear archivos __init__.py y main.py
    clean_nombre = nombre.strip()
    blueprint_var = clean_nombre.lower() + '_bp'
    url_prefix = '/' + clean_nombre.lower()

    # __init__.py
    init_file_path = os.path.join(blueprint_folder, '__init__.py')
    init_content = f'''
    from flask import Blueprint

    {blueprint_var} = Blueprint(
        '{clean_nombre}',
        __name__,
        url_prefix='{url_prefix}',
        template_folder='templates'
    )

    from . import main
    '''
    with open(init_file_path, 'w', encoding='utf-8') as f:
        f.write(textwrap.dedent(init_content))

    # main.py
    main_file_path = os.path.join(blueprint_folder, 'main.py')
    main_content = f'''
    import os
    from flask import abort, render_template
    from . import {blueprint_var}
    from flask_login import login_required

    @{blueprint_var}.route('/')
    @login_required
    def mostrar_archivo():
        archivo_html = '{html_filename}'

        # Validaciones de seguridad
        if not archivo_html.endswith('.html'):
            abort(404)
        safe_path = os.path.normpath(archivo_html)
        if '..' in safe_path or os.path.isabs(safe_path):
            abort(404)

        try:
            return render_template(archivo_html)
        except:
            abort(404)
    '''
    with open(main_file_path, 'w', encoding='utf-8') as f:
        f.write(textwrap.dedent(main_content))

    # Guardar en la base de datos
    tarjeta = Tarjeta(
        nombre=nombre,
        carpeta=nombre,
        imagen_url=imagen_url,
        archivo_html=html_filename
    )
    grupos = Grupo.query.filter(Grupo.id.in_([int(gid) for gid in grupo_ids if gid.isdigit()])).all()
    tarjeta.grupos = grupos
    db.session.add(tarjeta)
    db.session.commit()

    flash(f'Tarjeta "{nombre}" creada correctamente', 'success')
    return redirect(url_for('admin.index'))

@admin_bp.route('/tarjetas/<int:tarjeta_id>/editar', methods=['POST'])
def editar_tarjeta(tarjeta_id):
    tarjeta = Tarjeta.query.get_or_404(tarjeta_id)
    nombre = request.form.get('nombre', '').strip()
    imagen_url = request.form.get('imagen_url', '').strip()
    archivo_html = request.form.get('archivo_html', '').strip()
    grupo_ids = request.form.getlist('grupo_ids')

    if not nombre or not imagen_url or not archivo_html:
        flash('Todos los campos son obligatorios para editar una tarjeta', 'warning')
        return redirect(url_for('admin.index'))

    blueprint_dir = os.path.join('blueprints', nombre)
    if not os.path.isdir(blueprint_dir):
        flash('La carpeta blueprint no existe.', 'danger')
        return redirect(url_for('admin.index'))

    image_path = os.path.join(current_app.static_folder, imagen_url)
    if not os.path.isfile(image_path):
        flash('La imagen especificada no existe.', 'danger')
        return redirect(url_for('admin.index'))

    tarjeta.nombre = nombre
    tarjeta.carpeta = nombre
    tarjeta.imagen_url = imagen_url
    tarjeta.archivo_html = archivo_html

    grupos = Grupo.query.filter(Grupo.id.in_([int(gid) for gid in grupo_ids if gid.isdigit()])).all()
    tarjeta.grupos = grupos if grupos else []

    db.session.commit()
    flash(f'Tarjeta "{tarjeta.nombre}" actualizada correctamente', 'success')
    return redirect(url_for('admin.index'))

@admin_bp.route('/tarjetas/<int:tarjeta_id>/eliminar', methods=['POST'])
def eliminar_tarjeta(tarjeta_id):
    tarjeta = Tarjeta.query.get_or_404(tarjeta_id)
    db.session.delete(tarjeta)
    db.session.commit()
    flash(f'Tarjeta "{tarjeta.nombre}" eliminada correctamente', 'success')
    return redirect(url_for('admin.index'))

@admin_bp.route('/usuarios/crear', methods=['POST'])
def crear_usuario():
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '').strip()
    grupo_ids = request.form.getlist('grupo_ids')

    if not username or not password:
        flash('Nombre de usuario y contraseña son obligatorios', 'warning')
        return redirect(url_for('admin.index'))

    if Usuario.query.filter_by(username=username).first():
        flash('El usuario ya existe', 'danger')
        return redirect(url_for('admin.index'))

    pw_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    usuario = Usuario(username=username, password_hash=pw_hash)

    grupos = Grupo.query.filter(Grupo.id.in_([int(gid) for gid in grupo_ids if gid.isdigit()])).all()
    usuario.grupos = grupos

    db.session.add(usuario)
    db.session.commit()

    flash(f'Usuario "{username}" creado correctamente', 'success')
    return redirect(url_for('admin.index'))


@admin_bp.route('/usuarios/<int:usuario_id>/editar', methods=['POST'])
def editar_usuario(usuario_id):
    usuario = Usuario.query.get_or_404(usuario_id)
    grupo_ids = request.form.getlist('grupo_ids')
    password = request.form.get('password', '').strip()

    grupos = Grupo.query.filter(Grupo.id.in_([int(gid) for gid in grupo_ids if gid.isdigit()])).all()
    usuario.grupos = grupos

    if password:
        usuario.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    db.session.commit()
    flash(f'Usuario "{usuario.username}" actualizado correctamente', 'success')
    return redirect(url_for('admin.index'))


@admin_bp.route('/usuarios/<int:usuario_id>/eliminar', methods=['POST'])
def eliminar_usuario(usuario_id):
    usuario = Usuario.query.get_or_404(usuario_id)
    if usuario.username == 'admin':
        flash('No puedes eliminar al usuario admin', 'danger')
        return redirect(url_for('admin.index'))

    db.session.delete(usuario)
    db.session.commit()
    flash(f'Usuario "{usuario.username}" eliminado correctamente', 'success')
    return redirect(url_for('admin.index'))

@admin_bp.route('/grupos/crear', methods=['POST'])
def crear_grupo():
    nombre = request.form.get('nombre', '').strip()
    usuario_ids = request.form.getlist('usuario_ids')
    tarjeta_ids = request.form.getlist('tarjeta_ids')

    if not nombre:
        flash('Nombre del grupo es obligatorio', 'warning')
        return redirect(url_for('admin.index'))

    if Grupo.query.filter_by(nombre=nombre).first():
        flash('El grupo ya existe', 'danger')
        return redirect(url_for('admin.index'))

    grupo = Grupo(nombre=nombre)

    usuarios = Usuario.query.filter(Usuario.id.in_([int(uid) for uid in usuario_ids if uid.isdigit()])).all()
    tarjetas = Tarjeta.query.filter(Tarjeta.id.in_([int(tid) for tid in tarjeta_ids if tid.isdigit()])).all()

    grupo.usuarios = usuarios
    grupo.tarjetas = tarjetas

    db.session.add(grupo)
    db.session.commit()

    flash(f'Grupo "{nombre}" creado correctamente', 'success')
    return redirect(url_for('admin.index'))


@admin_bp.route('/grupos/<int:grupo_id>/editar', methods=['POST'])
def editar_grupo(grupo_id):
    grupo = Grupo.query.get_or_404(grupo_id)
    nombre = request.form.get('nombre', '').strip()
    usuario_ids = request.form.getlist('usuario_ids')
    tarjeta_ids = request.form.getlist('tarjeta_ids')

    if not nombre:
        flash('El nombre del grupo es obligatorio', 'warning')
        return redirect(url_for('admin.index'))

    grupo.nombre = nombre

    usuarios = Usuario.query.filter(Usuario.id.in_([int(uid) for uid in usuario_ids if uid.isdigit()])).all()
    tarjetas = Tarjeta.query.filter(Tarjeta.id.in_([int(tid) for tid in tarjeta_ids if tid.isdigit()])).all()

    grupo.usuarios = usuarios
    grupo.tarjetas = tarjetas

    db.session.commit()
    flash(f'Grupo "{nombre}" actualizado correctamente', 'success')
    return redirect(url_for('admin.index'))


@admin_bp.route('/grupos/<int:grupo_id>/eliminar', methods=['POST'])
def eliminar_grupo(grupo_id):
    grupo = Grupo.query.get_or_404(grupo_id)
    db.session.delete(grupo)
    db.session.commit()
    flash(f'Grupo "{grupo.nombre}" eliminado correctamente', 'success')
    return redirect(url_for('admin.index'))
