from app import app
from app import db
from app.models import Users


def create_user(id, username, email, password, admin=False):
    user = Users(id=id, username=username, email=email, is_admin=admin)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()


if __name__ == "__main__":
    create_user(
        id=0,
        username="test-admin",
        email="test-admin@peaksandtroughs.com",
        password="test321",
        admin=True,
    )
    create_user(
        id=1, username="test-user", email="test-user@peaksandtroughs.com", password="test123"
    )
