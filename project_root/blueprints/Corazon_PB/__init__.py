
from flask import Blueprint

corazon_pb_bp = Blueprint(
    'Corazon_PB',
    __name__,
    url_prefix='/corazon_pb',
    template_folder='templates'
)

from . import main
