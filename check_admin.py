from app import app, db
from models import User

with app.app_context():
    db.create_all()  # Ensure tables are created
    admin = User.query.filter_by(email="admin@gmail.com").first()
    if admin:
        print(f"Admin user found: {admin.email}, role: {admin.role}")
    else:
        print("Admin user not found.")
