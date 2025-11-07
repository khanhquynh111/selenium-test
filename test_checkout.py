import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.login_page import LoginPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage


@pytest.mark.usefixtures("driver")
class TestCheckout:

    def login_and_go_to_cart(self, driver):
        """Đăng nhập, thêm 1 sản phẩm vào giỏ và mở trang giỏ hàng."""
        login = LoginPage(driver)
        login.open()
        login.login("standard_user", "secret_sauce")

        # Đợi trang inventory load (dựa vào DOM, không dùng url_contains)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "inventory_list"))
        )

        cart = CartPage(driver)
        cart.add_product_to_cart("Sauce Labs Backpack")

        cart.open_cart()

        # Đợi trang cart: dựa vào cart_list
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "cart_list"))
        )

        return CheckoutPage(driver)

    # TC: Nhập đầy đủ thông tin hợp lệ và bấm Continue → sang Checkout Overview
    def test_checkout_valid_info(self, driver):
        checkout = self.login_and_go_to_cart(driver)
        checkout.click_checkout()

        # Đợi trang Checkout: Your Information (step 1)
        WebDriverWait(driver, 10).until(EC.url_contains("checkout-step-one"))

        # Nhập thông tin hợp lệ
        checkout.fill_information("John", "Doe", "700000")
        checkout.click_continue()

        # Đợi chuyển sang trang Checkout Overview (step 2)
        WebDriverWait(driver, 10).until(EC.url_contains("checkout-step-two"))
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "summary_total_label"))
        )

        actual_url = driver.current_url
        cart_items = driver.find_elements(By.CLASS_NAME, "cart_item")

        assert "checkout-step-two" in actual_url, (
            "TC01 - EXPECTED: Sau khi nhập thông tin hợp lệ và bấm Continue, "
            "hệ thống chuyển sang trang Checkout Overview.\n"
            f"ACTUAL URL: {actual_url}"
        )
        assert len(cart_items) > 0, (
            "TC01 - EXPECTED: Trang Checkout Overview hiển thị danh sách sản phẩm.\n"
            f"ACTUAL: số sản phẩm hiển thị = {len(cart_items)}"
        )

    # TC: Để trống tất cả các trường → lỗi “Error: First Name is required”
    def test_checkout_empty_fields(self, driver):
        checkout = self.login_and_go_to_cart(driver)
        checkout.click_checkout()

        WebDriverWait(driver, 10).until(EC.url_contains("checkout-step-one"))

        checkout.fill_information("", "", "")
        checkout.click_continue()

        error_el = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-test='error']"))
        )
        error_text = error_el.text.strip()

        expected_error = "Error: First Name is required"
        assert error_text == expected_error, (
            "TC02 - EXPECTED: Để trống tất cả các trường và bấm Continue, "
            "hiển thị thông báo lỗi: 'Error: First Name is required'.\n"
            f"EXPECTED: {expected_error}\nACTUAL:   {error_text}"
        )

    # TC: Chỉ nhập First Name và Zip Code → thiếu Last Name
    def test_checkout_missing_lastname(self, driver):
        checkout = self.login_and_go_to_cart(driver)
        checkout.click_checkout()

        WebDriverWait(driver, 10).until(EC.url_contains("checkout-step-one"))

        checkout.fill_information("John", "", "700000")
        checkout.click_continue()

        error_el = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-test='error']"))
        )
        error_text = error_el.text.strip()

        expected_error = "Error: Last Name is required"
        assert error_text == expected_error, (
            "TC03 - EXPECTED: Chỉ nhập First Name và Zip Code, hệ thống báo thiếu Last Name.\n"
            f"EXPECTED: {expected_error}\nACTUAL:   {error_text}"
        )

    # TC: Nhập First + Last Name, bỏ trống Zip Code
    def test_checkout_missing_zipcode(self, driver):
        checkout = self.login_and_go_to_cart(driver)
        checkout.click_checkout()

        WebDriverWait(driver, 10).until(EC.url_contains("checkout-step-one"))

        checkout.fill_information("John", "Doe", "")
        checkout.click_continue()

        error_el = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-test='error']"))
        )
        error_text = error_el.text.strip()

        expected_error = "Error: Postal Code is required"
        assert error_text == expected_error, (
            "TC04 - EXPECTED: Nhập First và Last Name nhưng bỏ trống Zip Code, "
            "hệ thống báo 'Error: Postal Code is required'.\n"
            f"EXPECTED: {expected_error}\nACTUAL:   {error_text}"
        )

    # TC: Bấm nút Cancel tại trang Checkout → quay về Cart
    def test_checkout_cancel_button(self, driver):
        checkout = self.login_and_go_to_cart(driver)
        checkout.click_checkout()

        WebDriverWait(driver, 10).until(EC.url_contains("checkout-step-one"))

        checkout.click_cancel()

        # Kỳ vọng quay lại trang giỏ hàng
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "cart_list"))
        )
        actual_url = driver.current_url

        assert "cart" in actual_url, (
            "TC05 - EXPECTED: Bấm Cancel tại trang Checkout, hệ thống quay lại trang Cart.\n"
            f"ACTUAL URL: {actual_url}"
        )

    # TC: Bấm Finish để hoàn tất thanh toán → Checkout Complete
    def test_checkout_finish(self, driver):
        checkout = self.login_and_go_to_cart(driver)
        checkout.click_checkout()

        WebDriverWait(driver, 10).until(EC.url_contains("checkout-step-one"))

        checkout.fill_information("Jane", "Smith", "11111")
        checkout.click_continue()

        WebDriverWait(driver, 10).until(EC.url_contains("checkout-step-two"))

        checkout.click_finish()

        # Đợi trang Checkout Complete
        WebDriverWait(driver, 10).until(EC.url_contains("checkout-complete"))
        complete_header = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "complete-header"))
        )

        actual_url = driver.current_url
        assert "checkout-complete" in actual_url, (
            "TC06 - EXPECTED: Bấm Finish, hệ thống chuyển sang trang Checkout Complete.\n"
            f"ACTUAL URL: {actual_url}"
        )
        assert complete_header.is_displayed(), (
            "TC06 - EXPECTED: Trang Checkout Complete hiển thị trạng thái hoàn tất.\n"
            "ACTUAL: complete-header không hiển thị."
        )

    # TC: Không có sản phẩm trong giỏ nhưng bấm Checkout
    # Theo spec: Kỳ vọng KHÔNG cho tiếp tục → nhưng thực tế app Swag Labs cho đi tiếp.
    # Đánh dấu xfail để thể hiện bug, không làm đỏ cả suite.
    @pytest.mark.xfail(reason="Ứng dụng cho phép checkout khi giỏ trống (khác spec)")
    def test_checkout_empty_cart(self, driver):
        login = LoginPage(driver)
        login.open()
        login.login("standard_user", "secret_sauce")

        # Chờ inventory load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "inventory_list"))
        )

        # Vào cart trực tiếp, không dùng CartPage.open_cart (tránh wait theo URL)
        driver.find_element(By.ID, "shopping_cart_container").click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "cart_list"))
        )

        # Đảm bảo giỏ hàng trống
        cart_items = driver.find_elements(By.CLASS_NAME, "cart_item")
        assert len(cart_items) == 0, (
            "TC07 - SETUP: Giỏ hàng phải trống trước khi test.\n"
            f"ACTUAL: số sản phẩm trong giỏ = {len(cart_items)}"
        )

        checkout = CheckoutPage(driver)
        checkout.click_checkout()

        # Kỳ vọng theo spec: không cho tiếp tục (vẫn ở trang cart hoặc báo lỗi)
        actual_url = driver.current_url
        on_checkout_info = "checkout-step-one" in actual_url

        assert not on_checkout_info, (
            "TC07 - EXPECTED: Không có sản phẩm trong giỏ nhưng bấm Checkout, "
            "hệ thống không cho phép tiếp tục hoặc hiển thị lỗi.\n"
            "ACTUAL: Hệ thống vẫn chuyển sang trang Checkout (checkout-step-one)."
        )

    # TC: Nhấn Back trên trình duyệt sau khi hoàn tất thanh toán
    # Kỳ vọng: quay lại được, nhưng không thể tiếp tục thanh toán với sản phẩm cụ thể đó nữa (giỏ trống).
    def test_checkout_back_after_finish(self, driver):
        checkout = self.login_and_go_to_cart(driver)
        checkout.click_checkout()

        WebDriverWait(driver, 10).until(EC.url_contains("checkout-step-one"))

        checkout.fill_information("John", "Doe", "700000")
        checkout.click_continue()

        WebDriverWait(driver, 10).until(EC.url_contains("checkout-step-two"))

        checkout.click_finish()

        WebDriverWait(driver, 15).until(EC.url_contains("checkout-complete"))

        # Nhấn Back trên trình duyệt (quay về 1 bước trong history)
        driver.back()

        # Đợi lại trang Checkout Overview
        WebDriverWait(driver, 10).until(EC.url_contains("checkout-step-two"))
        summary_label = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "summary_total_label"))
        )

        # Không còn sản phẩm nào trong bill
        cart_items = driver.find_elements(By.CLASS_NAME, "cart_item")
        assert len(cart_items) == 0, (
            "TC09 - EXPECTED: Sau khi hoàn tất thanh toán và nhấn Back, "
            "bill không còn sản phẩm nào.\n"
            f"ACTUAL: số dòng sản phẩm trên bill = {len(cart_items)}"
        )

        # Tổng tiền = 0
        total_text = summary_label.text.strip()
        assert "Total: $0.00" in total_text, (
            "TC08 - EXPECTED: Tổng tiền trên bill sau khi Back phải là 0 (Total: $0.00).\n"
            f"ACTUAL: {total_text}"
        )
