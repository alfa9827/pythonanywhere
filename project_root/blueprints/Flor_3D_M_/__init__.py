
from flask import Blueprint

flor_3d_m__bp = Blueprint(
    'Flor_3D_M_',
    __name__,
    url_prefix='/flor_3d_m_',
    template_folder='templates'
)

from . import main
