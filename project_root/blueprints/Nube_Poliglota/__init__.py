
from flask import Blueprint

nube_poliglota_bp = Blueprint(
    'Nube_Poliglota',
    __name__,
    url_prefix='/nube_poliglota',
    template_folder='templates'
)

from . import main
