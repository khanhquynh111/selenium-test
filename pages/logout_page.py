# pages/logout_page.py
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LogoutPage:
    MENU_BTN = (By.ID, "react-burger-menu-btn")
    LOGOUT_LINK = (By.ID, "logout_sidebar_link")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open_menu(self):
        """Bấm vào nút menu và chờ menu hiện ra."""
        self.wait.until(EC.element_to_be_clickable(self.MENU_BTN)).click()
        # Có thể giữ hoặc bỏ sleep, tuỳ app có animation hay không
        time.sleep(0.5)

    def logout(self):
        """Bấm nút logout từ menu."""
        self.wait.until(EC.element_to_be_clickable(self.LOGOUT_LINK)).click()
        # Chờ trang login tải xong
        # (có thể dùng wait login-button ở đây luôn, nhưng mình để trong flow)
        time.sleep(0.5)

    def logout_flow(self):
        """Thực hiện toàn bộ quy trình logout (mở menu → logout)."""
        self.open_menu()
        self.logout()

        # Đợi form login xuất hiện để đảm bảo logout thành công
        self.wait.until(
            EC.presence_of_element_located((By.ID, "login-button"))
        )

    def is_logged_in(self):
        """Kiểm tra có đang ở inventory page (dành cho assert nếu cần)."""
        return "inventory.html" in self.driver.current_url
