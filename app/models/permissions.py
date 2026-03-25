from app import db


class RolePermission(db.Model):
    __tablename__ = "role_permissions"

    id = db.Column(db.Integer, primary_key=True)
    # If null, applies to everyone (Default / No rank)
    tipo_cargo_id = db.Column(
        db.Integer, db.ForeignKey("tipos_cargo.id"), nullable=True
    )
    permission = db.Column(db.String(64), nullable=False)

    tipo_cargo = db.relationship("TipoCargo", backref="permissions")
