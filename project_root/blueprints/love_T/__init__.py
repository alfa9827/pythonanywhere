
from flask import Blueprint

love_t_bp = Blueprint(
    'love_T',
    __name__,
    url_prefix='/love_t',
    template_folder='templates'
)

from . import main
