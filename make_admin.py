from app import create_app
from ext import db
from models import User

app = create_app()
with app.app_context():
    user = User.query.filter_by(username='Mathews').first()
    if user:
        user.is_admin = True  # Set to False to remove admin
        db.session.commit()
        print(f"{user.username} admin status is now {user.is_admin}")
    else:
        print("User not found")
