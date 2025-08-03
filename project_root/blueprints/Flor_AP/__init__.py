
from flask import Blueprint

flor_ap_bp = Blueprint(
    'Flor_AP',
    __name__,
    url_prefix='/flor_ap',
    template_folder='templates'
)

from . import main
