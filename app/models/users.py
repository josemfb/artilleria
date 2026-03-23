from werkzeug.security import check_password_hash, generate_password_hash

from app import db


class Usuario(db.Model):
    """
    Clase para los usuarios de Quintanet.
    Incluye datos básicos, y referencia a una hoja de servicios completa.
    """

    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    run = db.Column(db.String(64), index=True, unique=True)
    nombre = db.Column(db.String(64))
    apellido1 = db.Column(db.String(64))
    apellido2 = db.Column(db.String(64))
    pass_hash = db.Column(db.String(256))

    profile = db.relationship(
        "HojaServicio", backref="user", uselist=False, cascade="all, delete-orphan"
    )

    def set_password(self, password):
        self.pass_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pass_hash, password)

    def __repr__(self):
        return f"<User {self.nombre} {self.apellido1} {self.apellido2}>"
