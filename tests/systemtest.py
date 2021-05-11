import unittest, os, time
from app import app, db
from app.models import Users, Progress, Attempt, Questions
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys


basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "test.db")


class AccessSystemTest(unittest.TestCase):
    driver = None

    def setUp(self):
        self.driver = webdriver.Firefox(executable_path=os.path.join(basedir, "geckodriver"))

        if not self.driver:
            self.skipTest("Web browser is not available")
        else:
            db.init_app(app)
            db.create_all()
            u1 = Users(id=9999, username="FirstSysTest", email="test-s1@peaksandtroughs.com")
            u1.set_password("systemTest1!")
            db.session.add(u1)
            db.session.commit()
            self.driver.maximize_window()
            self.driver.get("http://localhost:5000/")

    def tearDown(self):
        if self.driver:
            self.driver.close()
            db.session.remove()
            db.drop_all()

    def test_register_and_login(self):
        # Check user is not in the database
        u = Users.query.get(9999)
        self.assertEqual(u.username, "FirstSysTest", msg="user does not exist in database")

        self.driver.get("http://localhost:5000/register")
        self.driver.implicitly_wait(5)

        # Register new user
        username_field = self.driver.find_element_by_id("username")
        username_field.send_keys("SecondSysTest")
        email_field = self.driver.find_element_by_id("email")
        email_field.send_keys("test-s2@peaksandtroughs.com")
        password_field = self.driver.find_element_by_id("password")
        password_field.send_keys("systemTest2!")
        password2_field = self.driver.find_element_by_id("password2")
        password2_field.send_keys("systemTest2!")
        register = self.driver.find_element_by_id("submit")
        register.click()
        self.driver.implicitly_wait(5)

        # Login with new user
        username_field = self.driver.find_element_by_id("username")
        username_field.send_keys("SecondSysTest")
        password_field = self.driver.find_element_by_id("password")
        password_field.send_keys("systemTest2!")
        login = self.driver.find_element_by_id("submit")
        login.click()
        self.driver.implicitly_wait(5)

        # Check that the user is logged in and can logout
        nav_logout = self.driver.find_element_by_id("nav_logout")
        self.assertEqual(nav_logout.get_attribute("innerHTML"), "Logout", msg="user not logged in")

    def test_login(self):
        u = Users.query.get(9999)
        self.driver.get("http://localhost:5000/login")
        self.driver.implicitly_wait(5)

        # Login user
        username_field = self.driver.find_element_by_id("username")
        username_field.send_keys(u.username)
        password_field = self.driver.find_element_by_id("password")
        password_field.send_keys("systemTest1!")
        login = self.driver.find_element_by_id("submit")
        login.click()
        self.driver.implicitly_wait(5)

        # Check that the user is logged in and can logout
        nav_logout = self.driver.find_element_by_id("nav_logout")
        self.assertEqual(nav_logout.get_attribute("innerHTML"), "Logout", msg="user not logged in")

    def test_failed_login(self):
        u = Users.query.get(9999)
        self.driver.get("http://localhost:5000/login")
        self.driver.implicitly_wait(5)

        # Login with user with incorrect credentials
        username_field = self.driver.find_element_by_id("username")
        username_field.send_keys(u.username)
        password_field = self.driver.find_element_by_id("password")
        password_field.send_keys("systemTest2!")
        login = self.driver.find_element_by_id("submit")
        login.click()
        self.driver.implicitly_wait(5)

        # Check that the user is not logged in
        nav_login = self.driver.find_element_by_id("nav_login")
        self.assertEqual(nav_login.get_attribute("innerHTML"), "Login", msg="user has logged in")


