import json
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from ext import db, login_manager


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30),  unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    pwd_hash = db.Column(db.String(128), nullable=False)
    banner = db.Column(db.String(120))
    games = db.Column(db.Text, default=json.dumps([]))

    # helpers
    def set_password(self, pwd):  self.pwd_hash = generate_password_hash(pwd)
    def check_password(self, pwd): return check_password_hash(
        self.pwd_hash, pwd)

    def games_list(self): return json.loads(self.games or "[]")


@login_manager.user_loader
def load_user(uid):
    return User.query.get(int(uid))
