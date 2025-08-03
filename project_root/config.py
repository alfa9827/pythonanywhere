import os

class Config:
    # Clave secreta para sesiones y CSRF (debe ser segura en producción)
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'cambia_por_una_clave_muy_segura_1234'

    # URI de conexión a la base de datos SQLite en archivo local
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(BASE_DIR, 'database.db')

    # Evita señales innecesarias (mejora rendimiento)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Otras configuraciones útiles
    # Tiempo de sesión en segundos (por ejemplo 1 día)
    PERMANENT_SESSION_LIFETIME = 86400  # 24h en segundos

    # Configuración para subir archivos (si llegas a implementar)
    # UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    # MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # Límite de 16MB
