import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CheckoutPage:
    FIRSTNAME_INPUT = (By.ID, "first-name")
    LASTNAME_INPUT = (By.ID, "last-name")
    ZIP_INPUT = (By.ID, "postal-code")
    CONTINUE_BTN = (By.ID, "continue")
    CANCEL_BTN = (By.ID, "cancel")
    FINISH_BTN = (By.ID, "finish")
    ERROR_MSG = (By.CSS_SELECTOR, "h3[data-test='error']")
    BACK_HOME_BTN = (By.ID, "back-to-products")
    CHECKOUT_BTN = (By.ID, "checkout")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def click_checkout(self):
        """Bấm nút Checkout từ trang Cart."""
        btn = self.wait.until(EC.element_to_be_clickable(self.CHECKOUT_BTN))
        btn.click()
        time.sleep(1.5)

    def fill_information(self, firstname="", lastname="", zipcode=""):
        """Nhập thông tin người dùng (có thể để trống)."""
        self.wait.until(EC.presence_of_element_located(self.FIRSTNAME_INPUT))

        fn = self.driver.find_element(*self.FIRSTNAME_INPUT)
        ln = self.driver.find_element(*self.LASTNAME_INPUT)
        zp = self.driver.find_element(*self.ZIP_INPUT)

        fn.clear()
        fn.send_keys(firstname)
        ln.clear()
        ln.send_keys(lastname)
        zp.clear()
        zp.send_keys(zipcode)
        time.sleep(1)

    def click_continue(self):
        """Bấm nút Continue."""
        btn = self.wait.until(EC.element_to_be_clickable(self.CONTINUE_BTN))
        btn.click()
        time.sleep(1.5)

    def click_cancel(self):
        """Bấm Cancel để quay lại giỏ hàng."""
        btn = self.wait.until(EC.element_to_be_clickable(self.CANCEL_BTN))
        btn.click()
        time.sleep(1.5)

    def click_finish(self):
        """Hoàn tất thanh toán."""
        btn = self.wait.until(EC.element_to_be_clickable(self.FINISH_BTN))
        btn.click()
        time.sleep(1.5)

    def get_error_message(self):
        """Trả về lỗi nếu có."""
        try:
            msg = self.driver.find_element(*self.ERROR_MSG)
            return msg.text.strip()
        except:
            return None

    def back_to_products(self):
        """Bấm nút Back Home sau khi hoàn tất."""
        try:
            btn = self.wait.until(EC.element_to_be_clickable(self.BACK_HOME_BTN))
            btn.click()
            time.sleep(1.5)
        except:
            pass
