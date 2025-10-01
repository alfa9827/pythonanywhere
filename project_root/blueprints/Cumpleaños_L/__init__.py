
from flask import Blueprint

cumpleaños_l_bp = Blueprint(
    'Cumpleaños_L',
    __name__,
    url_prefix='/cumpleaños_l',
    template_folder='templates'
)

from . import main
