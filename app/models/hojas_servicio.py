import calendar
from datetime import date, timedelta

from app import db

MOTIVOS_BAJA = ("Falleció", "Renunció", "Separado", "Expulsado")
CATEGORIAS = ("Voluntario activo", "Voluntario honorario", "Voluntario 3.ª Valparaíso")
CATEGORIAS_CARGO = ("Compañía", "Cuerpo")

CARGOS_INICIAL = (
    ("Director", "Compañía"),
    ("Capitán", "Compañía"),
    ("Teniente 1.º", "Compañía"),
    ("Teniente 2.º", "Compañía"),
    ("Teniente 3.º", "Compañía"),
    ("Secretario", "Compañía"),
    ("Tesorero", "Compañía"),
    ("Intendente", "Compañía"),
    ("Maquinista", "Compañía"),
    ("Ayudante", "Compañía"),
    ("Consejero de Disciplina", "Compañía"),
    ("Consejero de Disciplina Suplente", "Compañía"),
    ("Cirujano", "Compañía"),
    ("Superintendente", "Cuerpo"),
    ("Vicesuperintendente", "Cuerpo"),
    ("Comandante", "Cuerpo"),
    ("2.º Comandante", "Cuerpo"),
    ("3.º Comandante", "Cuerpo"),
    ("4.º Comandante", "Cuerpo"),
    ("Secretario General", "Cuerpo"),
    ("Tesorero General", "Cuerpo"),
    ("Intendente General", "Cuerpo"),
    ("Director Honorario", "Cuerpo"),
    ("Inspector de Administración", "Cuerpo"),
    ("Ayudante de Administración", "Cuerpo"),
    ("Inspector de Comandancia", "Cuerpo"),
    ("Ayudante de Comandancia", "Cuerpo"),
)

COMPETENCIAS = (
    "Premio Dávila",
    "Premio Matte",
    "Premio M. Humbser",
    "Premio J.M. Besoaín",
)
NIVELES_ACADEMICOS = ("Bombero inicial", "Bombero operativo", "Bombero profesional")


class HojaServicio(db.Model):
    __tablename__ = "hojas_servicio"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), unique=True)

    # Datos básicos y registro
    fecha_alta = db.Column(db.Date)
    num_registro_general = db.Column(db.Integer)
    num_registro_quinta = db.Column(db.Integer)
    fecha_baja = db.Column(db.Date, nullable=True)
    motivo_baja = db.Column(
        db.Enum(*MOTIVOS_BAJA, name="motivo_baja_enum"),
        nullable=True,
    )
    categoria = db.Column(
        db.Enum(
            *CATEGORIAS,
            name="categoria_enum",
        )
    )

    # Datos personales
    fecha_nacimiento = db.Column(db.Date)
    ocupacion = db.Column(db.String(128))
    direccion = db.Column(db.String(256))
    telefono = db.Column(db.String(20))
    email = db.Column(db.String(120))

    # Voluntarios patrocinantes
    patrocinante1_id = db.Column(
        db.Integer, db.ForeignKey("usuarios.id"), nullable=True
    )
    patrocinante2_id = db.Column(
        db.Integer, db.ForeignKey("usuarios.id"), nullable=True
    )

    # Relaciones para acceder a los nombres de los patrocinantes
    patrocinante1 = db.relationship("Usuario", foreign_keys=[patrocinante1_id])
    patrocinante2 = db.relationship("Usuario", foreign_keys=[patrocinante2_id])

    # Relaciones uno-a-muchos con las tablas auxiliares
    # TODO: app/models/guardia.py
    # noches_guardia = db.relationship(
    #     "NocheGuardia", back_populates="hoja", lazy=True, cascade="all, delete-orphan"
    # )
    altas_anteriores = db.relationship(
        "AltaAnterior", back_populates="hoja", lazy=True, cascade="all, delete-orphan"
    )
    asistencias = db.relationship(
        "Asistencia", back_populates="hoja", lazy=True, cascade="all, delete-orphan"
    )
    premios = db.relationship(
        "PremioAsistencia",
        back_populates="hoja",
        lazy=True,
        cascade="all, delete-orphan",
    )
    cargos = db.relationship(
        "Cargo", back_populates="hoja", lazy=True, cascade="all, delete-orphan"
    )
    operadores = db.relationship(
        "Operador", back_populates="hoja", lazy=True, cascade="all, delete-orphan"
    )
    competencias = db.relationship(
        "Competencia", back_populates="hoja", lazy=True, cascade="all, delete-orphan"
    )
    cursos = db.relationship(
        "Curso", back_populates="hoja", lazy=True, cascade="all, delete-orphan"
    )
    niveles_academicos = db.relationship(
        "NivelAcademico", back_populates="hoja", lazy=True, cascade="all, delete-orphan"
    )
    otras_anotaciones = db.relationship(
        "OtraAnotacion", back_populates="hoja", lazy=True, cascade="all, delete-orphan"
    )

    @property
    def cargo_actual(self):
        cargos = [
            c.nombre_cargo
            for c in self.cargos
            if c.fecha_termino is None and c.nombre_cargo
        ]
        return ", ".join(cargos) if cargos else None

    @property
    def antiguedad(self):
        sum_dias_anteriores = sum((a.total_dias or 0) for a in self.altas_anteriores)

        fecha_alta_simulada = self.fecha_alta - timedelta(days=sum_dias_anteriores)

        today = date.today()

        years = today.year - fecha_alta_simulada.year
        months = today.month - fecha_alta_simulada.month
        days = today.day - fecha_alta_simulada.day

        if days < 0:
            months -= 1
            prev_month = today.month - 1 if today.month > 1 else 12
            prev_year = today.year if today.month > 1 else today.year - 1
            days += calendar.monthrange(prev_year, prev_month)[1]

        if months < 0:
            years -= 1
            months += 12

        return (years, months, days)


