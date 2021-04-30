from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import Users, Questions


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")


class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField("Repeat Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Register")

    def validate_username(self, username):
        user = Users.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError("Please use a different username.")

    def validate_email(self, email):
        user = Users.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError("Please use a different email address.")


class AttemptForm(FlaskForm):
    questions = [1, 2, 3, 4, 5]  # REMEMBER TO REMOVE
    question_1 = Questions.query.get(questions[0])
    answer_1 = SelectField(
        u"Question 1: " + question_1.question_text,
        choices=[
            ("A", question_1.answer_1),
            ("B", question_1.answer_2),
            ("C", question_1.answer_3),
            ("D", question_1.answer_4),
        ],
        validators=[DataRequired()],
    )
    question_2 = Questions.query.get(questions[1])
    answer_2 = SelectField(
        u"Question 2: " + question_2.question_text,
        choices=[
            ("A", question_2.answer_1),
            ("B", question_2.answer_2),
            ("C", question_2.answer_3),
            ("D", question_2.answer_4),
        ],
        validators=[DataRequired()],
    )
    question_3 = Questions.query.get(questions[2])
    answer_3 = SelectField(
        u"Question 3: " + question_3.question_text,
        choices=[
            ("A", question_3.answer_1),
            ("B", question_3.answer_2),
            ("C", question_3.answer_3),
            ("D", question_3.answer_4),
        ],
        validators=[DataRequired()],
    )
    question_4 = Questions.query.get(questions[3])
    answer_4 = SelectField(
        u"Question 4: " + question_4.question_text,
        choices=[
            ("A", question_4.answer_1),
            ("B", question_4.answer_2),
            ("C", question_4.answer_3),
            ("D", question_4.answer_4),
        ],
        validators=[DataRequired()],
    )
    question_5 = Questions.query.get(questions[4])
    answer_5 = SelectField(
        u"Question 5: " + question_5.question_text,
        choices=[
            ("A", question_5.answer_1),
            ("B", question_5.answer_2),
            ("C", question_5.answer_3),
            ("D", question_5.answer_4),
        ],
        validators=[DataRequired()],
    )
    submit = SubmitField("Submit Attempt")

    # def __init__(self, questions):
    #     self.questions = questions
