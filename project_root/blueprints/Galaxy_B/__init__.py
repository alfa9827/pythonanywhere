
from flask import Blueprint

galaxy_b_bp = Blueprint(
    'Galaxy_B',
    __name__,
    url_prefix='/galaxy_b',
    template_folder='templates'
)

from . import main
