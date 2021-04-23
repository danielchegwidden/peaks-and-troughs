from app import app, db
from app.models import User, LearnProgress, Attempt

# $ flask shell
@app.shell_context_processor
def make_shell_context():
    return {"db": db, "User": User, "Progress": LearnProgress, "Attempt": Attempt}


if __name__ == "__main__":
    app.run(debug=True, use_debugger=False, use_reloader=False)
