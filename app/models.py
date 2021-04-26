from app import db
from app import login
from sqlalchemy.ext.declarative import DeclarativeMeta
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime

BaseModel: DeclarativeMeta = db.Model


class Users(UserMixin, BaseModel):
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
        return "{}".format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return Users.query.get(int(id))


class LearnProgress(BaseModel):
    """
    Table to store learning progress
    """

    user_id = db.Column(db.Integer, primary_key=True)
    high_a = db.Column(db.Boolean(), default=False)
    high_b = db.Column(db.Boolean(), default=False)
    high_c = db.Column(db.Boolean(), default=False)
    high_d = db.Column(db.Boolean(), default=False)
    low_a = db.Column(db.Boolean(), default=False)
    low_b = db.Column(db.Boolean(), default=False)
    low_c = db.Column(db.Boolean(), default=False)
    low_d = db.Column(db.Boolean(), default=False)

    def __repr__(self):
        return "{}".format(self.user_id)


class Attempt(BaseModel):
    """
    Table to store assessment attempts
    """

    user_id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(64))
    question_1 = db.Column(db.Boolean())
    question_2 = db.Column(db.Boolean())
    question_3 = db.Column(db.Boolean())
    question_4 = db.Column(db.Boolean())
    question_5 = db.Column(db.Boolean())
    timestamp = db.Column(db.DateTime, default=datetime.now)
    score = db.Column(db.Integer, default=0)

    def __repr__(self):
        return "{}".format(self.user_id)

    def calculate_scores(self, question_id, answer):
        return 1 if answer == correct(question_id) else 0

    def post_score(self, category, question_1, question_2, question_3, question_4, question_5):
        self.category = category
        self.question_1 = calculate_scores(1, question_1)
        self.question_2 = calculate_scores(2, question_2)
        self.question_3 = calculate_scores(3, question_3)
        self.question_4 = calculate_scores(4, question_4)
        self.question_5 = calculate_scores(5, question_5)
        self.timestamp = datetime.now()

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
        self.score = sum(scores)


class Questions(BaseModel):
    """
    Table to store questions and answers
    """

    question_id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.String(256))
    answer_1 = db.Column(db.String(64))
    answer_2 = db.Column(db.String(64))
    answer_3 = db.Column(db.String(64))
    answer_4 = db.Column(db.String(64))
    correct_answer = db.Column(db.String(64))

    def __repr__(self):
        return "{}".format(self.question_id)

    def correct(self, question_id):
        return self.correct_answer
