from app import app
from app import db
from app.models import Attempt, Progress


def add_progress(user_id):
    prog = Progress(user_id=user_id)
    db.session.add(prog)
    db.session.commit()


def add_attempts(user_id, category, questions, answers):
    a = Attempt(
        user_id=user_id,
        category=category,
        question_1_id=questions[0],
        question_2_id=questions[1],
        question_3_id=questions[2],
        question_4_id=questions[3],
        question_5_id=questions[4],
    )
    a.post_results(category=category, questions=questions, answers=answers)
    a.post_score()
    db.session.add(a)
    db.session.commit()


def main():
    add_progress(0)
    add_progress(1)
    # add_attempts(0, "High", [1, 2, 3, 4, 5], ["A", "A", "A", "A", "A"])
    # add_attempts(0, "High", [1, 2, 3, 4, 5], ["A", "B", "C", "D", "A"])
    # add_attempts(0, "High", [1, 2, 3, 4, 5], ["C", "D", "B", "C", "A"])


if __name__ == "__main__":
    main()
