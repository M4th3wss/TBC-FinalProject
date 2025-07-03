# models.py
import json
from functools import wraps
from flask import abort
from flask_login import UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from ext import db, login_manager


# ─────────────────── USER ───────────────────
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30),  unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    pwd_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=True)
    banner = db.Column(db.String(120))
    avatar = db.Column(db.String(120))
    bio = db.Column(db.Text)
    games = db.Column(db.Text, default=json.dumps([]))

    def set_password(self, pwd):
        self.pwd_hash = generate_password_hash(pwd)

    def check_password(self, pwd):
        return check_password_hash(self.pwd_hash, pwd)

    def games_list(self):
        try:
            return json.loads(self.games or "[]")
        except Exception:
            return []


# ─────────────────── CATEGORY & GAME ───────────────────
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=True, nullable=False)
    slug = db.Column(db.String(40), unique=True, nullable=False)


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(250), nullable=False)
    publisher = db.Column(db.String(250), nullable=False)
    release_date = db.Column(db.String(250), nullable=False)

    cover = db.Column(db.String(120), nullable=False)
    background_image = db.Column(db.String(120), nullable=False)
    torrent_file = db.Column(db.String(120), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey(
        'category.id'), nullable=False)
    category = db.relationship(
        'Category', backref=db.backref('games', lazy=True))


# ─────────────────── LOGIN ───────────────────
@login_manager.user_loader
def load_user(uid):
    return User.query.get(int(uid))


# ─────────────────── ADMIN DECORATOR ───────────────────
def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not (current_user.is_authenticated and current_user.is_admin):
            return abort(403)
        return f(*args, **kwargs)
    return wrapper
