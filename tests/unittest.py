import unittest, os
from app import app, db, models
from app.models import Users, Progress, Attempt, Questions
from datetime import datetime


class UserModelCase(unittest.TestCase):
    def setUp(self):
        basedir = os.path.abspath(os.path.dirname(__file__))
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "test.db")
        self.app = app.test_client()
        db.create_all()
        user1 = Users(id=9999, username="FirstTest", email="test-u1@peaksandtroughs.com")
        user2 = Users(id=9998, username="SecondTest", email="test-u2@peaksandtroughs.com")
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_password_hashing(self):
        u1 = Users.query.get(9999)
        u1.set_password("testmyPassword!")
        self.assertFalse(u1.check_password("notmypassword"))
        self.assertTrue(u1.check_password("testmyPassword!"))
        self.assertFalse(u1.password_hash == "testmyPassword!")

    def test_users_repr(self):
        self.assertTrue(str(Users.query.get(9999)) == "FirstTest")

    def test_user(self):
        self.assertTrue(models.load_user(9999))
        self.assertFalse(models.load_user(9997))


class ProgressModelCase(unittest.TestCase):
    def setUp(self):
        basedir = os.path.abspath(os.path.dirname(__file__))
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "test.db")
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_learn_progress(self):
        p1 = Progress(user_id=9999)
        db.session.add(p1)
        db.session.commit()
        self.assertFalse(Progress.learn_progress(user_id=9999)[1] == 1)
        self.assertTrue(Progress.learn_progress(user_id=9999)[0] == 1)

        p1.high_a = True
        db.session.add(p1)
        db.session.commit()
        self.assertFalse(Progress.learn_progress(user_id=9999)[0] == 1)
        self.assertTrue(Progress.learn_progress(user_id=9999)[1] == 1)
        self.assertTrue(len(Progress.learn_progress(user_id=9999)) == 5)

    def test_get_progress(self):
        p2 = Progress(user_id=9998)
        db.session.add(p2)
        db.session.commit()
        self.assertTrue(Progress.get_progress(progress=p2) == 0)
        self.assertTrue(Progress.get_progress(progress=p2, category="Low") == 0)
        self.assertTrue(Progress.get_progress(progress=p2, category="Medium") is None)

        p2.high_a = True
        db.session.add(p2)
        db.session.commit()
        self.assertTrue(Progress.get_progress(progress=p2) == 1)

    def test_progress_repr(self):
        p3 = Progress(user_id=9999)
        db.session.add(p3)
        db.session.commit()
        self.assertTrue(str(Progress.query.filter_by(user_id=9999).first()) == "1")


