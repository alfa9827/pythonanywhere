
import os
from flask import abort, render_template
from . import flor_ap_bp
from flask_login import login_required

@flor_ap_bp.route('/')
@login_required
def mostrar_archivo():
    archivo_html = 'Flor_AP.html'

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
