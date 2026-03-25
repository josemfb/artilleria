from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError

from app.models import Usuario
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
