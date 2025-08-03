from flask import Blueprint

Corazon3DV_bp = Blueprint(
    'Corazon3DV',
    __name__,
    url_prefix='/corazon3DV',
    template_folder='templates'
)

from . import main
