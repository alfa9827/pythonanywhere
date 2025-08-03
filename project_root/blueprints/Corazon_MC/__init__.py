
from flask import Blueprint

corazon_mc_bp = Blueprint(
    'Corazon_MC',
    __name__,
    url_prefix='/corazon_mc',
    template_folder='templates'
)

from . import main
