
from flask import Blueprint

corazon_sr_bp = Blueprint(
    'Corazon_SR',
    __name__,
    url_prefix='/corazon_sr',
    template_folder='templates'
)

from . import main
