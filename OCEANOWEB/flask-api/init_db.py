import os
from db import Base, engine, Session, Usuario, AnimalMarino

# Crear las tablas (si no existen)
Base.metadata.create_all(engine)

# Crear sesión activa
db = Session()

# Crear usuarios de ejemplo
usuarios = [
    Usuario(usuario="admin", email="admin@oceano.com", rol="admin"),
    Usuario(usuario="usuario", email="usuario@oceano.com", rol="usuario")
]

usuarios[0].set_password("admin123")
usuarios[1].set_password("usuario123")

db.add_all(usuarios)

# Lista animales marinos
animales = [
    AnimalMarino(
        nombre="Delfín nariz de botella",
        especie="Tursiops truncatus",
        habitat="Océanos templados y tropicales",
        descripcion="Los delfines son conocidos por su inteligencia y comportamiento social.",
        imagen_url="https://www.freepik.es/fotos-vectores-gratis/delf%C3%ADn-nariz-de-botella"
    ),
    AnimalMarino(
        nombre="Tiburón blanco",
        especie="Carcharodon carcharias",
        habitat="Aguas costeras y oceánicas",
        descripcion="El mayor depredador marino, conocido por su tamaño y fuerza.",
        imagen_url="https://concepto.de/tiburon-blanco/"
    ),
    AnimalMarino(
        nombre="Medusa luna",
        especie="Aurelia aurita",
        habitat="Mares templados y fríos",
        descripcion="Una medusa transparente con forma de campana que flota con las corrientes.",
        imagen_url="https://es.pinterest.com/ideas/medusas-luna/948642562775/"
    ),
    AnimalMarino(
        nombre="Caballito de mar común",
        especie="Hippocampus hippocampus",
        habitat="Arrecifes y pastos marinos",
        descripcion="Pequeño pez con cuerpo en forma de caballo, conocido por su método único de reproducción.",
        imagen_url="https://ejemplo.com/caballito_mar.jpg"
    ),
    AnimalMarino(
        nombre="Tortuga laúd",
        especie="Dermochelys coriacea",
        habitat="Océanos tropicales y subtropicales",
        descripcion="La tortuga marina más grande del mundo, conocida por su caparazón flexible.",
        imagen_url="https://ejemplo.com/tortuga_laud.jpg"
    ),
    AnimalMarino(
        nombre="Orca",
        especie="Orcinus orca",
        habitat="Océanos fríos y templados",
        descripcion="También conocida como ballena asesina, es un depredador tope en el océano.",
        imagen_url="https://ejemplo.com/orca.jpg"
    ),
    AnimalMarino(
        nombre="Pez payaso",
        especie="Amphiprioninae",
        habitat="Arrecifes de coral",
        descripcion="Famoso por su relación simbiótica con las anémonas de mar.",
        imagen_url="https://ejemplo.com/pez_payaso.jpg"
    ),
    AnimalMarino(
        nombre="Estrella de mar común",
        especie="Asterias rubens",
        habitat="Fondos marinos rocosos y arenosos",
        descripcion="Animal equinodermo con cinco brazos, capaz de regenerarlos.",
        imagen_url="https://ejemplo.com/estrella_mar.jpg"
    )
]

db.add_all(animales)

db.commit()
db.close()

print("Base de datos creada.")
