from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import secrets
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Habilita CORS correctamente

tokens_activos = {}
DATABASE = 'tareas.db'



# Crear las tablas si no existen
def init_db():
    with sqlite3.connect(DATABASE) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT UNIQUE NOT NULL,
                contrasena TEXT NOT NULL
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS tareas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER NOT NULL,
                descripcion TEXT NOT NULL,
                completada BOOLEAN NOT NULL DEFAULT 0,
                FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
            )
        ''')

# Obtener ID del usuario desde el nombre
def obtener_id_usuario(usuario):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.execute("SELECT id FROM usuarios WHERE usuario = ?", (usuario,))
        fila = cursor.fetchone()
        if fila:
            return fila[0]
        return None


# Ruta de inicio
@app.route('/')
def inicio():
    return "Servidor funcionando correctamente."

# Registro de usuario
@app.route('/registro', methods=['POST'])
def registrar_usuario():
    data = request.get_json()
    usuario = data.get('usuario')
    contrasena = data.get('contrasena')

    if not usuario or not contrasena:
        return jsonify({"error": "Faltan datos"}), 400

    hash_contrasena = generate_password_hash(contrasena)

    try:
        with sqlite3.connect(DATABASE) as conn:
            conn.execute(
                "INSERT INTO usuarios (usuario, contrasena) VALUES (?, ?)",
                (usuario, hash_contrasena)
            )
        return jsonify({"mensaje": "Usuario registrado con éxito"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "El usuario ya existe"}), 409

# Login de usuario
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    usuario = data.get('usuario')
    contrasena = data.get('contrasena')

    if not usuario or not contrasena:
        return jsonify({"error": "Faltan datos"}), 400

    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.execute(
            "SELECT contrasena FROM usuarios WHERE usuario = ?", (usuario,)
        )
        fila = cursor.fetchone()

    if fila is None:
        return jsonify({"error": "Usuario no encontrado"}), 404

    hash_almacenado = fila[0]

    if check_password_hash(hash_almacenado, contrasena):
        token = secrets.token_hex(16)
        tokens_activos[token] = usuario
        return jsonify({"mensaje": "Inicio de sesión exitoso", "token": token}), 200
    else:
        return jsonify({"error": "Contraseña incorrecta"}), 401

# HTML de bienvenida si está autenticado
@app.route('/tareas', methods=['GET'])
def mostrar_tareas():
    auth_header = request.headers.get('Authorization')
    if not auth_header or auth_header not in tokens_activos:
        return jsonify({"error": "No autorizado"}), 401

    usuario = tokens_activos[auth_header]

    html_bienvenida = f'''
    <html>
      <head><title>Gestión de Tareas</title></head>
      <body>
        <h1>¡Bienvenido a tu gestor de tareas, {usuario}!</h1>
        <p>Aquí podrás ver y administrar tus tareas.</p>
      </body>
    </html>
    '''
    return html_bienvenida

# Crear nueva tarea
@app.route('/tareas', methods=['POST'])
def crear_tarea():
    auth_header = request.headers.get('Authorization')
    if not auth_header or auth_header not in tokens_activos:
        return jsonify({"error": "No autorizado"}), 401

    usuario = tokens_activos[auth_header]
    usuario_id = obtener_id_usuario(usuario)

    data = request.get_json()
    descripcion = data.get('descripcion')

    if not descripcion:
        return jsonify({"error": "Falta la descripción de la tarea"}), 400

    with sqlite3.connect(DATABASE) as conn:
        conn.execute(
            "INSERT INTO tareas (usuario_id, descripcion, completada) VALUES (?, ?, ?)",
            (usuario_id, descripcion, False)
        )
    return jsonify({"mensaje": "Tarea creada con éxito"}), 201

# Listar tareas del usuario
@app.route('/tareas/listar', methods=['GET'])
def listar_tareas():
    auth_header = request.headers.get('Authorization')
    if not auth_header or auth_header not in tokens_activos:
        return jsonify({"error": "No autorizado"}), 401

    usuario = tokens_activos[auth_header]
    usuario_id = obtener_id_usuario(usuario)

    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.execute(
            "SELECT id, descripcion, completada FROM tareas WHERE usuario_id = ?",
            (usuario_id,)
        )
        tareas = [
            {"id": row[0], "descripcion": row[1], "completada": bool(row[2])}
            for row in cursor.fetchall()
        ]
    return jsonify(tareas)

# Eliminar tarea
@app.route('/tareas/<int:id>', methods=['DELETE'])
def borrar_tarea(id):
    auth_header = request.headers.get('Authorization')
    if not auth_header or auth_header not in tokens_activos:
        return jsonify({"error": "No autorizado"}), 401

    usuario = tokens_activos[auth_header]
    usuario_id = obtener_id_usuario(usuario)

    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.execute(
            "DELETE FROM tareas WHERE id = ? AND usuario_id = ?",
            (id, usuario_id)
        )
        if cursor.rowcount == 0:
            return jsonify({"error": "Tarea no encontrada o no te pertenece"}), 404

    return jsonify({"mensaje": "Tarea eliminada con éxito"})

@app.route('/tareas/<int:id>/completar', methods=['PATCH'])
def completar_tarea(id):
    auth_header = request.headers.get('Authorization')
    if not auth_header or auth_header not in tokens_activos:
        return jsonify({"error": "No autorizado"}), 401

    usuario = tokens_activos[auth_header]
    usuario_id = obtener_id_usuario(usuario)

    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.execute(
            "UPDATE tareas SET completada = 1 WHERE id = ? AND usuario_id = ?",
            (id, usuario_id)
        )
        if cursor.rowcount == 0:
            return jsonify({"error": "Tarea no encontrada o no te pertenece"}), 404

    return jsonify({"mensaje": "Tarea marcada como completada"})


# Iniciar servidor
if __name__ == '__main__':
    init_db()
    app.run(debug=True)