from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.controllers import UserController, AdminController
from app.models import Users, Progress, Attempt, Questions
from app.forms import LoginForm, RegistrationForm, AttemptForm
from flask_login import current_user, login_user, login_required
from flask_login import logout_user
from werkzeug.urls import url_parse


@app.route("/")
@app.route("/index")
def index():
    return AdminController.home()


@app.route("/login", methods=["GET", "POST"])
def login():
    if not current_user.is_authenticated:
        return UserController.login()
    return redirect(url_for("index"))


@app.route("/logout")
def logout():
    return UserController.logout()


@app.route("/register", methods=["GET", "POST"])
def register():
    if not current_user.is_authenticated:
        return UserController.register()
    return redirect(url_for("index"))


@app.route("/learn")
@login_required
def learn():
    return UserController.learn()


@app.route("/assessment", methods=["GET", "POST"])
@login_required
def assessment():
    return UserController.attempt()


@app.route("/feedback")
@login_required
def feedback():
    return UserController.feedback()


@app.route("/statistics")
@login_required
def statistics():
    return AdminController.stats()
