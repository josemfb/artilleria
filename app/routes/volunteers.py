from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app import db
from app.forms import CargoForm, EditVolunteerForm, InlineEditPersonalDataForm
from app.models import Cargo, Usuario

volunteers_bp = Blueprint("volunteers", __name__, url_prefix="/voluntarios")


@volunteers_bp.route("/")
@login_required
def index():
    sort_by = request.args.get("sort_by", "apellido")
    order = request.args.get("order", "asc")
    reverse = order == "desc"

    users = Usuario.query.join(Usuario.profile).all()

    def get_sort_key(user):
        profile = user.profile

        if sort_by == "apellido":
            # Sort by Last Name, then Second Last Name, then First Name
            return (user.apellido1 or "", user.apellido2 or "", user.nombre or "")
        elif sort_by == "categoria":
            return profile.categoria if profile and profile.categoria else ""
        elif sort_by == "cargo":
            return profile.cargo_actual if profile and profile.cargo_actual else ""
        elif sort_by == "antiguedad":
            # Tuple (years, months, days).
            # Default to (-1, -1, -1) for those without data so they appear
            # at the beginning (asc) or end (desc) appropriately.
            if profile and profile.fecha_alta:
                return profile.antiguedad
            return (-1, -1, -1)

        # Fallback to default
        return (user.apellido1 or "", user.apellido2 or "", user.nombre or "")

    users.sort(key=get_sort_key, reverse=reverse)

    if request.headers.get("HX-Request"):
        return render_template(
            "volunteers/list.html",
            users=users,
            current_sort=sort_by,
            current_order=order,
        )

    return render_template(
        "volunteers/list.html",
        users=users,
        current_sort=sort_by,
        current_order=order,
    )


@volunteers_bp.route("/<int:user_id>")
@login_required
def details(user_id):
    user = db.session.get(Usuario, user_id)
    if not user:
        flash("Voluntario no encontrado.", "error")
        return redirect(url_for("volunteers.index"))

    show_full = current_user.has_permission("volunteers.view_details")

    # Create inline edit form for personal data
    inline_form = InlineEditPersonalDataForm()

    if request.headers.get("HX-Request"):
        return render_template(
            "volunteers/details.html",
            user=user,
            show_full=show_full,
            inline_form=inline_form,
        )
    return render_template(
        "volunteers/details.html",
        user=user,
        show_full=show_full,
        inline_form=inline_form,
    )


@volunteers_bp.route("/edit/<int:user_id>", methods=["GET", "POST"])
@login_required
def edit_volunteer(user_id):
    if not current_user.has_permission("volunteers.add_volunteer"):
        flash("No tienes permiso para realizar esta acción.", "error")
        return redirect(url_for("volunteers.details", user_id=user_id))

    user = db.session.get(Usuario, user_id)
    if not user:
        flash("Voluntario no encontrado.", "error")
        return redirect(url_for("volunteers.index"))

    form = EditVolunteerForm()

    if form.validate_on_submit():
        # Update Usuario
        user.nombre = form.nombre.data
        user.apellido1 = form.apellido1.data
        user.apellido2 = form.apellido2.data

        # Update HojaServicio (user.profile is created on user creation, so it exists)
        profile = user.profile
        profile.fecha_nacimiento = form.fecha_nacimiento.data
        profile.ocupacion = form.ocupacion.data
        profile.direccion = form.direccion.data
        profile.telefono = form.telefono.data
        profile.email = form.email.data
        profile.fecha_alta = form.fecha_alta.data
        profile.categoria = form.categoria.data
        profile.fecha_baja = form.fecha_baja.data
        profile.motivo_baja = form.motivo_baja.data or None

        db.session.commit()
        flash("Información actualizada correctamente.", "success")

        if request.headers.get("HX-Request"):
            return render_template("volunteers/details.html", user=user, show_full=True)

        return redirect(url_for("volunteers.details", user_id=user.id))

    # Pre-populate form
    if request.method == "GET":
        form.nombre.data = user.nombre
        form.apellido1.data = user.apellido1
        form.apellido2.data = user.apellido2

        if user.profile:
            form.fecha_nacimiento.data = user.profile.fecha_nacimiento
            form.ocupacion.data = user.profile.ocupacion
            form.direccion.data = user.profile.direccion
            form.telefono.data = user.profile.telefono
            form.email.data = user.profile.email
            form.fecha_alta.data = user.profile.fecha_alta
            form.categoria.data = user.profile.categoria
            form.fecha_baja.data = user.profile.fecha_baja
            form.motivo_baja.data = user.profile.motivo_baja

    if request.headers.get("HX-Request"):
        return render_template("volunteers/edit.html", form=form, user=user)

    return render_template("volunteers/edit.html", form=form, user=user)


