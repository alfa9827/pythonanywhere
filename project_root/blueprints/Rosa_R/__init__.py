
from flask import Blueprint

rosa_r_bp = Blueprint(
    'Rosa_R',
    __name__,
    url_prefix='/rosa_r',
    template_folder='templates'
)

from . import main
