
from flask import Blueprint

corazon_sa_bp = Blueprint(
    'Corazon_SA',
    __name__,
    url_prefix='/corazon_sa',
    template_folder='templates'
)

from . import main
