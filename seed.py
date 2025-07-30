from app import db, app  
from models import User 

def seed_admins():
    with app.app_context():
        

        admin1 = User(
            first_name="Alice",
            last_name="Anderson",
            email="alice.admin@example.com",
            role="admin",
            is_approved=True
        )
        admin1.set_password("SecurePassword123!")

        admin2 = User(
            first_name="Bob",
            last_name="Bennett",
            email="bob.admin@example.com",
            role="admin",
            is_approved=True
        )
        admin2.set_password("AnotherSecurePwd456!")

        db.session.add_all([admin1, admin2])
        db.session.commit()
        print("Admin users seeded successfully.")

if __name__ == '__main__':
    seed_admins()
