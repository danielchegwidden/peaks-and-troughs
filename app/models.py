from app import db
from app import login
from sqlalchemy.ext.declarative import DeclarativeMeta
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

BaseModel: DeclarativeMeta = db.Model


class User(UserMixin, BaseModel):
    """
    Table to store users

    Follow these to remove users from the database:
    https://flask-sqlalchemy.palletsprojects.com/en/2.x/queries/
    """

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean(), index=True, default=False)

    def __repr__(self):
        return "User: {}".format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class LearnProgress(UserMixin, BaseModel):
    """
    Table to store learning progress
    """

    user_id = db.Column(db.Integer, primary_key=True)
    high_a = db.Column(db.Boolean(), index=True, default=False)
    high_b = db.Column(db.Boolean(), index=True, default=False)
    high_c = db.Column(db.Boolean(), index=True, default=False)
    high_d = db.Column(db.Boolean(), index=True, default=False)
    low_a = db.Column(db.Boolean(), index=True, default=False)
    low_b = db.Column(db.Boolean(), index=True, default=False)
    low_c = db.Column(db.Boolean(), index=True, default=False)
    low_d = db.Column(db.Boolean(), index=True, default=False)

    def __repr__(self):
        return "UserID: {}".format(self.user_id)


class Attempt(UserMixin, BaseModel):
    """
    Table to store assessment attempts
    """

    user_id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(64), index=True)
    score = db.Column(db.Integer, default=0)
    question_1 = db.Column(db.Boolean(), index=True)
    question_2 = db.Column(db.Boolean(), index=True)
    question_3 = db.Column(db.Boolean(), index=True)
    question_4 = db.Column(db.Boolean(), index=True)
    question_5 = db.Column(db.Boolean(), index=True)
    timestamp = db.Column(db.DateTime(), index=True)

    def __repr__(self):
        return "UserID: {}".format(self.user_id)

    def generate_score(
        self,
        scores=[
            question_1,
            question_2,
            question_3,
            question_4,
            question_5,
        ],
    ):
        self.result = sum(scores)
