from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError

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
