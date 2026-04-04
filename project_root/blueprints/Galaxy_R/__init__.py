
from flask import Blueprint

galaxy_r_bp = Blueprint(
    'Galaxy_R',
    __name__,
    url_prefix='/galaxy_r',
    template_folder='templates'
)

from . import main
