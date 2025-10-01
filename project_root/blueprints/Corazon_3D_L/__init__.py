
from flask import Blueprint

corazon_3d_l_bp = Blueprint(
    'Corazon_3D_L',
    __name__,
    url_prefix='/corazon_3d_l',
    template_folder='templates'
)

from . import main
