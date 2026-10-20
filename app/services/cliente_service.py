import re
from sqlalchemy.exc import IntegrityError
from ..database import db
from ..models import Cliente, Interes

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class ServiceError(Exception):
    def __init__(self, msg, status=400):
        super().__init__(msg)
        self.status = status


def intereses_activos():
    return Interes.query.filter_by(activo=True).order_by(Interes.nombre).all()


def listar():
    return Cliente.query.filter_by(activo=True).order_by(Cliente.creado_en.desc()).all()


def obtener(cliente_id):
    return Cliente.query.filter_by(id=cliente_id, activo=True).first_or_404()


def _limpiar(d):
    nombre = (d.get("nombre") or "").strip()
    email = (d.get("email") or "").strip().lower()
    telefono = (d.get("telefono") or "").strip() or None
    mensaje = (d.get("mensaje") or "").strip()[:500] or None
    try:
        interes_id = int(d.get("interes_id"))
    except (TypeError, ValueError):
        raise ServiceError("Elige un curso de interés.")
    if len(nombre) < 3:
        raise ServiceError("Escribe tu nombre completo.")
    if not EMAIL_RE.match(email):
        raise ServiceError("Ingresa un correo válido.")
    if telefono and not re.fullmatch(r"\d{7,15}", telefono):
        raise ServiceError("El teléfono debe tener solo números (7 a 15).")
    return dict(nombre=nombre, email=email, telefono=telefono, interes_id=interes_id, mensaje=mensaje)


def _guardar(obj):
    try:
        db.session.add(obj)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        if "Duplicate" in str(e.orig):
            raise ServiceError("Ese correo ya está registrado.", 409)
        raise ServiceError("Curso no válido.")
    except Exception:
        db.session.rollback()
        raise ServiceError("No pudimos guardar tus datos. Intenta de nuevo.", 500)
    return obj


def crear(d):
    return _guardar(Cliente(**_limpiar(d)))


def actualizar(cliente_id, d):
    c = obtener(cliente_id)
    for k, v in _limpiar(d).items():
        setattr(c, k, v)
    return _guardar(c)


def eliminar(cliente_id):
    c = obtener(cliente_id)
    c.activo = False  # borrado lógico
    db.session.commit()
