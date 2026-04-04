
from flask import Blueprint

rosa_n_bp = Blueprint(
    'Rosa_N',
    __name__,
    url_prefix='/rosa_n',
    template_folder='templates'
)

from . import main
