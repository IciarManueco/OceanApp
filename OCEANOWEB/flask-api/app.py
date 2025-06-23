from flask import Flask, request, jsonify, render_template, redirect, url_for, session, flash
from flask_cors import CORS
from db import Usuario, AnimalMarino, Session as db_session, Base, engine
from werkzeug.security import generate_password_hash
from functools import wraps
import requests
import os
import logging
import time
from sqlalchemy import or_

# Configuración básica
app = Flask(__name__)
app.secret_key = 'clave_secreta'
CORS(app)

# Configuración de logging
LOG_FILE = 'app.log'
logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                    format='%(asctime)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

SPRING_BOOT_API = "http://localhost:8080/api/marine-animals"
LOCAL_API_PREFIX = '/api/v1'

# Decoradores
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Por favor inicia sesión', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'rol' not in session or session.get('rol') != 'admin':
            flash('Acceso denegado: se requieren privilegios de administrador', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

# Rutas principales
@app.route('/')
def index():
    return render_template('index.html', usuario=session.get('usuario'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario_form = request.form['usuario']
        contrasena_form = request.form['contrasena']
        db = db_session()
        user = db.query(Usuario).filter_by(usuario=usuario_form).first()
        if user and user.check_password(contrasena_form):
            session['user_id'] = user.id
            session['usuario'] = user.usuario
            session['rol'] = user.rol
            db.close()
            return redirect(url_for('perfil') if user.rol == 'admin' else url_for('index'))
        else:
            db.close()
            flash('Usuario o contraseña incorrectos', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Sesión cerrada', 'info')
    return redirect(url_for('index'))

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        usuario_form = request.form['usuario']
        email_form = request.form['email']
        contrasena_form = request.form['contrasena']
        db = db_session()
        if db.query(Usuario).filter_by(usuario=usuario_form).first():
            flash('El usuario ya existe', 'warning')
            db.close()
            return redirect(url_for('registro'))
        nuevo_usuario = Usuario(usuario=usuario_form, email=email_form, rol='usuario')
        nuevo_usuario.set_password(contrasena_form)
        db.add(nuevo_usuario)
        db.commit()
        db.close()
        flash('Registro exitoso. Ahora puedes iniciar sesión.', 'success')
        return redirect(url_for('login'))
    return render_template('registro.html')

@app.route('/perfil')
@login_required
@admin_required
def perfil():
    db = db_session()
    usuarios = db.query(Usuario).all()
    db.close()
    return render_template('perfil.html', usuarios=usuarios)

@app.route('/eliminar_usuario/<int:usuario_id>', methods=['POST'])
@login_required
@admin_required
def eliminar_usuario(usuario_id):
    db = db_session()
    user = db.query(Usuario).get(usuario_id)
    if user:
        db.delete(user)
        db.commit()
        flash(f'Usuario {user.usuario} eliminado', 'success')
    else:
        flash('Usuario no encontrado', 'warning')
    db.close()
    return redirect(url_for('perfil'))

# Animales
@app.route('/animales')
def animales():
    try:
        response = requests.get(f"{SPRING_BOOT_API}?limit=50")
        animales_api = response.json().get('data', []) if response.ok else []
        db = db_session()
        animales_locales = db.query(AnimalMarino).all()
        db.close()
        return render_template('animales.html',
                               animales_api=animales_api,
                               animales_locales=animales_locales,
                               usuario=session.get('usuario'))
    except requests.RequestException as e:
        logging.error(f"Error al conectar con la API externa: {e}")
        flash('Error al conectar con la API de animales', 'danger')
        return render_template('animales.html', animales_api=[], animales_locales=[])

@app.route(f'{LOCAL_API_PREFIX}/animals', methods=['GET'])
def get_animals():
    try:
        spring_response = requests.get(SPRING_BOOT_API)
        spring_data = spring_response.json() if spring_response.ok else {'data': []}
        db = db_session()
        local_animals = db.query(AnimalMarino).all()
        db.close()
        local_data = [{'id': f"local_{animal.id}",
                       'nombre': animal.nombre,
                       'especie': animal.especie,
                       'habitat': animal.habitat,
                       'origen': 'local'} for animal in local_animals]
        combined_data = spring_data.get('data', []) + local_data
        return jsonify({'status': 'success', 'count': len(combined_data), 'data': combined_data})
    except Exception as e:
        logging.error(f"Error general en get_animals: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/animales/buscar')
def buscar_animales():
    query = request.args.get('q', '').strip()
    habitat = request.args.get('habitat', '').strip()
    resultados_locales, resultados_api = [], []

    db = db_session()
    consulta = db.query(AnimalMarino)
    if query:
        consulta = consulta.filter(or_(
            AnimalMarino.nombre.ilike(f'%{query}%'),
            AnimalMarino.especie.ilike(f'%{query}%'),
            AnimalMarino.descripcion.ilike(f'%{query}%')
        ))
    if habitat:
        consulta = consulta.filter(AnimalMarino.habitat.ilike(f'%{habitat}%'))
    resultados_locales = consulta.all()
    db.close()

    try:
        params = {}
        if query: params['q'] = query
        if habitat: params['habitat'] = habitat
        response = requests.get(f"{SPRING_BOOT_API}/search", params=params)
        if response.ok:
            resultados_api = response.json().get('data', [])
    except requests.RequestException:
        logging.warning("No se pudo contactar con la API externa en búsqueda de animales")

    return render_template('buscar_animales.html',
                           query=query,
                           habitat=habitat,
                           resultados_locales=resultados_locales,
                           resultados_api=resultados_api,
                           usuario=session.get('usuario'))

# ------- Panel de errores ------
@app.route('/admin/errores')
@login_required
@admin_required
def admin_errores():
    logs = []
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r') as f:
            logs = f.readlines()[-100:]
    return render_template('admin_errores.html', logs=logs, usuario=session.get('usuario'))

@app.route('/admin/errores/limpiar', methods=['POST'])
@login_required
@admin_required
def limpiar_logs():
    open(LOG_FILE, 'w').close()
    flash("Logs limpiados", "success")
    return redirect(url_for('admin_errores'))

@app.route('/admin/simular_error/<int:error_code>')
@login_required
@admin_required
def simular_error(error_code):
    logging.warning(f"Simulando error {error_code}")
    return f"Simulación de error {error_code}", error_code

@app.route('/admin/simular_lentitud')
@login_required
@admin_required
def simular_lentitud():
    delay = int(request.args.get('delay', 3))
    logging.info(f"Simulando lentitud de {delay} segundos")
    time.sleep(delay)
    return f"Respuesta lenta después de {delay} segundos"

# ------ Manejo global de errores ------
@app.errorhandler(404)
def error_404(e):
    logging.warning(f"404 - {e}")
    return render_template('error_handler.html', error=e, error_code=404), 404

@app.errorhandler(500)
def error_500(e):
    logging.error(f"500 - {e}")
    return render_template('error_handler.html', error=e, error_code=500), 500

@app.errorhandler(Exception)
def error_general(e):
    logging.exception(f"Excepción general: {e}")
    return render_template('error_handler.html', error=e), 500

# Inicialización
if __name__ == '__main__':
    Base.metadata.create_all(engine)
    db = db_session()
    if not db.query(Usuario).filter_by(usuario='admin').first():
        admin = Usuario(usuario='admin', email='admin@oceano.com', rol='admin')
        admin.set_password('admin123')
        db.add(admin)
        db.commit()
    db.close()
    app.run(debug=True, port=5000)
