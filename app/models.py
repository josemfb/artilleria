from app import db


class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    run = db.Column(db.String(64), index=True, unique=True)
    nombre = db.Column(db.String(64))
    apellido1 = db.Column(db.String(64))
    apellido2 = db.Column(db.String(64))
    pass_hash = db.Column(db.String(256))

    profile = db.relationship('HojaServicios', backref='user', uselist=False, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<User {self.run}>'


class HojaServicios(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), unique=True, nullable=False)

    # TODO: check all this
    # Static Service Sheet Data
    rut = db.Column(db.String(12), unique=True, index=True)
    admission_date = db.Column(db.Date)
    birth_date = db.Column(db.Date)
    address = db.Column(db.String(255))
    phone_number = db.Column(db.String(20))
    blood_type = db.Column(db.String(5))
    profession = db.Column(db.String(100))

    # For lists (like Awards, Past Ranks, Sanctions), you should create 
    # separate tables (e.g., Award, RankHistory) with a ForeignKey to User.
