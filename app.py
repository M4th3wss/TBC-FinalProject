from flask_migrate import Migrate
from flask import Flask, render_template
from ext import db, login_manager, csrf
from routes import bp
import os


def create_app():
    app = Flask(__name__)
    app.config.update(
        SECRET_KEY="123123",

        SQLALCHEMY_DATABASE_URI="sqlite:///site.db",

        MAX_CONTENT_LENGTH=20 * 1024 * 1024
    )

    db.init_app(app)
    migrate = Migrate(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)

    app.register_blueprint(bp)

    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/site.db'

    return app


if __name__ == "__main__":

    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)
