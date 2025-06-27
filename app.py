from flask import Flask, render_template
from ext import db, login_manager, csrf
from routes import bp   # blueprint-ი, უკვე გამზადებული


def create_app():
    app = Flask(__name__)
    app.config.update(
        SECRET_KEY="replace-with-random-string",
        SQLALCHEMY_DATABASE_URI="sqlite:///site.db",
        MAX_CONTENT_LENGTH=3 * 1024 * 1024
    )

    # ───── Extensions
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    # ───── Blueprints
    app.register_blueprint(bp)

    # ───── Home route (genres/new/recommended) ─────
    @app.route("/")
    def home():
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

    return app


# ───── CLI / python app.py ─────
if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)
