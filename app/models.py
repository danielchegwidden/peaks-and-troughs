from app import db
from app import login
from sqlalchemy.ext.declarative import DeclarativeMeta
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
from sqlalchemy.sql import func

BaseModel: DeclarativeMeta = db.Model


@login.user_loader
def load_user(id):
    return Users.query.get(int(id))


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

    # def is_committed(self):
    #     return self.username is not None


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

    def learn_progress(user_id=False):
        progress = Progress.query.filter_by(user_id=user_id)
        progress_map = {x: 0 for x in range(5)}
        progress_scores = [Progress.get_progress(p) for p in progress]
        for prog in progress_scores:
            progress_map[prog] += 1
        return [val[1] for val in sorted(progress_map.items())]

    def get_progress(progress, category="High"):
        if category == "High":
            return sum([progress.high_a, progress.high_b, progress.high_c, progress.high_d])
        elif category == "Low":
            return sum([progress.low_a, progress.low_b, progress.low_c, progress.low_d])
        return None


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

    def post_results(self, category, questions, answers):
        self.category = category
        self.question_1_id = questions[0]
        self.question_2_id = questions[1]
        self.question_3_id = questions[2]
        self.question_4_id = questions[3]
        self.question_5_id = questions[4]
        self.question_1_result = Questions.calculate_results(
            question_id=questions[0], answer=answers[0]
        )
        self.question_2_result = Questions.calculate_results(
            question_id=questions[1], answer=answers[1]
        )
        self.question_3_result = Questions.calculate_results(
            question_id=questions[2], answer=answers[2]
        )
        self.question_4_result = Questions.calculate_results(
            question_id=questions[3], answer=answers[3]
        )
        self.question_5_result = Questions.calculate_results(
            question_id=questions[4], answer=answers[4]
        )
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

    def get_attempts(user_id=False):
        if user_id:
            return Attempt.query.filter_by(user_id=user_id)
        else:
            return Attempt.query.all()

    def calculate_num_attempts(user_id=False):
        attempts = Attempt.get_attempts(user_id)
        return sum([1 for _ in attempts])

    def calculate_avg_score(user_id=False):
        avg_score = (
            Attempt.query.with_entities(func.avg(Attempt.score).label("average"))
            .filter(Attempt.user_id == user_id)
            .all()[0][0]
        )
        return avg_score if avg_score is not None else 0.0

    def calculate_max_score(user_id=False):
        max_score = (
            Attempt.query.with_entities(func.max(Attempt.score).label("maximum"))
            .filter(Attempt.user_id == user_id)
            .all()[0][0]
        )
        return max_score if max_score is not None else 0

    def get_latest_attempt(user_id=False):
        latest_time = max(
            Attempt.query.with_entities(func.max(Attempt.timestamp).label("latest"))
            .filter(Attempt.user_id == user_id)
            .all()
        )
        latest_attempt = Attempt.query.filter_by(user_id=user_id, timestamp=latest_time[0])
        return latest_attempt

    def day_frequency(user_id=False):
        attempts = Attempt.get_attempts(user_id=user_id)
        days_map = {x: 0 for x in range(8)}
        days = [a.timestamp.weekday() for a in attempts]
        for day in days:
            days_map[day] += 1
        return [val[1] for val in sorted(days_map.items())]

    def score_frequency(user_id=False):
        attempts = Attempt.get_attempts(user_id=user_id)
        scores_map = {x: 0 for x in range(6)}
        scores = [a.score for a in attempts]
        for score in scores:
            scores_map[score] += 1
        return [val[1] for val in sorted(scores_map.items())]


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

    def calculate_results(question_id, answer):
        question = Questions.query.get(question_id)
        if question is not None:
            return answer == question.correct_answer
        return False
        # return 1 if answer == Questions.query.get(question_id).correct_answer else 0

    def get_my_questions(attempt_id=1):
        attempt = Attempt.query.filter_by(id=attempt_id).first()
        questions = {
            "question_1": Questions.query.filter_by(question_id=attempt.question_1_id)
            .first()
            .question_text,
            "question_2": Questions.query.filter_by(question_id=attempt.question_2_id)
            .first()
            .question_text,
            "question_3": Questions.query.filter_by(question_id=attempt.question_3_id)
            .first()
            .question_text,
            "question_4": Questions.query.filter_by(question_id=attempt.question_4_id)
            .first()
            .question_text,
            "question_5": Questions.query.filter_by(question_id=attempt.question_5_id)
            .first()
            .question_text,
        }
        return questions
