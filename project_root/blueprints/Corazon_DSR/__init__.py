
from flask import Blueprint

corazon_dsr_bp = Blueprint(
    'Corazon_DSR',
    __name__,
    url_prefix='/corazon_dsr',
    template_folder='templates'
)

from . import main
