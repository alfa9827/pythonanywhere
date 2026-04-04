
from flask import Blueprint

galaxy_p_bp = Blueprint(
    'Galaxy_P',
    __name__,
    url_prefix='/galaxy_p',
    template_folder='templates'
)

from . import main
