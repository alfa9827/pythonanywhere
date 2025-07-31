
from flask import Blueprint

flor_an_bp = Blueprint(
    'Flor_AN',
    __name__,
    url_prefix='/flor_an',
    template_folder='templates'
)

from . import main
