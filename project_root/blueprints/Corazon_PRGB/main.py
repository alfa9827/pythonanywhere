import os
from flask import abort, render_template
from . import Corazon_PRGB_bp
from flask_login import login_required

@Corazon_PRGB_bp.route('/<string:archivo_html>')
@login_required
def mostrar_archivo(archivo_html):
    # Validaciones para evitar path traversal:
    if not archivo_html.endswith('.html'):
        abort(404)
    safe_path = os.path.normpath(archivo_html)
    if '..' in safe_path or os.path.isabs(safe_path):
        abort(404)

    # Intenta renderizar
    try:
        return render_template(archivo_html)
    except:
        abort(404)
