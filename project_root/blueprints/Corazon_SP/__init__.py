
from flask import Blueprint

corazon_sp_bp = Blueprint(
    'Corazon_SP',
    __name__,
    url_prefix='/corazon_sp',
    template_folder='templates'
)

from . import main
