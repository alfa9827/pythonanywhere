
from flask import Blueprint

fuegos_artificiales_bp = Blueprint(
    'Fuegos_Artificiales',
    __name__,
    url_prefix='/fuegos_artificiales',
    template_folder='templates'
)

from . import main
