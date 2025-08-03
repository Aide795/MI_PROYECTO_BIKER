import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres.glpdduiyfjmhelanflvr:Gar38755522@aws-0-us-east-2.pooler.supabase.com:6543/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Cliente(db.Model):
    __tablename__ = 'clientes'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    email = db.Column(db.String(100))
    telefono = db.Column(db.String(50))
    ciudad = db.Column(db.String(50))
    pais = db.Column(db.String(50))
    servicio = db.Column(db.String(50))

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "email": self.email,
            "telefono": self.telefono,
            "ciudad": self.ciudad,
            "pais": self.pais,
            "servicio": self.servicio
        }

@app.route('/clientes', methods=['GET'])
def get_clientes():
    clientes = Cliente.query.all()
    return jsonify([c.to_dict() for c in clientes])

@app.route('/clientes', methods=['POST'])
def registrar_cliente():
    data = request.get_json()
    nuevo = Cliente(**data)
    db.session.add(nuevo)
    db.session.commit()
    return jsonify({"mensaje": "Cliente registrado", "cliente": nuevo.to_dict()}), 201

@app.route('/clientes', methods=['DELETE'])
def cancelar_servicio():
    data = request.get_json()
    cliente = Cliente.query.filter_by(email=data['email'], servicio=data['servicio']).first()
    if cliente:
        db.session.delete(cliente)
        db.session.commit()
        return jsonify({"mensaje": "Servicio cancelado correctamente"}), 200
    return jsonify({"mensaje": "No se encontró el servicio con ese correo"}), 404

@app.route('/')
def index():
    return "API de clientes corriendo correctamente."

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))