from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app import db
from app.models.hojas_servicio import TipoCargo

settings_bp = Blueprint("settings", __name__, url_prefix="/settings")

@settings_bp.route("/cargos", methods=["GET", "POST"])
@login_required
def cargos():
    if request.method == "POST":
        nuevo_cargo = request.form.get("nombre")
        if nuevo_cargo:
            if TipoCargo.query.filter_by(nombre=nuevo_cargo).first():
                flash("El cargo ya existe.")
            else:
                db.session.add(TipoCargo(nombre=nuevo_cargo))
                db.session.commit()
                flash("Cargo agregado.")
        return redirect(url_for("settings.cargos"))
    
    cargos = TipoCargo.query.all()
    return render_template("settings/cargos.html", cargos=cargos)

@settings_bp.route("/cargos/delete/<int:id>", methods=["POST"])
@login_required
def delete_cargo(id):
    cargo = db.session.get(TipoCargo, id)
    if cargo:
        db.session.delete(cargo)
        db.session.commit()
        flash("Cargo eliminado.")
    return redirect(url_for("settings.cargos"))
