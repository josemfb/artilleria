from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required
from sqlalchemy import func

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
                max_orden = db.session.query(func.max(TipoCargo.orden)).scalar()
                # If table is empty, max_orden is None, so new orden is 1 (or 0)
                nuevo_orden = (max_orden if max_orden is not None else -1) + 1
                db.session.add(TipoCargo(nombre=nuevo_cargo, orden=nuevo_orden))
                db.session.commit()
                flash("Cargo agregado.")
        return redirect(url_for("settings.cargos"))

    cargos = TipoCargo.query.order_by(TipoCargo.orden).all()
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


@settings_bp.route("/cargos/move/<int:id>/<direction>", methods=["POST"])
@login_required
def move_cargo(id, direction):
    cargo = db.session.get(TipoCargo, id)
    if not cargo:
        return redirect(url_for("settings.cargos"))

    target_cargo = None
    if direction == "up":
        target_cargo = (
            TipoCargo.query.filter(TipoCargo.orden < cargo.orden)
            .order_by(TipoCargo.orden.desc())
            .first()
        )
    elif direction == "down":
        target_cargo = (
            TipoCargo.query.filter(TipoCargo.orden > cargo.orden)
            .order_by(TipoCargo.orden.asc())
            .first()
        )

    if target_cargo:
        # Swap orden
        cargo.orden, target_cargo.orden = target_cargo.orden, cargo.orden
        db.session.add(cargo)
        db.session.add(target_cargo)
        db.session.commit()

    return redirect(url_for("settings.cargos"))


@settings_bp.route("/cargos/edit/<int:id>", methods=["POST"])
@login_required
def edit_cargo(id):
    cargo = db.session.get(TipoCargo, id)
    nuevo_nombre = request.form.get("nombre")
    if cargo and nuevo_nombre:
        cargo.nombre = nuevo_nombre
        db.session.commit()
        flash("Cargo actualizado.")
    return redirect(url_for("settings.cargos"))
