from forms import AddGameForm, RegistrationForm, LoginForm, EditProfileForm
from models import Category, Game, User, admin_required
from ext import db
import os
import json
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import (
    login_user, login_required, logout_user, current_user
)
from werkzeug.utils import secure_filename
AVATAR_FOLDER = os.path.join("static", "avatars")


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
        flash("ბანერი უნდა იყოს 3-ზე ნაკლები MB.", "warning")
        return None
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    fname = secure_filename(storage.filename)
    storage.save(os.path.join(UPLOAD_FOLDER, fname))
    return fname


# ────────────────────────── PUBLIC PAGES ─────────────────────────
@bp.route("/")
def index():
    games_new = [
        {"title": "Elder Ring: Nightreign", "image": "images/cover1.jpg"},
        {"title": "Elder Scrolls IV: Oblivion (remastered)",
         "image": "images/cover2.png"},
        {"title": "Schedule I", "image": "images/cover3.jpg"},
    ]
    games_recommended = [
        {"title": "Hollow Knight", "image": "images/cover4normal.png"},
        {"title": "Deltarune", "image": "images/cover5.png"},
        {"title": "Outer Wilds", "image": "images/cover6.png"},
    ]
    genres = [
        {"title": "RPG", "image": "images/rpg-game.png"},
        {"title": "ACTION", "image": "images/action-movie.png"},
        {"title": "HORROR", "image": "images/horror.png"},
        {"title": "RACING", "image": "images/racing.png"},
        {"title": "FPS", "image": "images/fps.png"},
        {"title": "strategy", "image": "images/strategy.png"},
    ]
    return render_template(
        "index.html",
        new_games=games_new,
        recommended_games=games_recommended,
        genre_type=genres
    )


@bp.route("/categories")
def categories():
    all_categories = Category.query.all()
    categories = [
        {"name": "RPG", "slug": "rpg"},
        {"name": "SHOOTER", "slug": "shooter"},
        {"name": "HORROR", "slug": "horror"},
        {"name": "ACTION", "slug": "action"},
        {"name": "RACING", "slug": "racing"},
        {"name": "STRATEGY", "slug": "strategy"},
        {"name": "METROIDVANIA", "slug": "metroidvania"},
        {"name": "SPORTS", "slug": "sports"},
        {"name": "ROGUE-LIKE", "slug": "rogue-like"},
        {"name": "SIMULATION", "slug": "simulation"},
        {"name": "SCI-FI", "slug": "sci-fi"},
        {"name": "CASUAL", "slug": "casual"},
    ]

    for c in categories:
        if not Category.query.filter_by(slug=c["slug"]).first():
            db.session.add(Category(name=c["name"], slug=c["slug"]))
    db.session.commit()
    all_categories = Category.query.all()
    return render_template("categories.html", categories=all_categories)


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
    else:
        print(form.errors)
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


@bp.route("/profile/edit", methods=["GET", "POST"])
@login_required
def edit_profile():
    form = EditProfileForm(
        username=current_user.username,
        bio=getattr(current_user, "bio", "")
    )
    if form.validate_on_submit():
        # --- username & bio ---
        current_user.username = form.username.data
        current_user.bio = form.bio.data

        # --- avatar upload ---
        if form.avatar.data:
            fname = save_avatar(form.avatar.data)   # იმავე helper-ს ვიყენებთ
            if fname:
                current_user.avatar = fname

        # --- banner upload ---
        if form.banner.data:
            fname = save_banner(form.banner.data)
            if fname:
                current_user.banner = fname

        db.session.commit()
        flash("Profile updated ✨", "success")
        return redirect(url_for(".profile"))
    return render_template("edit_profile.html", form=form, user=current_user)


def save_avatar(storage):
    if not storage:
        return None
    ext_ok = storage.filename.rsplit(".", 1)[1].lower() in {
        "png", "jpg", "jpeg"}
    if not ext_ok:
        return None
    os.makedirs(AVATAR_FOLDER, exist_ok=True)
    fname = secure_filename(storage.filename)
    storage.save(os.path.join(AVATAR_FOLDER, fname))
    return fname


# ────────────────────────── ADDGAME ──────────────────────────────
@bp.route("/admin/add_game", methods=["GET", "POST"])
@admin_required
def add_game():
    form = AddGameForm()
    # Populate category choices
    form.category.choices = [(c.id, c.name)
                             for c in Category.query.order_by(Category.name).all()]

    if form.validate_on_submit():
        # Save files
        cover_filename = secure_filename(form.cover.data.filename)
        background_filename = secure_filename(
            form.background_image.data.filename)
        torrent_filename = secure_filename(form.torrent_file.data.filename)

        cover_path = os.path.join(
            current_app.root_path, 'static/covers', cover_filename)
        background_path = os.path.join(
            current_app.root_path, 'static/banners', background_filename)
        torrent_path = os.path.join(
            current_app.root_path, 'static/torrents', torrent_filename)

        # Ensure directories exist
        os.makedirs(os.path.dirname(cover_path), exist_ok=True)
        os.makedirs(os.path.dirname(background_path), exist_ok=True)
        os.makedirs(os.path.dirname(torrent_path), exist_ok=True)

        form.cover.data.save(cover_path)
        form.background_image.data.save(background_path)
        form.torrent_file.data.save(torrent_path)

        # Create game instance
        game = Game(
            title=form.title.data,
            description=form.description.data,
            cover='covers/' + cover_filename,
            background_image='banners/' + background_filename,
            torrent_file='torrents/' + torrent_filename,
            category_id=form.category.data
        )
        db.session.add(game)
        db.session.commit()
        flash("თამაში დაემატა!", "success")
        return redirect(url_for(".add_game"))

    return render_template("admin_add_game.html", form=form)


def save_cover(storage):
    """ჩამოტვირთული თამაშის ყდის სურათი ინახავს static/covers/ საქაღალდეში
       და აბრუნებს მხოლოდ ფაილის სახელს (fname)."""
    folder = os.path.join("static", "covers")
    os.makedirs(folder, exist_ok=True)          # თუ არ არსებობს - შექმნა
    fname = secure_filename(storage.filename)   # Unsafe სახელის გასაწმენდად
    storage.save(os.path.join(folder, fname))   # რეალურად ვწერთ დისკზე
    return fname


@bp.route("/category/<slug>")
def category_page(slug):
    print("Slug:", slug)
    category = Category.query.filter_by(slug=slug).first_or_404()
    print("Category:", category)
    games = Game.query.filter_by(category=category).all()
    print("Games:", games)
    return render_template("category.html", category=category, games=games)


@bp.route('/game/<int:game_id>')
def game_detail(game_id):
    game = Game.query.get_or_404(game_id)
    return render_template('game.html', game=game)
