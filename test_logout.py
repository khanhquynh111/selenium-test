import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.login_page import LoginPage
from pages.logout_page import LogoutPage


@pytest.mark.usefixtures("driver")
class TestLogout:

    def test_logout_valid(self, driver):
        """TC01: Đăng nhập thành công → chọn Logout → quay về trang login."""
        login = LoginPage(driver)
        login.open()
        login.login("standard_user", "secret_sauce")

        # Đảm bảo đã login (thấy inventory_list)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "inventory_list"))
        )

        logout = LogoutPage(driver)
        logout.logout_flow()  # trong này đã chờ login-button xuất hiện

        # Nếu muốn rõ ràng, chờ lại và GÁN vào biến
        login_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "login-button"))
        )
        time.sleep(1)

        # Kết quả thực tế
        actual_url = driver.current_url

        # So sánh với kỳ vọng
        expected_url = "https://www.saucedemo.com/"
        assert actual_url == expected_url, (
            "TC01 - EXPECTED: Sau khi bấm Logout, hệ thống quay lại trang login.\n"
            f"EXPECTED URL: {expected_url}\nACTUAL URL:   {actual_url}"
        )
        assert login_button.is_displayed(), (
            "TC01 - EXPECTED: Trang login hiển thị (nút Login nhìn thấy).\n"
            "ACTUAL: login-button không hiển thị."
        )

    def test_logout_back_button(self, driver):
        """TC02: Logout → nhấn nút Back trên trình duyệt."""
        login = LoginPage(driver)
        login.open()
        login.login("standard_user", "secret_sauce")

        # Đảm bảo đã login
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "inventory_list"))
        )

        logout = LogoutPage(driver)
        logout.logout_flow()

        # chờ form login & gán biến
        login_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "login-button"))
        )
        assert login_button.is_displayed(), "TC02 - Sau khi logout xong phải ở trang login."
        time.sleep(1)

        # nhấn back
        driver.back()
        time.sleep(2)

        # chờ xem login form vẫn hiển thị & gán lại biến
        login_button = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, "login-button"))
        )
        time.sleep(1)
        actual_url = driver.current_url

        # Kỳ vọng: vẫn phải login lại (tức là vẫn ở trang login, không quay về Products)
        assert login_button.is_displayed(), (
            "TC02 - EXPECTED: Sau khi Logout rồi bấm Back, hệ thống vẫn yêu cầu đăng nhập lại "
            "(trang login hiển thị).\n"
            "ACTUAL: login-button không hiển thị."
        )
        assert "inventory" not in actual_url.lower(), (
            "TC02 - EXPECTED: Người dùng không thể quay lại trang Products chỉ bằng nút Back sau khi logout.\n"
            f"ACTUAL URL: {actual_url}"
        )

    def test_logout_direct_url(self, driver):
        """TC03: Logout xong → truy cập inventory.html trực tiếp."""
        login = LoginPage(driver)
        login.open()
        login.login("standard_user", "secret_sauce")

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "inventory_list"))
        )

        logout = LogoutPage(driver)
        logout.logout_flow()

        # truy cập trực tiếp inventory
        driver.get("https://www.saucedemo.com/inventory.html")
        time.sleep(2)

        # đợi login page hiện lại & gán biến
        login_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "login-button"))
        )
        time.sleep(1)
        actual_url = driver.current_url

        assert login_button.is_displayed(), (
            "TC03 - EXPECTED: Khi truy cập trực tiếp /inventory.html sau khi logout, "
            "hệ thống chuyển hướng đến trang login.\n"
            "ACTUAL: login-button không hiển thị."
        )
        assert "inventory" not in actual_url.lower(), (
            "TC03 - EXPECTED: Không thể truy cập trang 'Products' nếu chưa đăng nhập lại.\n"
            f"ACTUAL URL: {actual_url}"
        )

    @pytest.mark.xfail(reason="Ứng dụng không đồng bộ logout giữa nhiều tab")
    def test_logout_multi_tab(self, driver):
        """TC04: Đăng nhập ở tab 1 → mở tab 2 → logout tab 1 → refresh tab 2."""
        login = LoginPage(driver)
        login.open()
        login.login("standard_user", "secret_sauce")

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "inventory_list"))
        )

        # mở tab 2
        driver.execute_script(
            "window.open('https://www.saucedemo.com/inventory.html','_blank');"
        )
        tabs = driver.window_handles

        # tab 1 → logout
        driver.switch_to.window(tabs[0])
        logout = LogoutPage(driver)
        logout.logout_flow()

        # tab 2 → refresh
        driver.switch_to.window(tabs[1])
        driver.refresh()
        time.sleep(2)

        login_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "login-button"))
        )
        actual_url = driver.current_url

        assert login_button.is_displayed(), (
            "TC04 - EXPECTED: Khi refresh tab 2 sau khi đã logout ở tab 1, "
            "hệ thống phải yêu cầu login lại (trang login hiển thị).\n"
            "ACTUAL: login-button không hiển thị."
        )
        assert "inventory" not in actual_url.lower(), (
            "TC04 - EXPECTED: Session bị invalidate toàn bộ, tab 2 không thể ở trang Products.\n"
            f"ACTUAL URL: {actual_url}"
        )
