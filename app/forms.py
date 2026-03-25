from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    DateField,
    PasswordField,
    SelectField,
    StringField,
    SubmitField,
)
from wtforms.validators import DataRequired, Email, Optional, ValidationError

from app.models import Usuario
from app.models.hojas_servicio import CATEGORIAS, MOTIVOS_BAJA, TipoCargo
from app.utils import validate_and_format_run


class LoginForm(FlaskForm):
    username = StringField("RUN", validators=[DataRequired()])
    password = PasswordField("Contraseña", validators=[DataRequired()])
    remember_me = BooleanField("Recordarme")
    submit = SubmitField("Iniciar Sesión")

    def validate_username(self, username):
        try:
            username.data = validate_and_format_run(username.data)
        except ValueError as e:
            raise ValidationError(str(e))


class AddVolunteerForm(FlaskForm):
    username = StringField("RUN", validators=[DataRequired()])
    nombre = StringField("Nombres", validators=[DataRequired()])
    apellido1 = StringField("Apellido Paterno", validators=[DataRequired()])
    apellido2 = StringField("Apellido Materno", validators=[DataRequired()])
    password = PasswordField("Contraseña Provisoria", validators=[DataRequired()])
    submit = SubmitField("Registrar Voluntario")

    def validate_username(self, username):
        try:
            username.data = validate_and_format_run(username.data)
        except ValueError as e:
            raise ValidationError(str(e))

        if Usuario.query.filter_by(run=username.data).first():
            raise ValidationError("Ya existe un voluntario con este RUN.")


class EditVolunteerForm(FlaskForm):
    # Usuario fields
    nombre = StringField("Nombres", validators=[DataRequired()])
    apellido1 = StringField("Apellido Paterno", validators=[DataRequired()])
    apellido2 = StringField("Apellido Materno", validators=[DataRequired()])

    # HojaServicio fields
    fecha_nacimiento = DateField(
        "Fecha de Nacimiento", format="%Y-%m-%d", validators=[Optional()]
    )
    ocupacion = StringField("Ocupación")
    direccion = StringField("Dirección")
    telefono = StringField("Teléfono")
    email = StringField("Email", validators=[Optional(), Email()])

    # Institutional fields
    fecha_alta = DateField("Fecha de Alta", format="%Y-%m-%d", validators=[Optional()])
    categoria = SelectField(
        "Categoría", choices=[(c, c) for c in CATEGORIAS], validators=[Optional()]
    )

    # Baja fields
    fecha_baja = DateField("Fecha de Baja", format="%Y-%m-%d", validators=[Optional()])
    motivo_baja = SelectField(
        "Motivo de Baja",
        choices=[("", "Seleccione un motivo")] + [(m, m) for m in MOTIVOS_BAJA],
        validators=[Optional()],
    )
    submit = SubmitField("Guardar Cambios")


class CargoForm(FlaskForm):
    nombre_cargo = SelectField("Cargo", validators=[DataRequired()])
    fecha_inicio = DateField(
        "Fecha de Inicio", format="%Y-%m-%d", validators=[DataRequired()]
    )
    fecha_termino = DateField(
        "Fecha de Término", format="%Y-%m-%d", validators=[Optional()]
    )
    submit = SubmitField("Guardar Cargo")

    def __init__(self, *args, **kwargs):
        super(CargoForm, self).__init__(*args, **kwargs)
        self.nombre_cargo.choices = [("", "Seleccione un cargo")] + [
            (tc.nombre, tc.nombre)
            for tc in TipoCargo.query.order_by(TipoCargo.orden).all()
        ]
