from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.models import Users, Progress, Attempt, Questions
from app.forms import LoginForm, RegistrationForm, AttemptForm, SubmitForm
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.urls import url_parse
from sqlalchemy.sql import func


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
            user = Users.query.filter_by(username=current_user.username).first()
            progress = Progress(user_id=user.user_id)
            db.session.add(progress)
            db.session.commit()
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
        user = Users.query.filter_by(username=current_user.username).first()
        results = Attempt.query.filter_by(user_id=user.id)
        attempts = len(Attempt.query.filter(Attempt.user_id == user.id).all())
        max_score = (
            Attempt.query.with_entities(func.max(Attempt.score).label("maximum"))
            .filter(Attempt.user_id == user.id)
            .all()[0][0]
        )
        avg_score = (
            Attempt.query.with_entities(func.avg(Attempt.score).label("average"))
            .filter(Attempt.user_id == user.id)
            .all()[0][0]
        )
        latest = max(
            Attempt.query.with_entities(func.max(Attempt.timestamp).label("latest"))
            .filter(Attempt.user_id == user.id)
            .all()
        )
        latest_attempt = Attempt.query.filter_by(user_id=user.id, timestamp=latest[0])
        questions = [
            Questions.query.filter_by(question_id=latest_attempt[0].question_1_id)
            .first()
            .question_text,
            Questions.query.filter_by(question_id=latest_attempt[0].question_2_id)
            .first()
            .question_text,
            Questions.query.filter_by(question_id=latest_attempt[0].question_3_id)
            .first()
            .question_text,
            Questions.query.filter_by(question_id=latest_attempt[0].question_4_id)
            .first()
            .question_text,
            Questions.query.filter_by(question_id=latest_attempt[0].question_5_id)
            .first()
            .question_text,
        ]
        return render_template(
            "feedback.html",
            title="Feedback",
            results=results,
            attempts=attempts,
            max_score=max_score,
            avg_score=avg_score,
            latest=latest_attempt,
            questions=questions,
        )


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


class ProgressController:
    @staticmethod
    def highrisk():
        form = SubmitForm()
        progress = Progress.query.filter_by(user_id=current_user.id).first()
        if "high_a" in request.form:
            progress.high_a = True
        elif "high_b" in request.form:
            progress.high_b = True
        elif "high_c" in request.form:
            progress.high_c = True
        elif "high_d" in request.form:
            progress.high_d = True
        db.session.add(progress)
        db.session.commit()
        return render_template(
            "highrisk.html", title="Learn - High Risk", form=form, progress=progress
        )

    @staticmethod
    def lowrisk():
        form = SubmitForm()
        progress = Progress.query.filter_by(user_id=current_user.id).first()
        if "low_a" in request.form:
            progress.low_a = True
        elif "low_b" in request.form:
            progress.low_b = True
        elif "low_c" in request.form:
            progress.low_c = True
        elif "low_d" in request.form:
            progress.low_d = True
        db.session.add(progress)
        db.session.commit()
        return render_template(
            "lowrisk.html", title="Learn - Low Risk", form=form, progress=progress
        )

    # def reset_progress():
    #     progress = Progress.query.filter_by(user_id=current_user.id).first()
    #     progress.high_a = False
    #     progress.high_b = False
    #     progress.high_c = False
    #     progress.high_d = False
    #     progress.low_a = False
    #     progress.low_b = False
    #     progress.low_c = False
    #     progress.low_d = False
    #     return render_template("learn.html", title="Learn")
