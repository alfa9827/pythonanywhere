
from flask import Blueprint

corazon_ps_bp = Blueprint(
    'Corazon_PS',
    __name__,
    url_prefix='/corazon_ps',
    template_folder='templates'
)

from . import main