@volunteers_bp.route("/<int:user_id>/inline-edit-personal-data", methods=["POST"])
@login_required
def inline_edit_personal_data(user_id):
    if not current_user.has_permission("volunteers.add_volunteer"):
        if request.headers.get("HX-Request"):
            return (
                jsonify({"error": "No tienes permiso para realizar esta acción."}),
                403,
            )
        flash("No tienes permiso para realizar esta acción.", "error")
        return redirect(url_for("volunteers.details", user_id=user_id))

    user = db.session.get(Usuario, user_id)
    if not user:
        if request.headers.get("HX-Request"):
            return jsonify({"error": "Voluntario no encontrado."}), 404
        flash("Voluntario no encontrado.", "error")
        return redirect(url_for("volunteers.index"))

    form = InlineEditPersonalDataForm()

    if form.validate_on_submit():
        # Update only personal data fields (not RUN)
        profile = user.profile
        profile.fecha_nacimiento = form.fecha_nacimiento.data
        profile.ocupacion = form.ocupacion.data
        profile.direccion = form.direccion.data
        profile.telefono = form.telefono.data
        profile.email = form.email.data
        profile.fecha_alta = form.fecha_alta.data

        db.session.commit()
        flash("Datos personales actualizados correctamente.", "success")

        # Handle HTMX requests
        if request.headers.get("HX-Request"):
            # Return updated data for the display fields
            response_data = {
                "fecha_nacimiento": (
                    profile.fecha_nacimiento.strftime("%d-%m-%Y")
                    if profile.fecha_nacimiento
                    else "-"
                ),
                "ocupacion": profile.ocupacion or "-",
                "telefono": profile.telefono or "-",
                "email": profile.email or "-",
                "direccion": profile.direccion or "-",
                "fecha_alta": (
                    profile.fecha_alta.strftime("%d-%m-%Y")
                    if profile.fecha_alta
                    else "-"
                ),
            }
            return jsonify({"success": True, "data": response_data})

        return redirect(url_for("volunteers.details", user_id=user.id))

    else:
        # Form validation failed
        if request.headers.get("HX-Request"):
            return (
                jsonify(
                    {
                        "error": "Por favor, corrija los errores en el formulario.",
                        "errors": form.errors,
                    }
                ),
                400,
            )

        # For non-HTMX requests, render the edit page with errors
        return render_template(
            "volunteers/details.html",
            user=user,
            inline_form=form,
            show_full=current_user.has_permission("volunteers.view_details"),
        )


@volunteers_bp.route("/<int:user_id>/cargos/add", methods=["GET", "POST"])
@login_required
def add_cargo(user_id):
    if not current_user.has_permission("volunteers.add_volunteer"):
        flash("No tienes permiso para realizar esta acción.")
        return redirect(url_for("volunteers.details", user_id=user_id))

    # Needs to find user first
    user = db.session.get(Usuario, user_id)
    if not user:
        flash("Voluntario no encontrado.", "error")
        return redirect(url_for("volunteers.index"))

    form = CargoForm()
    if form.validate_on_submit():
        new_cargo = Cargo(
            hoja_id=user.profile.id,
            nombre_cargo=form.nombre_cargo.data,
            fecha_inicio=form.fecha_inicio.data,
            fecha_termino=form.fecha_termino.data or None,
        )
        db.session.add(new_cargo)
        db.session.commit()
        flash("Cargo agregado correctamente.", "success")

        if request.headers.get("HX-Request"):
            # Re-render edit page content to show new cargo
            edit_form = EditVolunteerForm()
            # We need to re-populate the edit form data so it doesn't show empty fields
            edit_form.nombre.data = user.nombre
            edit_form.apellido1.data = user.apellido1
            edit_form.apellido2.data = user.apellido2
            if user.profile:
                edit_form.fecha_nacimiento.data = user.profile.fecha_nacimiento
                edit_form.ocupacion.data = user.profile.ocupacion
                edit_form.direccion.data = user.profile.direccion
                edit_form.telefono.data = user.profile.telefono
                edit_form.email.data = user.profile.email
                edit_form.fecha_alta.data = user.profile.fecha_alta
                edit_form.categoria.data = user.profile.categoria
                edit_form.fecha_baja.data = user.profile.fecha_baja
                edit_form.motivo_baja.data = user.profile.motivo_baja
            return render_template("volunteers/edit.html", form=edit_form, user=user)

        return redirect(url_for("volunteers.edit_volunteer", user_id=user_id))

    if request.headers.get("HX-Request"):
        return render_template(
            "volunteers/manage_cargo.html", form=form, title="Añadir Cargo", user=user
        )

    return render_template(
        "volunteers/manage_cargo.html", form=form, title="Añadir Cargo", user=user
    )


