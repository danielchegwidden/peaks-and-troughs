from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_wtf.csrf import CSRFProtect


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db, render_as_batch=True)
bootstrap = Bootstrap(app)
csrf = CSRFProtect(app)
login = LoginManager(app)
login.login_view = "login"

from app import routes, models, controllers

from app.models import Users, Progress, Attempt, Questions
from tests import test_accounts, initial_questions, initial_data

DEVELOP = True
if DEVELOP:
    Users.query.delete()
    Progress.query.delete()
    Attempt.query.delete()
    Questions.query.delete()
    test_accounts.main()
    initial_questions.main()
    initial_data.main()
