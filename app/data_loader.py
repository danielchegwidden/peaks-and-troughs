from app import app
from app import db
from app.models import Users, Attempt, Progress, Questions
from datetime import datetime, timedelta


def create_user(id, username, email, password, admin=False):
    user = Users(id=id, username=username, email=email, is_admin=admin)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    progress = Progress(user_id=id)
    db.session.add(progress)
    db.session.commit()


def add_question(question_id, question_text, answers, correct_answer):
    question = Questions(
        question_id=question_id,
        question_text=question_text,
        answer_1=answers[0][1],
        answer_2=answers[1][1],
        answer_3=answers[2][1],
        answer_4=answers[3][1],
        correct_answer=correct_answer,
    )
    db.session.add(question)
    db.session.commit()


def add_progress(user_id, prog_a, prog_b, prog_c, prog_d):
    progress = Progress.query.filter_by(user_id=user_id).first()
    progress.high_a = prog_a
    progress.high_b = prog_b
    progress.high_c = prog_c
    progress.high_d = prog_d
    db.session.add(progress)
    db.session.commit()


def add_attempts(user_id, category, questions, answers, day):
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
    a.timestamp = datetime.now() - timedelta(days=day)
    db.session.add(a)
    db.session.commit()


def test_admin():
    create_user(
        id=1,
        username="test-admin",
        email="test-admin@peaksandtroughs.com",
        password="Test3210",
        admin=True,
    )


def test_users():
    create_user(
        id=2, username="test-user", email="test-user@peaksandtroughs.com", password="Test0123"
    )
    for new in range(3, 13):
        create_user(
            id=new,
            username="test-user-" + str(new),
            email="test-user-" + str(new) + "@peaksandtroughs.com",
            password="MyTestUser123",
        )


def initial_questions():
    add_question(
        question_id=1,
        question_text="In 2001 when Enron collapsed under a $40 billion accounting scandal, shareholders had to pay which of the following?",
        answers=[
            ("A", "Up to the value of the shares they held at the time"),
            ("B", "Up to the value of the debts Enron had oustanding"),
            ("C", "$1,000 per shareholder"),
            ("D", "Nothing, they had no liability"),
        ],
        correct_answer="D",
    )

    add_question(
        question_id=2,
        question_text="Which of the following is not an example of a derivative product?",
        answers=[
            ("A", "Put Option"),
            ("B", "Oil Future"),
            ("C", "Currency Swap"),
            ("D", "Index Fund"),
        ],
        correct_answer="D",
    )

    add_question(
        question_id=3,
        question_text="In which of the following cryptocurrencies can you find the Nyan Cat animation embedded on the blockchain?",
        answers=[
            ("A", "Bitcoin"),
            ("B", "Ethereum"),
            ("C", "Dogecoin"),
            ("D", "Litecoin"),
        ],
        correct_answer="B",
    )

    add_question(
        question_id=4,
        question_text="The people who had their entire savings wiped out by Bernie Madoff faced which of the following risks?",
        answers=[
            ("A", "Concentration Risk"),
            ("B", "Market Risk"),
            ("C", "Liquidity Risk"),
            ("D", "Inflation Risk"),
        ],
        correct_answer="A",
    )

    add_question(
        question_id=5,
        question_text="Which of the following did not contribute to the 2008 Financial Crisis?",
        answers=[
            ("A", "Subprime mortgages being signed to people who could not repay them"),
            ("B", "Lack of regulation and oversight by government entities and agencies"),
            ("C", "The volatile nature of cryptocurrencies"),
            (
                "D",
                "Bonuses and incentives rewarding traders and bankers for risky investment decisions",
            ),
        ],
        correct_answer="C",
    )


def initial_attempts():
    add_progress(3, False, False, False, False)
    add_attempts(3, "High", [1, 2, 3, 4, 5], ["A", "A", "A", "A", "A"], 1)
    add_progress(4, True, False, False, False)
    add_attempts(4, "High", [1, 2, 3, 4, 5], ["B", "D", "A", "C", "B"], 2)
    add_progress(5, True, True, False, False)
    add_attempts(5, "High", [1, 2, 3, 4, 5], ["A", "B", "C", "D", "A"], 3)
    add_progress(6, True, True, True, False)
    add_attempts(6, "High", [1, 2, 3, 4, 5], ["C", "A", "B", "A", "D"], 4)
    add_progress(7, True, True, True, True)
    add_attempts(7, "High", [1, 2, 3, 4, 5], ["A", "C", "A", "B", "D"], 5)
    add_progress(8, False, False, False, True)
    add_attempts(8, "High", [1, 2, 3, 4, 5], ["D", "A", "C", "A", "B"], 6)
    add_progress(9, False, False, True, True)
    add_attempts(9, "High", [1, 2, 3, 4, 5], ["A", "D", "A", "C", "A"], 1)
    add_progress(10, False, True, True, True)
    add_attempts(10, "High", [1, 2, 3, 4, 5], ["B", "D", "C", "A", "C"], 2)
    add_progress(11, True, True, True, True)
    add_attempts(11, "High", [1, 2, 3, 4, 5], ["A", "B", "A", "D", "A"], 3)
    add_progress(12, False, True, True, False)
    add_attempts(12, "High", [1, 2, 3, 4, 5], ["D", "D", "B", "A", "C"], 4)


def main():
    test_admin()
    test_users()
    initial_questions()
    initial_attempts()


if __name__ == "__main__":
    main()
