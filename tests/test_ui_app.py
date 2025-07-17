import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time

class LoginUITest(unittest.TestCase):
    def setUp(self):
        options = Options()
        options.add_argument("--headless")  # Execute without GUI
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(options=options)
        self.base_url = "http://localhost:8081"

    def login(self):
        self.driver.get(f"{self.base_url}/login")
        time.sleep(1)

        # fill the form
        self.driver.find_element(By.NAME, "username").send_keys("CARLOS")
        self.driver.find_element(By.NAME, "password").send_keys("carlos123")
        self.driver.find_element(By.NAME, "login").click()
        time.sleep(1)

    def test_login_page_shows_dashboard(self):
        self.login()
        self.assertIn("Dashboard", self.driver.page_source)

    def test_logout_redirects_to_login(self):
        self.login()
        self.driver.get(f"{self.base_url}/logout")
        time.sleep(1)
        self.assertIn("Login", self.driver.page_source)

    def test_dashboard_access(self):
        self.login()
        self.driver.get(f"{self.base_url}/dashboard")
        time.sleep(1)
        self.assertIn("Dashboard", self.driver.page_source)

    def test_users_list_access(self):
        self.login()
        self.driver.get(f"{self.base_url}/users")
        time.sleep(1)
        self.assertIn("Users", self.driver.page_source)

    #def test_register_page_exists(self):
    #    self.driver.get(f"{self.base_url}/register")
    #    time.sleep(1)
    #    self.assertIn("Register", self.driver.page_source)

    def tearDown(self):
        self.driver.quit()

if __name__ == '__main__':
    unittest.main()