@volunteers_bp.route("/cargos/edit/<int:cargo_id>", methods=["GET", "POST"])
@login_required
def edit_cargo(cargo_id):
    if not current_user.has_permission("volunteers.add_volunteer"):
        flash("No tienes permiso para realizar esta acción.")
        return redirect(url_for("volunteers.index"))

    cargo = db.session.get(Cargo, cargo_id)
    if not cargo:
        flash("Cargo no encontrado.")
        return redirect(url_for("volunteers.index"))

    user = cargo.hoja.user
    form = CargoForm()

    if form.validate_on_submit():
        cargo.nombre_cargo = form.nombre_cargo.data
        cargo.fecha_inicio = form.fecha_inicio.data
        cargo.fecha_termino = form.fecha_termino.data or None
        db.session.commit()
        flash("Cargo actualizado correctamente.", "success")

        if request.headers.get("HX-Request"):
            # Re-render edit page content
            edit_form = EditVolunteerForm()
            edit_form.nombre.data = user.nombre
            edit_form.apellido1.data = user.apellido1
            edit_form.apellido2.data = user.apellido2
            if user.profile:
                edit_form.fecha_nacimiento.data = user.profile.fecha_nacimiento
                edit_form.ocupacion.data = user.profile.ocupacion
                edit_form.direccion.data = user.profile.direccion
                edit_form.telefono.data = user.profile.telefono
                edit_form.email.data = user.profile.email
                edit_form.fecha_alta.data = user.profile.fecha_alta
                edit_form.categoria.data = user.profile.categoria
                edit_form.fecha_baja.data = user.profile.fecha_baja
                edit_form.motivo_baja.data = user.profile.motivo_baja
            return render_template("volunteers/edit.html", form=edit_form, user=user)

        return redirect(url_for("volunteers.edit_volunteer", user_id=user.id))

    elif request.method == "GET":
        form.nombre_cargo.data = cargo.nombre_cargo
        form.fecha_inicio.data = cargo.fecha_inicio
        form.fecha_termino.data = cargo.fecha_termino

    if request.headers.get("HX-Request"):
        return render_template(
            "volunteers/manage_cargo.html", form=form, title="Editar Cargo", user=user
        )

    return render_template(
        "volunteers/manage_cargo.html", form=form, title="Editar Cargo", user=user
    )


@volunteers_bp.route("/cargos/delete/<int:cargo_id>", methods=["POST"])
@login_required
def delete_cargo(cargo_id):
    if not current_user.has_permission("volunteers.add_volunteer"):
        flash("No tienes permiso para realizar esta acción.")
        return redirect(url_for("volunteers.index"))

    cargo = db.session.get(Cargo, cargo_id)
    if not cargo:
        flash("Cargo no encontrado.")
        return redirect(request.referrer or url_for("volunteers.index"))

    user_id = cargo.hoja.user_id
    user = cargo.hoja.user
    db.session.delete(cargo)
    db.session.commit()
    flash("Cargo eliminado correctamente.", "success")

    if request.headers.get("HX-Request"):
        # Re-render edit page content
        edit_form = EditVolunteerForm()
        edit_form.nombre.data = user.nombre
        edit_form.apellido1.data = user.apellido1
        edit_form.apellido2.data = user.apellido2
        if user.profile:
            edit_form.fecha_nacimiento.data = user.profile.fecha_nacimiento
            edit_form.ocupacion.data = user.profile.ocupacion
            edit_form.direccion.data = user.profile.direccion
            edit_form.telefono.data = user.profile.telefono
            edit_form.email.data = user.profile.email
            edit_form.fecha_alta.data = user.profile.fecha_alta
            edit_form.categoria.data = user.profile.categoria
            edit_form.fecha_baja.data = user.profile.fecha_baja
            edit_form.motivo_baja.data = user.profile.motivo_baja
        return render_template("volunteers/edit.html", form=edit_form, user=user)

    return redirect(url_for("volunteers.edit_volunteer", user_id=user_id))
