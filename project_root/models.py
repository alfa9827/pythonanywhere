from flask_login import UserMixin
from extensions import db

usuarios_grupos = db.Table(
    'usuarios_grupos',
    db.Column('usuario_id', db.Integer, db.ForeignKey('usuarios.id'), primary_key=True),
    db.Column('grupo_id', db.Integer, db.ForeignKey('grupos.id'), primary_key=True)
)

acceso_tarjetas_grupos = db.Table(
    'acceso_tarjetas_grupos',
    db.Column('grupo_id', db.Integer, db.ForeignKey('grupos.id'), primary_key=True),
    db.Column('tarjeta_id', db.Integer, db.ForeignKey('tarjetas.id'), primary_key=True)
)

class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    grupos = db.relationship('Grupo', secondary=usuarios_grupos, back_populates='usuarios')

    def __repr__(self):
        return f'<Usuario {self.username}>'

    def verificar_password(self, password):
        from app import bcrypt
        return bcrypt.check_password_hash(self.password_hash, password)

class Grupo(db.Model):
    __tablename__ = 'grupos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), unique=True, nullable=False)
    usuarios = db.relationship('Usuario', secondary=usuarios_grupos, back_populates='grupos')
    tarjetas = db.relationship('Tarjeta', secondary=acceso_tarjetas_grupos, back_populates='grupos')

    def __repr__(self):
        return f'<Grupo {self.nombre}>'

class Tarjeta(db.Model):
    __tablename__ = 'tarjetas'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    imagen_url = db.Column(db.String(200), nullable=False)
    carpeta = db.Column(db.String(100), nullable=False)
    archivo_html = db.Column(db.String(200), nullable=False)
    grupos = db.relationship('Grupo', secondary='acceso_tarjetas_grupos', back_populates='tarjetas')

    def __repr__(self):
        return f'<Tarjeta {self.nombre}>'
