from flask_migrate import Migrate
from flask import Flask, render_template
from ext import db, login_manager, csrf
from routes import bp
import os


def create_app():
    app = Flask(__name__)
    app.config.update(
        SECRET_KEY="replace-with-random-string",

        SQLALCHEMY_DATABASE_URI="sqlite:///site.db",

        MAX_CONTENT_LENGTH=20 * 1024 * 1024
    )

    # ───── Extensions
    db.init_app(app)
    migrate = Migrate(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)

    # ───── Blueprints
    app.register_blueprint(bp)

    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/site.db'

    return app


# ───── CLI / python app.py ─────
if __name__ == "__main__":

    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)
