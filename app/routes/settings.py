from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy import func

from app import db
from app.models import RolePermission, TipoCargo
from app.models.hojas_servicio import CATEGORIAS_CARGO
from app.permissions import SYSTEM_PERMISSIONS

settings_bp = Blueprint("settings", __name__, url_prefix="/settings")


@settings_bp.before_request
def restrict_to_admins():
    if not current_user.is_authenticated or not current_user.is_admin:
        flash("No tienes permiso para acceder a esta sección.")
        return redirect(url_for("main.index"))


@settings_bp.route("/cargos", methods=["GET", "POST"])
@login_required
def cargos():
    if request.method == "POST":
        nuevo_cargo = request.form.get("nombre")
        nueva_categoria = request.form.get("categoria")
        if nuevo_cargo and nueva_categoria:
            # Check if exists
            exists = TipoCargo.query.filter_by(nombre=nuevo_cargo).first()
            if exists:
                flash("El cargo ya existe.", "error")
            else:
                max_orden = db.session.query(func.max(TipoCargo.orden)).scalar()
                # If table is empty, max_orden is None, so new orden is 1 (or 0)
                nuevo_orden = (max_orden if max_orden is not None else -1) + 1
                new_cargo = TipoCargo(
                    nombre=nuevo_cargo, categoria=nueva_categoria, orden=nuevo_orden
                )
                db.session.add(new_cargo)
                db.session.commit()
                flash("Cargo agregado.", "success")
        
        return redirect(url_for("settings.cargos"))

    cargos = TipoCargo.query.order_by(TipoCargo.orden).all()
    if request.headers.get("HX-Request"):
        return render_template(
             "settings/cargos.html", cargos=cargos, categorias=CATEGORIAS_CARGO
        )
    return render_template(
        "settings/cargos.html", cargos=cargos, categorias=CATEGORIAS_CARGO
    )


@settings_bp.route("/cargos/delete/<int:id>", methods=["POST"])
@login_required
def delete_cargo(id):
    cargo = db.session.get(TipoCargo, id)
    if cargo:
        db.session.delete(cargo)
        db.session.commit()
        flash("Cargo eliminado.", "success")
    
    if request.headers.get("HX-Request"):
        cargos = TipoCargo.query.order_by(TipoCargo.orden).all()
        return render_template(
            "settings/cargos.html", cargos=cargos, categorias=CATEGORIAS_CARGO
        )

    return redirect(url_for("settings.cargos"))


@settings_bp.route("/cargos/move/<int:id>/<direction>", methods=["POST"])
@login_required
def move_cargo(id, direction):
    cargo = db.session.get(TipoCargo, id)
    if not cargo:
        if request.headers.get("HX-Request"):
            cargos = TipoCargo.query.order_by(TipoCargo.orden).all()
            return render_template(
                "settings/cargos.html", cargos=cargos, categorias=CATEGORIAS_CARGO
            )
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
    
    if request.headers.get("HX-Request"):
        cargos = TipoCargo.query.order_by(TipoCargo.orden).all()
        return render_template(
            "settings/cargos.html", cargos=cargos, categorias=CATEGORIAS_CARGO
        )

    return redirect(url_for("settings.cargos"))


@settings_bp.route("/cargos/edit/<int:id>", methods=["POST"])
@login_required
def edit_cargo(id):
    cargo = db.session.get(TipoCargo, id)
    nuevo_nombre = request.form.get("nombre")
    nueva_categoria = request.form.get("categoria")
    if cargo and nuevo_nombre and nueva_categoria:
        cargo.nombre = nuevo_nombre
        cargo.categoria = nueva_categoria
        db.session.commit()
        flash("Cargo actualizado.", "success")
    
    if request.headers.get("HX-Request"):
        cargos = TipoCargo.query.order_by(TipoCargo.orden).all()
        return render_template(
            "settings/cargos.html", cargos=cargos, categorias=CATEGORIAS_CARGO
        )

    return redirect(url_for("settings.cargos"))


@settings_bp.route("/permissions", methods=["GET", "POST"])
@login_required
def permissions():
    cargos = (
        TipoCargo.query.filter_by(categoria="Compañía").order_by(TipoCargo.orden).all()
    )

    # Determine which cargo is selected (None = Default/No Rank)
    selected_cargo_id = request.args.get("cargo_id", type=int)

    # If no ID provided or ID is 0 (old default), select the first available cargo
    if (not selected_cargo_id or selected_cargo_id == 0) and cargos:
        selected_cargo_id = cargos[0].id

    selected_cargo = (
        db.session.get(TipoCargo, selected_cargo_id) if selected_cargo_id else None
    )

    if request.method == "POST":
        # Clear existing permissions for this scope
        RolePermission.query.filter_by(tipo_cargo_id=selected_cargo_id).delete()

        # Add new permissions
        # Form keys are like "perm_volunteers.view"
        for key in request.form:
            if key.startswith("perm_"):
                perm_code = key.replace("perm_", "")
                new_perm = RolePermission(
                    tipo_cargo_id=selected_cargo_id, permission=perm_code
                )
                db.session.add(new_perm)

        db.session.commit()
        flash("Permisos actualizados correctamente.", "success")
        
        # When using HTMX, we just want to re-render the page content with updated state
        if request.headers.get("HX-Request"):
            active_perms = [
                p.permission
                for p in RolePermission.query.filter_by(tipo_cargo_id=selected_cargo_id).all()
            ]
            return render_template(
                "settings/permissions.html",
                cargos=cargos,
                system_permissions=SYSTEM_PERMISSIONS,
                selected_cargo=selected_cargo,
                active_perms=active_perms,
            )

        return redirect(url_for("settings.permissions", cargo_id=selected_cargo_id))

    # Get active permissions for the selected scope to pre-fill checkboxes
    active_perms = [
        p.permission
        for p in RolePermission.query.filter_by(tipo_cargo_id=selected_cargo_id).all()
    ]
    
    if request.headers.get("HX-Request"):
        return render_template(
            "settings/permissions.html",
            cargos=cargos,
            system_permissions=SYSTEM_PERMISSIONS,
            selected_cargo=selected_cargo,
            active_perms=active_perms,
        )

    return render_template(
        "settings/permissions.html",
        cargos=cargos,
        system_permissions=SYSTEM_PERMISSIONS,
        selected_cargo=selected_cargo,
        active_perms=active_perms,
    )
