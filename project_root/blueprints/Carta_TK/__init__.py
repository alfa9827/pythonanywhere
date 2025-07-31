
from flask import Blueprint

carta_tk_bp = Blueprint(
    'Carta_TK',
    __name__,
    url_prefix='/carta_tk',
    template_folder='templates'
)

from . import main
