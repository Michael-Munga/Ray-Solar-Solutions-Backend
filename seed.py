from models import db, User
from app import app

def seed_admin():
    with app.app_context():
        admin_email = "hopeyunia@gmail.com"
        admin_password = "admin123"
        existing_admin = User.query.filter_by(email=admin_email).first()
        if existing_admin:
            print("Admin user already exists.")
            return
        admin = User(
            first_name="Admin",
            last_name="User",
            email=admin_email,
            role="admin",
            is_approved=True
        )
        admin.set_password(admin_password)
        db.session.add(admin)
        db.session.commit()
        print(f"Admin user created with email: {admin_email} and password: {admin_password}")

if __name__ == "__main__":
    seed_admin()
