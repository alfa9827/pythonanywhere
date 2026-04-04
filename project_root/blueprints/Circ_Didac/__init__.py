
from flask import Blueprint

circ_didac_bp = Blueprint(
    'Circ_Didac',
    __name__,
    url_prefix='/circ_didac',
    template_folder='templates'
)

from . import main
