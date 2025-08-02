
from flask import Blueprint

flor_as_bp = Blueprint(
    'Flor_AS',
    __name__,
    url_prefix='/flor_as',
    template_folder='templates'
)

from . import main
