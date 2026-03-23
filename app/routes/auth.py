from urllib.parse import urlsplit

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user

from app.forms import LoginForm
from app.models import Usuario

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    form = LoginForm()
    if form.validate_on_submit():
        user = Usuario.query.filter_by(run=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("RUN o contraseña inválidos")
            return redirect(url_for("auth.login"))

        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get("next")
        if not next_page or urlsplit(next_page).netloc != "":
            next_page = url_for("main.index")
        return redirect(next_page)

    if form.username.errors:
        flash("RUN inválido")

    return render_template("login.html", title="Ingresar", form=form)


@auth_bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.index"))
