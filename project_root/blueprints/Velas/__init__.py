
from flask import Blueprint

velas_bp = Blueprint(
    'Velas',
    __name__,
    url_prefix='/velas',
    template_folder='templates'
)

from . import main
