
from flask import Blueprint

snoopy_bp = Blueprint(
    'Snoopy',
    __name__,
    url_prefix='/snoopy',
    template_folder='templates'
)

from . import main
