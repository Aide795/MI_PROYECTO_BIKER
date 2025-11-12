from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# Inicialización de la app Flask
app = Flask(__name__)
CORS(app)

# 🔧 Conexión a MySQL local (XAMPP)
# Asegúrate de tener creada la base de datos 'bikertapizados' en phpMyAdmin
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/bikertapizados'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# 🧱 Modelo de la tabla Servicio
class Servicio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    modelo = db.Column(db.String(100))
    precio = db.Column(db.Float)
    estado = db.Column(db.String(20), default="Activo")

# Crear tablas si no existen
with app.app_context():
    db.create_all()

# 🧭 Ruta principal
@app.route('/')
def home():
    return """
    <h2 style='text-align:center'>API Biker Tapizados</h2>
    <p style='text-align:center'>Usa las rutas /api/servicios para interactuar</p>
    """

# 🧭 Ruta para listar servicios
@app.route('/api/servicios', methods=['GET'])
def listar_servicios():
    servicios = Servicio.query.all()
    data = []
    for s in servicios:
        data.append({
            'id': s.id,
            'nombre': s.nombre,
            'modelo': s.modelo,
            'precio': s.precio,
            'estado': s.estado
        })
    return jsonify(data)

# 🧩 Ruta para crear un servicio
@app.route('/api/servicios', methods=['POST'])
def crear_servicio():
    data = request.get_json()
    nuevo = Servicio(
        nombre=data['nombre'],
        modelo=data['modelo'],
        precio=data['precio']
    )
    db.session.add(nuevo)
    db.session.commit()
    return jsonify({'mensaje': 'Servicio creado exitosamente'})

# ✏️ Ruta para actualizar un servicio
@app.route('/api/servicios/<int:id>', methods=['PUT'])
def actualizar_servicio(id):
    data = request.get_json()
    servicio = Servicio.query.get(id)
    if not servicio:
        return jsonify({'error': 'Servicio no encontrado'})
    servicio.nombre = data.get('nombre', servicio.nombre)
    servicio.modelo = data.get('modelo', servicio.modelo)
    servicio.precio = data.get('precio', servicio.precio)
    servicio.estado = data.get('estado', servicio.estado)
    db.session.commit()
    return jsonify({'mensaje': 'Servicio actualizado'})

# ❌ Ruta para eliminar un servicio
@app.route('/api/servicios/<int:id>', methods=['DELETE'])
def eliminar_servicio(id):
    servicio = Servicio.query.get(id)
    if not servicio:
        return jsonify({'error': 'Servicio no encontrado'})
    db.session.delete(servicio)
    db.session.commit()
    return jsonify({'mensaje': 'Servicio eliminado'})

# 🚀 Ejecutar servidor
if __name__ == '__main__':
    app.run(debug=True, port=5000)
