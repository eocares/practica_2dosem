from ..database import db


class Interes(db.Model):
    __tablename__ = "intereses"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(60), nullable=False, unique=True)
    activo = db.Column(db.Boolean, nullable=False, default=True)


class Cliente(db.Model):
    __tablename__ = "clientes"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    telefono = db.Column(db.String(15))
    interes_id = db.Column(db.Integer, db.ForeignKey("intereses.id"), nullable=False)
    mensaje = db.Column(db.String(500))
    activo = db.Column(db.Boolean, nullable=False, default=True)  # borrado lógico
    creado_en = db.Column(db.DateTime, server_default=db.func.now())
    interes = db.relationship("Interes")
