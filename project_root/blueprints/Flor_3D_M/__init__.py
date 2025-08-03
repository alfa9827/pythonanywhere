
from flask import Blueprint

flor_3d_m_bp = Blueprint(
    'Flor_3D_M',
    __name__,
    url_prefix='/flor_3d_m',
    template_folder='templates'
)

from . import main
