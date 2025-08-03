
from flask import Blueprint

flor_aw_bp = Blueprint(
    'Flor_AW',
    __name__,
    url_prefix='/flor_aw',
    template_folder='templates'
)

from . import main
