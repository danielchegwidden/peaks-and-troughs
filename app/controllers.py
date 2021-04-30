from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.models import Users, Progress, Attempt, Questions
from app.forms import LoginForm, RegistrationForm, AttemptForm
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.urls import url_parse


class UserController:
    @staticmethod
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            user = Users.query.filter_by(username=form.username.data).first()
            if user is None or not user.check_password(form.password.data):
                flash("Invalid username or password")
                return redirect(url_for("login"))
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get("next")
            if not next_page or url_parse(next_page).netloc != "":
                next_page = url_for("index")
            return redirect(next_page)
        return render_template("login.html", title="Sign In", form=form)

    @staticmethod
    def logout():
        logout_user()
        return redirect(url_for("index"))

    @staticmethod
    def register():
        form = RegistrationForm()
        if form.validate_on_submit():
            user = Users(username=form.username.data, email=form.email.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash("Congratulations, you are now a registered user!")
            return redirect(url_for("login"))
        return render_template("register.html", title="Register", form=form)

    @staticmethod
    def learn():
        return render_template("learn.html", title="Learn")

    @staticmethod
    def attempt():
        form = AttemptForm()
        user = Users.query.filter_by(username=current_user.username).first()
        questions = [1, 2, 3, 4, 5]  # REMEMBER TO REMOVE
        category = "High"  # REMEMBER TO REMOVE
        if form.validate_on_submit():
            attempt = Attempt(user_id=current_user.id)
            answers = [
                form.answer_1.data,
                form.answer_2.data,
                form.answer_3.data,
                form.answer_4.data,
                form.answer_5.data,
            ]
            attempt.post_results(category=category, questions=questions, answers=answers)
            attempt.post_score()
            db.session.add(attempt)
            db.session.commit()
            next_page = request.args.get("next")
            if not next_page or url_parse(next_page).netloc != "":
                next_page = url_for("feedback")
            return redirect(next_page)
        return render_template("assessment.html", title="Assessment", form=form)

    @staticmethod
    def feedback():
        return render_template("feedback.html", title="Feedback")


class AdminController:
    @staticmethod
    def home():
        try:
            user = Users.query.filter_by(username=current_user.username).first()
        except:
            user = ""
        return render_template("index.html", title="Home", user=user)

    @staticmethod
    def stats():
        users = Users.query.all()
        progress = Progress.query.all()
        attempts = Attempt.query.all()
        questions = Questions.query.all()
        if current_user.is_authenticated and current_user.is_admin:
            return render_template(
                "statistics.html",
                title="Statistics",
                users=users,
                progress=progress,
                attempts=attempts,
                questions=questions,
            )
        return redirect(url_for("index"))