class AttemptModelCase(unittest.TestCase):
    def setUp(self):
        basedir = os.path.abspath(os.path.dirname(__file__))
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "test.db")
        self.app = app.test_client()
        db.create_all()
        questions1 = Questions(
            question_text="Test Question 1",
            answer_1="Answer A",
            answer_2="Answer B",
            answer_3="Answer C",
            answer_4="Answer D",
            correct_answer="D",
        )
        db.session.add(questions1)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_get_attempts(self):
        self.assertFalse(Attempt.get_attempts())
        a1 = Attempt(
            user_id=9998,
            category="High",
            question_1_id=1,
            question_2_id=1,
            question_3_id=1,
            question_4_id=1,
            question_5_id=1,
        )
        db.session.add(a1)
        db.session.commit()
        self.assertTrue(Attempt.get_attempts())
        self.assertTrue(Attempt.get_attempts(user_id=9998))

    def test_calculate_num_attempts(self):
        self.assertFalse(Attempt.calculate_num_attempts())

        a2 = Attempt(
            user_id=9997,
            category="High",
            question_1_id=1,
            question_2_id=1,
            question_3_id=1,
            question_4_id=1,
            question_5_id=1,
        )
        db.session.add(a2)
        db.session.commit()
        self.assertTrue(Attempt.calculate_num_attempts())
        self.assertTrue(Attempt.calculate_num_attempts(user_id=9997) == 1)

        a3 = Attempt(
            user_id=9997,
            category="High",
            question_1_id=1,
            question_2_id=1,
            question_3_id=1,
            question_4_id=1,
            question_5_id=1,
        )
        db.session.add(a3)
        db.session.commit()
        self.assertTrue(Attempt.calculate_num_attempts(user_id=9997) == 2)

    def test_calculate_avg_score(self):
        self.assertFalse(Attempt.calculate_avg_score())

        a4 = Attempt(
            user_id=9996,
            category="High",
            question_1_id=1,
            question_2_id=1,
            question_3_id=1,
            question_4_id=1,
            question_5_id=1,
        )
        a4.post_results(
            category="High", questions=[1, 1, 1, 1, 1], answers=["A", "B", "C", "D", "A"]
        )
        a4.post_score()
        db.session.add(a4)
        db.session.commit()
        self.assertTrue(Attempt.calculate_avg_score(user_id=9996) == 1)

    def test_calculate_max_score(self):
        self.assertFalse(Attempt.calculate_max_score())

        a5 = Attempt(
            user_id=9995,
            category="High",
            question_1_id=1,
            question_2_id=1,
            question_3_id=1,
            question_4_id=1,
            question_5_id=1,
        )
        a5.post_results(
            category="High", questions=[1, 1, 1, 1, 1], answers=["A", "B", "C", "D", "A"]
        )
        a5.post_score()
        db.session.add(a5)
        db.session.commit()
        self.assertTrue(Attempt.calculate_max_score(user_id=9995) == 1)

    def test_get_latest_attempt(self):
        self.assertTrue(Attempt.get_latest_attempt())

        a6 = Attempt(
            user_id=9994,
            category="High",
            question_1_id=1,
            question_2_id=1,
            question_3_id=1,
            question_4_id=1,
            question_5_id=1,
        )
        db.session.add(a6)
        db.session.commit()
        self.assertTrue(Attempt.get_latest_attempt(user_id=9994)[0].user_id == 9994)
        self.assertTrue(Attempt.get_latest_attempt(user_id=9994)[0].timestamp < datetime.now())

    def test_day_frequency(self):
        self.assertTrue(sum(Attempt.day_frequency()) == 0)

        a7 = Attempt(
            user_id=9993,
            category="High",
            question_1_id=1,
            question_2_id=1,
            question_3_id=1,
            question_4_id=1,
            question_5_id=1,
        )
        db.session.add(a7)
        db.session.commit()
        self.assertTrue(sum(Attempt.day_frequency()) == 1)
        self.assertTrue(sum(Attempt.day_frequency(user_id=9993)) == 1)

        day = datetime.now().weekday()
        self.assertTrue(Attempt.day_frequency()[day] == 1)
        self.assertTrue(Attempt.day_frequency(user_id=9993)[day] == 1)

    def test_score_frequency(self):
        self.assertTrue(sum(Attempt.score_frequency()) == 0)

        a8 = Attempt(
            user_id=9992,
            category="High",
            question_1_id=1,
            question_2_id=1,
            question_3_id=1,
            question_4_id=1,
            question_5_id=1,
        )
        db.session.add(a8)
        db.session.commit()
        self.assertTrue(sum(Attempt.score_frequency()) == 1)
        self.assertTrue(Attempt.score_frequency()[0] == 1)
        self.assertTrue(sum(Attempt.score_frequency(user_id=9992)) == 1)
        self.assertTrue(Attempt.score_frequency(user_id=9992)[0] == 1)

    def test_get_my_questions(self):
        a9 = Attempt(
            user_id=9991,
            category="High",
            question_1_id=1,
            question_2_id=1,
            question_3_id=1,
            question_4_id=1,
            question_5_id=1,
        )
        db.session.add(a9)
        db.session.commit()
        self.assertTrue(
            Questions.get_my_questions(attempt_id=a9.id)["question_1"] == "Test Question 1"
        )

    def test_attempt_repr(self):
        a10 = Attempt(
            user_id=9990,
            category="High",
            question_1_id=1,
            question_2_id=1,
            question_3_id=1,
            question_4_id=1,
            question_5_id=1,
        )
        db.session.add(a10)
        db.session.commit()
        self.assertTrue(str(Attempt.query.filter_by(user_id=9990).first()) == "12")


class QuestionsModelCase(unittest.TestCase):
    def setUp(self):
        basedir = os.path.abspath(os.path.dirname(__file__))
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "test.db")
        self.app = app.test_client()
        db.create_all()
        q1 = Questions(
            question_text="Test Question 1",
            answer_1="Answer A",
            answer_2="Answer B",
            answer_3="Answer C",
            answer_4="Answer D",
            correct_answer="D",
        )
        db.session.add(q1)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_correct(self):
        q1 = Questions.query.get(1)
        self.assertFalse(q1.correct(question_id=1) == "A")
        self.assertTrue(q1.correct(question_id=1) == "D")

    def test_calculate_results(self):
        self.assertFalse(Questions.calculate_results(question_id=10, answer="A"))
        self.assertTrue(Questions.calculate_results(question_id=1, answer="D"))

    def test_question_repr(self):
        self.assertTrue(str(Questions.query.get(1)) == "1")


if __name__ == "__main__":
    unittest.main(verbosity=2)
