from flask import Blueprint, render_template, request
from flask_login import login_required

from app.models import HojaServicio, Usuario

volunteers_bp = Blueprint("volunteers", __name__, url_prefix="/voluntarios")


@volunteers_bp.route("/")
@login_required
def index():
    sort_by = request.args.get("sort_by", "apellido")
    order = request.args.get("order", "asc")
    reverse = order == "desc"

    users = Usuario.query.join(HojaServicio).all()

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

    return render_template(
        "volunteers/list.html",
        users=users,
        current_sort=sort_by,
        current_order=order,
    )
