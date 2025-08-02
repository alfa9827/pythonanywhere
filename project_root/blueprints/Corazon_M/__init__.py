
from flask import Blueprint

corazon_m_bp = Blueprint(
    'Corazon_M',
    __name__,
    url_prefix='/corazon_m',
    template_folder='templates'
)

from . import main
