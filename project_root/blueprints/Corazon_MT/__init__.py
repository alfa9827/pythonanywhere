
from flask import Blueprint

corazon_mt_bp = Blueprint(
    'Corazon_MT',
    __name__,
    url_prefix='/corazon_mt',
    template_folder='templates'
)

from . import main
