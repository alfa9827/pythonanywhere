
from flask import Blueprint

mariposas.html_bp = Blueprint(
    'Mariposas.html',
    __name__,
    url_prefix='/mariposas.html',
    template_folder='templates'
)

from . import main
