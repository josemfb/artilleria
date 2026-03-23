import os
import click
from flask import current_app
from flask.cli import with_appcontext

from app import db
from app.models import Usuario
from app.utils import validate_and_format_run


@click.command("create-admin")
@click.option("--username", prompt="Username", help="RUN.")
@click.option(
    "--password",
    prompt=True,
    hide_input=True,
    confirmation_prompt=True,
    help="Contraseña.",
)
@click.option("--nombre", prompt=True, help="Nombre.")
@click.option(
    "--apellido1",
    prompt=True,
    help="Primer apellido.",
)
@click.option(
    "--apellido2",
    prompt=True,
    help="Segundo apellido.",
)
@with_appcontext
def create_admin(username, password, nombre, apellido1, apellido2):
    """Create an external admin user."""

    try:
        username = validate_and_format_run(username)
    except ValueError as e:
        click.echo(f"Error: {e}")
        return

    if Usuario.query.filter_by(run=username).first():
        click.echo(f"Usuario {username} ya existe.")
        return

    # Create User without HojaServicio (Not a volunteer)
    user = Usuario(
        run=username, nombre=nombre, apellido1=apellido1, apellido2=apellido2
    )
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    click.echo(f"Usuario {username} creado.")


@click.command("init-db")
@with_appcontext
def init_db():
    """Crear las tablas de la base de datos."""
    db_url = current_app.config.get("SQLALCHEMY_DATABASE_URI")
    if db_url and db_url.startswith("sqlite:///"):
        path = db_url.replace("sqlite:///", "", 1)
        directory = os.path.dirname(path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
    db.create_all()
    click.echo("Base de datos inicializada.")
