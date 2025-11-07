import pytest
import time
from selenium.webdriver.common.by import By
from pages.login_page import LoginPage


# Tạo độ trễ chung cho mỗi case
DELAY = 2.5


@pytest.mark.usefixtures("driver")
class TestLogin:
   # Login with valid credentials
   def test_login_valid(self, driver):
       page = LoginPage(driver)
       page.open()
       page.login("standard_user", "secret_sauce")
       time.sleep(DELAY)
       assert "inventory.html" in driver.current_url, \
           " Đăng nhập hợp lệ nhưng không vào trang Products"
   # Login with incorrect password
   def test_login_incorrect_password(self, driver):
       page = LoginPage(driver)
       page.open()
       page.login("standard_user", "123456")
       time.sleep(DELAY)
       error = driver.find_element(By.CSS_SELECTOR, "[data-test='error']").text
       assert "Username and password do not match" in error, \
           "Sai mật khẩu nhưng không hiện lỗi đúng"
   # Login with empty username & password
   def test_login_empty_username_password(self, driver):
       page = LoginPage(driver)
       page.open()
       page.login("", "")
       time.sleep(DELAY)
       error = driver.find_element(By.CSS_SELECTOR, "[data-test='error']").text
       assert "Username is required" in error, \
           "Không hiện lỗi khi để trống username"
   # Login with uppercase username/password
   def test_login_uppercase_credentials(self, driver):
       page = LoginPage(driver)
       page.open()
       page.login("Standard_user", "Secret_sauce")
       time.sleep(DELAY)
       # Trường hợp sai hoa thường → không vào được inventory
       assert "inventory.html" not in driver.current_url, \
           "Nhập sai chữ hoa/thường mà vẫn login thành công"


   # Login with locked_out_user
   def test_login_locked_out_user(self, driver):
       page = LoginPage(driver)
       page.open()
       page.login("locked_out_user", "secret_sauce")
       time.sleep(DELAY)
       error = driver.find_element(By.CSS_SELECTOR, "[data-test='error']").text
       assert "Sorry, this user has been locked out" in error, \
           "Locked_out_user mà không hiện thông báo lỗi đúng"


   # Login with problem_user
   def test_login_problem_user(self, driver):
       page = LoginPage(driver)
       page.open()
       page.login("problem_user", "secret_sauce")
       time.sleep(DELAY)
       assert "inventory.html" in driver.current_url, \
           "Problem_user không đăng nhập được vào Products"


   # Login with performance_glitch_user
   def test_login_performance_glitch_user(self, driver):
       page = LoginPage(driver)
       page.open()
       page.login("performance_glitch_user", "secret_sauce")
       time.sleep(DELAY)
       assert "inventory.html" in driver.current_url, \
           "Performance_glitch_user không vào trang Products"
   # Login with error_user
   def test_login_error_user(self, driver):
       page = LoginPage(driver)
       page.open()
       page.login("error_user", "secret_sauce")
       time.sleep(DELAY)
       assert "inventory.html" in driver.current_url, \
           "Error_user không vào trang Products"


   # Login with visual_user
   def test_login_visual_user(self, driver):
       page = LoginPage(driver)
       page.open()
       page.login("visual_user", "secret_sauce")
       time.sleep(DELAY)
       assert "inventory.html" in driver.current_url, \
           "Visual_user không vào trang Products"
