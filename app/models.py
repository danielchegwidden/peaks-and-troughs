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
    progress = db.relationship("Progress", backref="user", lazy="dynamic")
    attempt = db.relationship("Attempt", backref="user", lazy="dynamic")

    def __repr__(self):
        return "{}".format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return Users.query.get(int(id))


class Progress(BaseModel):
    """
    Table to store learning progress
    """

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), index=True)
    high_a = db.Column(db.Boolean(), default=False)
    high_b = db.Column(db.Boolean(), default=False)
    high_c = db.Column(db.Boolean(), default=False)
    high_d = db.Column(db.Boolean(), default=False)
    low_a = db.Column(db.Boolean(), default=False)
    low_b = db.Column(db.Boolean(), default=False)
    low_c = db.Column(db.Boolean(), default=False)
    low_d = db.Column(db.Boolean(), default=False)

    def __repr__(self):
        return "{}".format(self.id)


class Attempt(BaseModel):
    """
    Table to store assessment attempts
    """

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), index=True)
    category = db.Column(db.String(64))
    question_1_id = db.Column(db.Integer, db.ForeignKey("questions.question_id"))
    question_1_result = db.Column(db.Boolean())
    question_2_id = db.Column(db.Integer, db.ForeignKey("questions.question_id"))
    question_2_result = db.Column(db.Boolean())
    question_3_id = db.Column(db.Integer, db.ForeignKey("questions.question_id"))
    question_3_result = db.Column(db.Boolean())
    question_4_id = db.Column(db.Integer, db.ForeignKey("questions.question_id"))
    question_4_result = db.Column(db.Boolean())
    question_5_id = db.Column(db.Integer, db.ForeignKey("questions.question_id"))
    question_5_result = db.Column(db.Boolean())
    timestamp = db.Column(db.DateTime, default=datetime.now)
    score = db.Column(db.Integer, default=0)

    def __repr__(self):
        return "{}".format(self.id)

    def calculate_results(self, question_id, answer):
        return 1 if answer == Questions.query.get(question_id).correct_answer else 0

    def post_results(self, category, questions, answers):
        self.category = category
        self.question_1_result = self.calculate_results(question_id=questions[0], answer=answers[0])
        self.question_2_result = self.calculate_results(question_id=questions[1], answer=answers[1])
        self.question_3_result = self.calculate_results(question_id=questions[2], answer=answers[2])
        self.question_4_result = self.calculate_results(question_id=questions[3], answer=answers[3])
        self.question_5_result = self.calculate_results(question_id=questions[4], answer=answers[4])
        self.timestamp = datetime.now()

    def post_score(self):
        self.score = sum(
            [
                self.question_1_result,
                self.question_2_result,
                self.question_3_result,
                self.question_4_result,
                self.question_5_result,
            ]
        )


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
    correct_answer = db.Column(db.String(8))

    def __repr__(self):
        return "{}".format(self.question_id)

    def correct(self, question_id):
        return self.query.get(question_id).correct_answer
