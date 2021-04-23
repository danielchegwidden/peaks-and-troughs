from flask import render_template, flash, redirect, url_for, request
from app import app
from app import db
from app.models import User, LearnProgress, Attempt
from app.forms import LoginForm, RegistrationForm, AttemptForm
from flask_login import current_user, login_user, login_required
from flask_login import logout_user
from werkzeug.urls import url_parse


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html", title="Home")


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("learn"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("login"))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("learn")
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
        user = User(username=form.username.data, email=form.email.data)
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
    if form.validate_on_submit():
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
    users = User.query.all()
    if current_user.is_authenticated and current_user.is_admin:
        return render_template("statistics.html", title="Statistics", users=users)
    return redirect(url_for("index"))
