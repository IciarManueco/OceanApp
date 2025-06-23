import os
from functools import wraps

from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import declarative_base, sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash

# Definir la ruta y URL de la base de datos SQLite
basedir = os.path.abspath(os.path.dirname(__file__))
DATABASE_URL = f"sqlite:///{os.path.join(basedir, 'animales_marinos.db')}"

# Crear motor (engine)
engine = create_engine(DATABASE_URL, echo=True)

# Crear clase base declarativa
Base = declarative_base()

# Crear sessionmaker, todavía no inicializar sesión (se hace con db = Session())
Session = sessionmaker(bind=engine)


# Clase Usuario con hashing de contraseña
class Usuario(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True)
    usuario = Column(String(50), unique=True, nullable=False)  # nombre de usuario
    contrasena = Column(String(255), nullable=False)           # contraseña hasheada
    email = Column(String(100))
    rol = Column(String(20), default='usuario')

    def set_password(self, password):
        """Hashea y establece la contraseña."""
        self.contrasena = generate_password_hash(password)

    def check_password(self, password):
        """Verifica que la contraseña sea correcta."""
        return check_password_hash(self.contrasena, password)


# Clase AnimalMarino para datos de animales
class AnimalMarino(Base):
    __tablename__ = 'animales_marinos'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    especie = Column(String(100))
    habitat = Column(String(100))
    descripcion = Column(Text)
    imagen_url = Column(String(255))


