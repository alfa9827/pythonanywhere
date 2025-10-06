
from flask import Blueprint

block_bp = Blueprint(
    'Block',
    __name__,
    url_prefix='/block',
    template_folder='templates'
)

from . import main
