from flask import Blueprint, render_template
from flask_login import login_required

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
@login_required
def index():
    return render_template("base.html")


@main_bp.route("/add_user", methods=["GET", "POST"])
def add_user(): ...
