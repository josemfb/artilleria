import click
from flask.cli import with_appcontext

from app import db
from app.models import Usuario


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

    if Usuario.query.filter_by(run=username).first():
        click.echo(f"User {username} already exists.")
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
    db.create_all()
    click.echo("Base de datos inicializada.")
