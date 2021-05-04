import unittest, os
from app import app, db
from app.models import Users, Progress, Attempt, Questions


class UserModelCase(unittest.TestCase):
    def set_up(self):
        self.app = app.test_client()
        user1 = Users(id=9999, username="FirstTest", email="test1@peaksandtroughs.com")
        user2 = Users(id=9998, username="SecondTest", email="test2@peaksandtroughs.com")
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()

    def tear_down(self):
        db.session.delete(user1)
        db.session.delete(user2)
        db.session.commit()

    def test_password_hashing(self):
        u1 = Users.query.get(9999)
        u1.set_password("testmypassword")
        self.assertFalse(u1.check_password("notmypassword"))
        self.assertTrue(u1.check_password("testmypassword"))

    def test_is_committed(self):
        pass


class ProgressModelCase(unittest.TestCase):
    def set_up(self):
        self.app = app.test_client()
        user1 = Users(id=9999, username="FirstTest", email="test1@peaksandtroughs.com")
        progress1 = Progress(user_id=9999)
        db.session.add(user1)
        db.session.add(progress1)
        db.session.commit()

    def tear_down(self):
        db.session.delete(user1)
        db.session.delete(progress1)
        db.session.commit()


class AttemptModelCase(unittest.TestCase):
    def set_up(self):
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

    def tear_down(self):
        db.session.delete(user1)
        db.session.delete(attempt1)
        db.session.commit()

    def test_calculate_results(self):
        pass

    def test_post_results(self):
        pass

    def test_post_score(self):
        pass


if __name__ == "__main__":
    unittest.main(verbosity=2)
