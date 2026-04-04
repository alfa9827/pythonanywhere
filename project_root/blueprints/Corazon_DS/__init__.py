
from flask import Blueprint

corazon_ds_bp = Blueprint(
    'Corazon_DS',
    __name__,
    url_prefix='/corazon_ds',
    template_folder='templates'
)

from . import main
