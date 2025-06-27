import os
import json
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import (
    login_user, login_required, logout_user, current_user
)
from werkzeug.utils import secure_filename

from ext import db
from models import User
from forms import RegistrationForm, LoginForm

bp = Blueprint("main", __name__)

UPLOAD_FOLDER = os.path.join("static", "banners")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
MAX_MB = 3


def allowed_file(fname):
    return "." in fname and fname.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def save_banner(storage):
    if not storage:
        return None
    if not allowed_file(storage.filename):
        flash("ფაილის ფორმატი არასწორია (PNG/JPG).", "warning")
        return None
    if storage.content_length and storage.content_length > MAX_MB * 1024 * 1024:
        flash("ბანერი უნდა იყოს ≤3 MB.", "warning")
        return None
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    fname = secure_filename(storage.filename)
    storage.save(os.path.join(UPLOAD_FOLDER, fname))
    return fname


# ────────────────────────── PUBLIC PAGES ─────────────────────────
@bp.route("/")
def index():
    return render_template("index.html")


@bp.route("/categories")
def categories():
    return render_template("categories.html")


# ────────────────────────── AUTH ─────────────────────────────────
@bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for(".profile"))

    form = RegistrationForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            flash("Username უკვე დაკავებულია!", "danger")
            return render_template("register.html", form=form)

        user = User(
            username=form.username.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        user.banner = save_banner(form.banner.data)
        user.games = json.dumps(["Hollow Knight"])
        db.session.add(user)
        db.session.commit()

        login_user(user)
        flash("Შესვლა წარმატებულია", "success")
        return redirect(url_for(".profile"))
    return render_template("register.html", form=form)


@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for(".profile"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash("Logged in!", "success")
            return redirect(url_for(".profile"))
        flash("Უწორი მონაცემები.", "danger")
    return render_template("login.html", form=form)


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("გაითიშე წარმატებით.", "info")
    return redirect(url_for(".index"))


# ────────────────────────── PROFILE ──────────────────────────────
@bp.route("/profile")
@login_required
def profile():
    return render_template("profile.html", user=current_user)
