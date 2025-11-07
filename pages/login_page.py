from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class LoginPage:
    URL = "https://www.saucedemo.com/"

    def __init__(self, driver):
        self.driver = driver

    def open(self):
        self.driver.get(self.URL)

    def login(self, username, password):
        wait = WebDriverWait(self.driver, 15)
        user_input = wait.until(EC.presence_of_element_located((By.ID, "user-name")))
        pass_input = self.driver.find_element(By.ID, "password")
        login_btn = self.driver.find_element(By.ID, "login-button")


        user_input.clear()
        user_input.send_keys(username)
        pass_input.clear()
        pass_input.send_keys(password)
        login_btn.click()

        try:
            wait.until(EC.presence_of_element_located((By.ID, "react-burger-menu-btn")))
            time.sleep(3)  # thêm delay nhẹ sau khi login
        except:
            pass