class AltaAnterior(db.Model):
    __tablename__ = "altas_anteriores"

    id = db.Column(db.Integer, primary_key=True)
    hoja_id = db.Column(db.Integer, db.ForeignKey("hojas_servicio.id"))
    hoja = db.relationship("HojaServicio", back_populates="altas_anteriores")

    fecha_alta = db.Column(db.Date)
    registro_general = db.Column(db.Integer)
    registro_quinta = db.Column(db.Integer)
    fecha_baja = db.Column(db.Date)
    motivo_baja = db.Column(
        db.Enum(*MOTIVOS_BAJA, name="motivo_baja_enum"),
        nullable=True,
    )

    @property
    def total_dias(self):
        if self.fecha_alta and self.fecha_baja:
            return (self.fecha_baja - self.fecha_alta).days
        return None


class Asistencia(db.Model):
    __tablename__ = "asistencias"

    id = db.Column(db.Integer, primary_key=True)
    hoja_id = db.Column(db.Integer, db.ForeignKey("hojas_servicio.id"))
    hoja = db.relationship("HojaServicio", back_populates="asistencias")

    fecha = db.Column(db.Integer)  # Año
    total_actos_obligatorios = db.Column(db.Integer)
    total_asistencias = db.Column(db.Integer)


class PremioAsistencia(db.Model):
    __tablename__ = "premios_asistencia"

    id = db.Column(db.Integer, primary_key=True)
    hoja_id = db.Column(db.Integer, db.ForeignKey("hojas_servicio.id"))
    hoja = db.relationship("HojaServicio", back_populates="premios")

    # TODO: Premio: {5:80:5} -> 5, 10, 15, etc.
    premio = db.Column(db.Integer)
    fecha_obtencion = db.Column(db.Date)
    asistencias_sobrantes = db.Column(db.Integer)


class TipoCargo(db.Model):
    __tablename__ = "tipos_cargo"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(64), unique=True, nullable=False)
    categoria = db.Column(
        db.Enum(*CATEGORIAS_CARGO, name="categoria_cargo_enum"),
        nullable=False,
        default="Compañía",
    )
    orden = db.Column(db.Integer, default=0)

    def __repr__(self):
        return self.nombre


class Cargo(db.Model):
    __tablename__ = "cargos"

    id = db.Column(db.Integer, primary_key=True)
    hoja_id = db.Column(db.Integer, db.ForeignKey("hojas_servicio.id"))
    hoja = db.relationship("HojaServicio", back_populates="cargos")

    # TODO:
    #  Referencia al nombre del cargo (String) para flexibilidad histórica
    #  Opcional: Podríamos vincularlo a TipoCargo con FK,
    #  pero el requerimiento es modificar los cargos posibles.
    #  Si borramos un tipo de cargo, ¿queremos borrar el historial? Probablemente no.
    #  Por lo tanto, guardaremos el nombre como String, pero la UI lo sacará de TipoCargo.
    nombre_cargo = db.Column(db.String(64))

    fecha_inicio = db.Column(db.Date)
    fecha_termino = db.Column(db.Date, nullable=True)


class Operador(db.Model):
    __tablename__ = "operadores"

    id = db.Column(db.Integer, primary_key=True)
    hoja_id = db.Column(db.Integer, db.ForeignKey("hojas_servicio.id"))
    hoja = db.relationship("HojaServicio", back_populates="operadores")

    fecha_autorizacion = db.Column(db.Date)
    maquina = db.Column(db.String(64))  # TODO: relacionar con tabla de máquinas
    nivel = db.Column(db.String(20))
    # TODO: Niveles fijos?
    # TODO: (Maquinista, operador N1, Operador N2, Operador N3, Conductor)
    # TODO:¿Se es máquinista de la cía o de una máquina?
    comentario = db.Column(db.Text)


class Competencia(db.Model):
    __tablename__ = "competencias"

    id = db.Column(db.Integer, primary_key=True)
    hoja_id = db.Column(db.Integer, db.ForeignKey("hojas_servicio.id"))
    hoja = db.relationship("HojaServicio", back_populates="competencias")

    fecha = db.Column(db.Integer)
    nombre_competencia = db.Enum(*COMPETENCIAS, name="competencias_enum")
    # TODO: Lugar: {1, 2, 3, 4}
    lugar = db.Column(db.Integer)


class Curso(db.Model):
    __tablename__ = "cursos"

    id = db.Column(db.Integer, primary_key=True)
    hoja_id = db.Column(db.Integer, db.ForeignKey("hojas_servicio.id"))
    hoja = db.relationship("HojaServicio", back_populates="cursos")

    fecha = db.Column(db.Integer)  # Año
    nombre_curso = db.Column(db.String(128))


class NivelAcademico(db.Model):
    __tablename__ = "niveles_academicos"

    id = db.Column(db.Integer, primary_key=True)
    hoja_id = db.Column(db.Integer, db.ForeignKey("hojas_servicio.id"))
    hoja = db.relationship("HojaServicio", back_populates="niveles_academicos")

    fecha = db.Column(db.Integer)  # Año
    nivel = db.Enum(*NIVELES_ACADEMICOS, name="nivel_academico_enum")


class OtraAnotacion(db.Model):
    # Como Premio La Llave o Cuadro de Honor
    __tablename__ = "otras_anotaciones"

    id = db.Column(db.Integer, primary_key=True)
    hoja_id = db.Column(db.Integer, db.ForeignKey("hojas_servicio.id"))
    hoja = db.relationship("HojaServicio", back_populates="otras_anotaciones")

    fecha = db.Column(db.Integer)  # Año
    texto_anotacion = db.Column(db.String(128))
    comentario = db.Column(db.Text)
