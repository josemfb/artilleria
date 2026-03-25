from datetime import date

from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from app import db
from app.forms import AddVolunteerForm
from app.models import HojaServicio, Usuario

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
@login_required
def index():
    return render_template("base.html")


@main_bp.route("/add_user", methods=["GET", "POST"])
@login_required
def add_user():
    if not current_user.has_permission("volunteers.add_volunteer"):
        flash("No tienes permiso para realizar esta acción.")
        return redirect(url_for("volunteers.index"))

    form = AddVolunteerForm()
    if form.validate_on_submit():
        user = Usuario(
            run=form.username.data,
            nombre=form.nombre.data,
            apellido1=form.apellido1.data,
            apellido2=form.apellido2.data,
        )
        user.set_password(form.password.data)

        # Create default HojaServicio so the user appears in the volunteer list
        profile = HojaServicio(user=user, fecha_alta=date.today())

        db.session.add(user)
        db.session.add(profile)
        db.session.commit()
        flash(f"Voluntario {user.nombre} {user.apellido1} agregado correctamente.")
        return redirect(url_for("volunteers.index"))

    return render_template("add_user.html", form=form)
