from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import Users


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
    answer_1 = SelectField(
        u"Question 1",
        choices=[("cpp", "C++"), ("py", "Python"), ("text", "Plain Text")],
        validators=[DataRequired()],
    )
    answer_2 = SelectField(
        u"Question 2",
        choices=[("cpp", "C++"), ("py", "Python"), ("text", "Plain Text")],
        validators=[DataRequired()],
    )
    answer_3 = SelectField(
        u"Question 3",
        choices=[("cpp", "C++"), ("py", "Python"), ("text", "Plain Text")],
        validators=[DataRequired()],
    )
    answer_4 = SelectField(
        u"Question 4",
        choices=[("cpp", "C++"), ("py", "Python"), ("text", "Plain Text")],
        validators=[DataRequired()],
    )
    answer_5 = SelectField(
        u"Question 5",
        choices=[("cpp", "C++"), ("py", "Python"), ("text", "Plain Text")],
        validators=[DataRequired()],
    )
    submit = SubmitField("Submit Attempt")
