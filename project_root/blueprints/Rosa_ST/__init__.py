
from flask import Blueprint

rosa_st_bp = Blueprint(
    'Rosa_ST',
    __name__,
    url_prefix='/rosa_st',
    template_folder='templates'
)

from . import main
