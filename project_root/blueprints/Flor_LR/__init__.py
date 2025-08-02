
from flask import Blueprint

flor_lr_bp = Blueprint(
    'Flor_LR',
    __name__,
    url_prefix='/flor_lr',
    template_folder='templates'
)

from . import main
