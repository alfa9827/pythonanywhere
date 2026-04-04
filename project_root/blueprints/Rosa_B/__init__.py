
from flask import Blueprint

rosa_b_bp = Blueprint(
    'Rosa_B',
    __name__,
    url_prefix='/rosa_b',
    template_folder='templates'
)

from . import main
