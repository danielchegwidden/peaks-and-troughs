import unittest, os
from app import app, db
from app.models import Users, Progress, Attempt, Questions
from datetime import datetime


class UserModelCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        user1 = Users(id=9999, username="FirstTest", email="test1@peaksandtroughs.com")
        user2 = Users(id=9998, username="SecondTest", email="test2@peaksandtroughs.com")
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()

    def tearDown(self):
        user1 = Users.query.filter_by(id=9999).first()
        user2 = Users.query.filter_by(id=9998).first()
        # user3 = Users.query.filter_by(id=9997).first()
        db.session.delete(user1)
        db.session.delete(user2)
        # db.session.delete(user3)
        db.session.commit()

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
        self.app = app.test_client()
        user1 = Users(id=9999, username="FirstTest", email="test1@peaksandtroughs.com")
        progress1 = Progress(user_id=9999)
        db.session.add(user1)
        db.session.add(progress1)
        db.session.commit()

    def tearDown(self):
        user1 = Users.query.filter_by(id=9999).first()
        progress1 = Progress.query.filter_by(user_id=9999).first()
        db.session.delete(user1)
        db.session.delete(progress1)
        db.session.commit()


class AttemptModelCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
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
        db.session.add(user1)
        db.session.add(attempt1)
        db.session.commit()

    def tearDown(self):
        user1 = Users.query.filter_by(id=9999).first()
        attempt1 = Attempt.query.filter_by(user_id=9999).first()
        db.session.delete(user1)
        db.session.delete(attempt1)
        db.session.commit()

    def test_calculate_results(self):
        a1 = Attempt.query.filter_by(user_id=9999).first()
        self.assertFalse(a1.calculate_results(question_id=1, answer="A"))
        self.assertTrue(a1.calculate_results(question_id=1, answer="D"))

    def test_post_results(self):
        a1 = Attempt.query.filter_by(user_id=9999).first()
        q1 = [
            a1.question_1_id,
            a1.question_2_id,
            a1.question_3_id,
            a1.question_4_id,
            a1.question_5_id,
        ]
        a1.post_results(category=a1.category, questions=q1, answers=["A", "A", "A", "A", "A"])
        db.session.add(a1)
        db.session.commit()
        self.assertFalse(a1.question_1_result)
        self.assertTrue(a1.question_4_result)
        self.assertTrue(a1.timestamp < datetime.now())

    def test_post_score(self):
        pass
        # a1 = Attempt.query.filter_by(user_id=9999).first()
        # a1.post_score()
        # db.session.add(a1)
        # db.session.commit()
        # self.assertFalse(a1.score == 0)
        # self.assertTrue(a1.score == 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
