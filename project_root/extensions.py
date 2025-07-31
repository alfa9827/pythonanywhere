from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

# Instancias globales sin app aún ligada
db = SQLAlchemy()
bcrypt = Bcrypt()
