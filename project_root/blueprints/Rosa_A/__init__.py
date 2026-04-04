
from flask import Blueprint

rosa_a_bp = Blueprint(
    'Rosa_A',
    __name__,
    url_prefix='/rosa_a',
    template_folder='templates'
)

from . import main
