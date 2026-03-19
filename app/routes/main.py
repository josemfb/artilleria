from flask import Blueprint, render_template, flash, redirect, url_for
from app import db
from app.models import Usuario

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('base.html')

@main_bp.route('/add_user', methods=['GET', 'POST'])
def add_user():
    ...
