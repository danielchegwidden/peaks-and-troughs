import unittest, os
from app import app, db
from app.models import Users, Progress, Attempt, Questions
from datetime import datetime


class UserModelCase(unittest.TestCase):
    def setUp(self):
        basedir = os.path.abspath(os.path.dirname(__file__))
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "test.db")
        self.app = app.test_client()
        db.create_all()
        user1 = Users(id=9999, username="FirstTest", email="test1@peaksandtroughs.com")
        user2 = Users(id=9998, username="SecondTest", email="test2@peaksandtroughs.com")
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_password_hashing(self):
        u1 = Users.query.get(9999)
        u1.set_password("testmypassword")
        self.assertFalse(u1.check_password("notmypassword"))
        self.assertTrue(u1.check_password("testmypassword"))

    def test_is_committed(self):
        pass
        # u3 = Users(id=9997, username="ThirdTest", email="test3@peaksandtroughs.com")
        # self.assertFalse(u3.is_committed())
        # db.session.add(u3)
        # db.session.commit()
        # self.assertTrue(u3.is_committed())


class ProgressModelCase(unittest.TestCase):
    def setUp(self):
        basedir = os.path.abspath(os.path.dirname(__file__))
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "test.db")
        self.app = app.test_client()
        db.create_all()
        user1 = Users(id=9999, username="FirstTest", email="test1@peaksandtroughs.com")
        progress1 = Progress(user_id=9999)
        db.session.add(user1)
        db.session.add(progress1)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_learn_progress(self):
        pass

    def test_get_progress(self):
        pass


class AttemptModelCase(unittest.TestCase):
    def setUp(self):
        basedir = os.path.abspath(os.path.dirname(__file__))
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "test.db")
        self.app = app.test_client()
        db.create_all()
        user1 = Users(id=9999, username="FirstTest", email="test1@peaksandtroughs.com")
        attempt1 = Attempt(
            user_id=9999,
            category="High",
            question_1_id=1,
            question_2_id=2,
            question_3_id=3,
            question_4_id=4,
            question_5_id=5,
        )
        q1 = Questions(
            question_text="Test Question 1",
            answer_1="Answer A",
            answer_2="Answer B",
            answer_3="Answer C",
            answer_4="Answer D",
            correct_answer="D",
        )
        db.session.add(user1)
        db.session.add(attempt1)
        db.session.add(q1)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    # def test_post_results(self):
    #     a1 = Attempt.query.filter_by(user_id=9999).first()
    #     q1 = [
    #         a1.question_1_id,
    #         a1.question_2_id,
    #         a1.question_3_id,
    #         a1.question_4_id,
    #         a1.question_5_id,
    #     ]
    #     a1.post_results(category=a1.category, questions=q1, answers=["A", "A", "A", "A", "A"])
    #     db.session.add(a1)
    #     db.session.commit()
    #     self.assertFalse(a1.question_1_result)
    #     self.assertTrue(a1.question_4_result) ##
    #     self.assertTrue(a1.timestamp < datetime.now())

    def test_post_score(self):
        pass
        # a1 = Attempt.query.filter_by(user_id=9999).first()
        # a1.post_score()
        # db.session.add(a1)
        # db.session.commit()
        # self.assertFalse(a1.score == 0)
        # self.assertTrue(a1.score == 1)

    def test_get_attempts(self):
        pass

    def test_calculate_num_attempts(self):
        pass

    def test_calculate_avg_score(self):
        pass

    def test_calculate_max_score(self):
        pass

    def test_get_latest_attempt(self):
        pass

    def test_day_frequency(self):
        pass

    def test_score_frequency(self):
        pass

    def test_get_my_questions(self):
        pass


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
        self.assertFalse(Questions.calculate_results(question_id=1, answer="A"))
        self.assertTrue(Questions.calculate_results(question_id=1, answer="D"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
