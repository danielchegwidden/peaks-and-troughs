from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm


@app.route("/")
@app.route("/index")
def index():
    user = {"username": "Daniel"}
    posts = [
        {"author": {"username": "John"}, "body": "Beautiful day in Portland!"},
        {"author": {"username": "Susan"}, "body": "The Avengers movie was so cool!"},
    ]
    return render_template("index.html", title="Home", user=user, posts=posts)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(
            "Login requested for user {}, remember_me={}".format(
                form.username.data, form.remember_me.data
            )
        )
        return redirect(url_for("index"))
    return render_template("login.html", title="Sign In", form=form)


@app.route("/learn")
def learn():
    return render_template("learn.html", title="Learn")


@app.route("/assessment")
def assessment():
    return render_template("assessment.html", title="Assessment")


@app.route("/feedback")
def feedback():
    return render_template("feedback.html", title="Feedback")


@app.route("/statistics")
def statistics():
    return render_template("statistics.html", title="Statistics")
