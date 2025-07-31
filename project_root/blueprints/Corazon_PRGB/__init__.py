from flask import Blueprint

Corazon_PRGB_bp = Blueprint(
    'Corazon_PRGB',
    __name__,
    url_prefix='/corazon_PRGB',
    template_folder='templates'
)

from . import main
