
from flask import Blueprint

corazon_p_bp = Blueprint(
    'Corazon_P',
    __name__,
    url_prefix='/corazon_p',
    template_folder='templates'
)

from . import main
