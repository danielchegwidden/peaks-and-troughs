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
    stocks_a = db.Column(db.Boolean(), index=True, default=False)
    stocks_b = db.Column(db.Boolean(), index=True, default=False)
    deriv_a = db.Column(db.Boolean(), index=True, default=False)
    deriv_b = db.Column(db.Boolean(), index=True, default=False)

    def __repr__(self):
        return "UserID: {}".format(self.user_id)


class Attempt(UserMixin, BaseModel):
    """
    Table to store assessment attempts
    """

    user_id = db.Column(db.Integer, primary_key=True)
    result = db.Column(db.Float, default=0.0)

    question_1_ans = db.Column(db.String(64), index=True)
    question_2_ans = db.Column(db.String(64), index=True)
    question_3_ans = db.Column(db.String(64), index=True)
    question_4_ans = db.Column(db.String(64), index=True)
    question_5_ans = db.Column(db.String(64), index=True)

    question_1_score = db.Column(db.Boolean(), index=True, default=False)
    question_2_score = db.Column(db.Boolean(), index=True, default=False)
    question_3_score = db.Column(db.Boolean(), index=True, default=False)
    question_4_score = db.Column(db.Boolean(), index=True, default=False)
    question_5_score = db.Column(db.Boolean(), index=True, default=False)

    def __repr__(self):
        return "UserID: {}".format(self.user_id)

    def post_score(self, question, score):
        self.question = score

    def generate_score(
        self,
        scores=[
            question_1_score,
            question_2_score,
            question_3_score,
            question_4_score,
            question_5_score,
        ],
    ):
        self.result = sum(scores) / len(scores)
