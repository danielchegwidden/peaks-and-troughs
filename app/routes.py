from flask import render_template, flash, redirect, url_for, request
from app import app
from app import db
from app.models import Users, LearnProgress, Attempt
from app.forms import LoginForm, RegistrationForm, AttemptForm
from flask_login import current_user, login_user, login_required
from flask_login import logout_user
from werkzeug.urls import url_parse


@app.route("/")
@app.route("/index")
def index():
    try:
        user = Users.query.filter_by(username=current_user.username).first()
    except:
        user = ""
    return render_template("index.html", title="Home", user=user)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
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


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("learn"))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = Users(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Congratulations, you are now a registered user!")
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)


@app.route("/learn")
@login_required
def learn():
    return render_template("learn.html", title="Learn")


@app.route("/assessment", methods=["GET", "POST"])
@login_required
def assessment():
    form = AttemptForm()
    user = Users.query.filter_by(username=current_user.username).first()
    if form.validate_on_submit():
        attempt = Attempt(user_id=user.id)
        answers = [
            form.answer_1.data,
            form.answer_2.data,
            form.answer_3.data,
            form.answer_4.data,
            form.answer_5.data,
        ]
        post_score(
            category="High",
            question_1=answer[0],
            question_2=answer[1],
            question_3=answer[2],
            question_4=answer[3],
            question_5=answer[4],
        )
        generate_score(answers)
        db.session.add(attempt)
        db.session.commit()

        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("feedback")
        return redirect(next_page)
    return render_template("assessment.html", title="Assessment", form=form)


@app.route("/feedback")
@login_required
def feedback():
    return render_template("feedback.html", title="Feedback")


@app.route("/statistics")
@login_required
def statistics():
    users = Users.query.all()
    progress = LearnProgress.query.all()
    attempts = Attempt.query.all()
    if current_user.is_authenticated and current_user.is_admin:
        return render_template(
            "statistics.html", title="Statistics", users=users, progress=progress, attempts=attempts
        )
    return redirect(url_for("index"))