class NavigationSystemTest(unittest.TestCase):
    driver = None

    def setUp(self):
        self.driver = webdriver.Firefox(executable_path=os.path.join(basedir, "geckodriver"))

        uname = "FirstSysTest"
        pwd = "systemTest1!"

        if not self.driver:
            self.skipTest("Web browser is not available")
        else:
            db.init_app(app)
            db.create_all()
            u1 = Users(id=9999, username=uname, email="test-s1@peaksandtroughs.com")
            progress = Progress(user_id=9999)
            u1.set_password(pwd)
            db.session.add(u1)
            db.session.add(progress)
            db.session.commit()
            self.driver.maximize_window()
            self.driver.get("http://localhost:5000/login")

            username_field = self.driver.find_element_by_id("username")
            username_field.send_keys(u1.username)
            password_field = self.driver.find_element_by_id("password")
            password_field.send_keys(pwd)
            login = self.driver.find_element_by_id("submit")
            login.click()
            self.driver.implicitly_wait(5)

    def tearDown(self):
        if self.driver:
            self.driver.close()
            db.session.remove()
            db.drop_all()

    def test_learn_progress(self):
        u = Users.query.get(9999)
        self.driver.get("http://localhost:5000/learn")
        self.driver.implicitly_wait(5)

        p1 = Progress.query.filter_by(user_id=u.id).first()
        self.assertFalse(p1.high_a)

        # Navigate to High Risk content
        high = self.driver.find_element_by_id("high")
        high.click()
        self.driver.implicitly_wait(5)

        # Naviagte to Stocks content
        high_a_box = self.driver.find_element_by_id("high_a_box")
        high_a_box.click()
        self.driver.implicitly_wait(5)

        # Scroll through content and submit progress feedback for Stocks content
        high_a = self.driver.find_element_by_id("high_a")
        high_a.send_keys(Keys.PAGE_DOWN)
        high_a.click()  # THIS FAILS FOR SOME REASON
        self.driver.implicitly_wait(5)

        # Check that progress has been reflected in database
        p2 = Progress.query.filter_by(user_id=u.id).first()
        self.assertTrue(p2.high_a)  # NOT CORRECT RESULT

    def test_access_feedback_locked(self):
        u = Users.query.get(9999)
        self.driver.get("http://localhost:5000/feedback")
        self.driver.implicitly_wait(5)

        # Attempt to navigate to feedback
        feedback = self.driver.find_element_by_id("feedback")
        feedback.click()
        self.driver.implicitly_wait(5)

        # Check to see if still on index page
        feedback2 = self.driver.find_element_by_id("feedback")
        self.assertEqual(
            feedback2.get_attribute("innerHTML"), "Feedback", msg="no longer on index page"
        )

    def test_assessment_and_feedback(self):
        u = Users.query.get(9999)
        self.driver.get("http://localhost:5000/assessment")
        self.driver.implicitly_wait(5)

        # Submit assessment with no answers
        submit = self.driver.find_element_by_id("submit")
        submit.click()
        self.driver.implicitly_wait(5)

        # Check to see still at the assessment page
        page = self.driver.find_element_by_id("assessment_title")
        self.assertEqual(
            page.get_attribute("innerHTML"), "Complete Assessment", msg="no longer at assessment"
        )
        self.driver.implicitly_wait(5)

        # Select assessment answers
        select_1 = Select(self.driver.find_element_by_id("answer_1"))
        select_1.select_by_value("A")
        select_2 = Select(self.driver.find_element_by_id("answer_2"))
        select_2.select_by_value("A")
        select_3 = Select(self.driver.find_element_by_id("answer_3"))
        select_3.select_by_value("A")
        select_4 = Select(self.driver.find_element_by_id("answer_4"))
        select_4.select_by_value("A")
        select_5 = Select(self.driver.find_element_by_id("answer_5"))
        select_5.select_by_value("A")
        submit.click()
        self.driver.implicitly_wait(5)

        # Navigate to Feedback
        self.driver.get("http://localhost:5000/index")
        self.driver.implicitly_wait(5)

        feedback = self.driver.find_element_by_id("feedback")
        feedback.click()
        self.driver.implicitly_wait(5)

        # Check to see if on feedback page with latest results
        self.assertTrue(self.driver.find_element_by_id("table_results"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
