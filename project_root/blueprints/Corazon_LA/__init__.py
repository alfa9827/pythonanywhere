
from flask import Blueprint

corazon_la_bp = Blueprint(
    'Corazon_LA',
    __name__,
    url_prefix='/corazon_la',
    template_folder='templates'
)

from . import main
