import unittest, os, time
from app import app, db
from app.models import Users, Progress, Attempt, Questions
from selenium import webdriver


basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "test.db")


class SystemTest(unittest.TestCase):
    driver = None

    def setUp(self):
        self.driver = webdriver.Firefox(executable_path=os.path.join(basedir, "geckodriver"))

        if not self.driver:
            self.skipTest("Web browser is not available")
        else:
            db.init_app(app)
            db.create_all()
            u1 = Users(id=9999, username="FirstSysTest", email="test-s1@peaksandtroughs.com")
            u1.set_password("systemtest1")
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
        u = Users.query.get(9999)
        self.assertEqual(u.username, "FirstSysTest", msg="user does not exist in database")

        self.driver.get("http://localhost:5000/register")
        self.driver.implicitly_wait(5)

        username_field = self.driver.find_element_by_id("username")
        username_field.send_keys("SecondSysTest")
        email_field = self.driver.find_element_by_id("email")
        email_field.send_keys("test-s2@peaksandtroughs.com")
        password_field = self.driver.find_element_by_id("password")
        password_field.send_keys("systemtest2")
        password2_field = self.driver.find_element_by_id("password2")
        password2_field.send_keys("systemtest2")
        register = self.driver.find_element_by_id("submit")
        register.click()
        self.driver.implicitly_wait(5)

        username_field = self.driver.find_element_by_id("username")
        username_field.send_keys("SecondSysTest")
        password_field = self.driver.find_element_by_id("password")
        password_field.send_keys("systemtest2")
        login = self.driver.find_element_by_id("submit")
        login.click()
        self.driver.implicitly_wait(5)

        nav_logout = self.driver.find_element_by_id("nav_logout")
        self.assertEqual(nav_logout.get_attribute("innerHTML"), "Logout", msg="user not logged in")

    def test_login(self):
        u = Users.query.get(9999)
        self.driver.get("http://localhost:5000/login")
        self.driver.implicitly_wait(5)

        username_field = self.driver.find_element_by_id("username")
        username_field.send_keys(u.username)
        password_field = self.driver.find_element_by_id("password")
        password_field.send_keys("systemtest1")
        login = self.driver.find_element_by_id("submit")
        login.click()
        self.driver.implicitly_wait(5)

        nav_logout = self.driver.find_element_by_id("nav_logout")
        self.assertEqual(nav_logout.get_attribute("innerHTML"), "Logout", msg="user not logged in")

    def test_failed_login(self):
        u = Users.query.get(9999)
        self.driver.get("http://localhost:5000/login")
        self.driver.implicitly_wait(5)

        username_field = self.driver.find_element_by_id("username")
        username_field.send_keys(u.username)
        password_field = self.driver.find_element_by_id("password")
        password_field.send_keys("systemtest2")
        login = self.driver.find_element_by_id("submit")
        login.click()
        self.driver.implicitly_wait(5)

        nav_login = self.driver.find_element_by_id("nav_login")
        self.assertEqual(nav_login.get_attribute("innerHTML"), "Login", msg="user has logged in")


if __name__ == "__main__":
    unittest.main(verbosity=2)
