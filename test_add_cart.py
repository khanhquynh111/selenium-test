import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.login_page import LoginPage
from pages.cart_page import CartPage


@pytest.mark.usefixtures("driver")
class TestCart:

    def login_and_wait(self, driver):
        """Đăng nhập, dọn giỏ hàng về TRỐNG và chờ trang sản phẩm load."""
        login = LoginPage(driver)
        login.open()
        login.login("standard_user", "secret_sauce")

        # Chờ tới khi list sản phẩm hiển thị
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "inventory_list"))
        )

        # DỌN GIỎ HÀNG: để mỗi test luôn bắt đầu từ cart trống
        # Mở giỏ
        driver.find_element(By.ID, "shopping_cart_container").click()
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "cart_list"))
        )

        # Click tất cả nút "Remove" nếu có
        remove_buttons = driver.find_elements(By.XPATH, "//button[normalize-space()='Remove']")
        for btn in remove_buttons:
            btn.click()
            time.sleep(0.3)

        # Nếu có nút "Continue Shopping" thì bấm để về lại trang sản phẩm
        continue_btns = driver.find_elements(By.ID, "continue-shopping")
        if continue_btns:
            continue_btns[0].click()
        else:
            # fallback: dùng nút Back nếu không có continue-shopping
            driver.back()

        # Đảm bảo đã quay lại trang inventory
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "inventory_list"))
        )

        time.sleep(1)
        return CartPage(driver)

    def test_add_one_product(self, driver):
        """Người dùng đăng nhập và thêm 1 sản phẩm vào giỏ hàng."""
        cart = self.login_and_wait(driver)

        # Thêm 1 sản phẩm
        cart.add_product_to_cart("Sauce Labs Backpack")
        count = cart.get_cart_count()
        print(f"[DEBUG] Cart count = {count}")

        # Kỳ vọng: biểu tượng giỏ hàng hiển thị số 1
        assert count == 1, (
            "TC01 - EXPECTED: Biểu tượng giỏ hàng hiển thị số '1' sau khi thêm 1 sản phẩm.\n"
            f"ACTUAL: cart_count = {count}"
        )

        # Mở trang Cart và kiểm tra sản phẩm hiển thị
        cart.open_cart()
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "cart_list"))
        )
        names = [item.text.strip() for item in driver.find_elements(By.CLASS_NAME, "inventory_item_name")]
        print(f"[DEBUG] Items in cart = {names}")

        assert "Sauce Labs Backpack" in names, (
            "TC01 - EXPECTED: Sản phẩm 'Sauce Labs Backpack' được hiển thị trong giỏ hàng khi vào Cart.\n"
            f"ACTUAL: items = {names}"
        )

    def test_add_multiple_products(self, driver):
        """Thêm nhiều sản phẩm khác nhau."""
        cart = self.login_and_wait(driver)
        products = ["Sauce Labs Backpack", "Sauce Labs Bike Light", "Sauce Labs Bolt T-Shirt"]

        # Thêm nhiều sản phẩm
        for p in products:
            cart.add_product_to_cart(p)
            time.sleep(0.5)

        count = cart.get_cart_count()
        print(f"[DEBUG] Cart count = {count}")

        # Kỳ vọng: badge = 3
        assert count == len(products), (
            f"TC02 - EXPECTED: Giỏ hàng hiển thị số '{len(products)}' sau khi thêm {len(products)} sản phẩm.\n"
            f"ACTUAL: cart_count = {count}"
        )

        # Mở Cart kiểm tra danh sách
        cart.open_cart()
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "cart_list"))
        )
        names = [item.text.strip() for item in driver.find_elements(By.CLASS_NAME, "inventory_item_name")]
        print(f"[DEBUG] Items in cart = {names}")

        for p in products:
            assert p in names, (
                "TC02 - EXPECTED: Sản phẩm phải hiển thị đúng trong Cart.\n"
                f"MISSING: {p}\nACTUAL ITEMS: {names}"
            )


    def test_add_then_back_to_products(self, driver):
        """Thêm sản phẩm rồi quay lại trang Products."""
        cart = self.login_and_wait(driver)

        cart.add_product_to_cart("Sauce Labs Bike Light")
        count = cart.get_cart_count()
        print(f"[DEBUG] Cart count sau khi thêm = {count}")

        assert count == 1, (
            "TC03 - SETUP: Sau khi thêm 'Sauce Labs Bike Light', giỏ hàng phải hiển thị số 1.\n"
            f"ACTUAL: cart_count = {count}"
        )

        # Vào trang Cart
        cart.open_cart()
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "cart_list"))
        )
        assert cart.is_cart_page_displayed(), "TC04 - EXPECTED: Phải đang ở trang giỏ hàng trước khi Back."

        # Quay lại trang Products (nút back riêng trong app hoặc browser)
        cart.click_back_to_products()

        # Chờ trang Products hiển thị lại
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "inventory_list"))
        )

        # Nút của 'Sauce Labs Bike Light' phải là 'Remove'
        btn_text = cart.get_button_text("Sauce Labs Bike Light")
        print(f"[DEBUG] Nút sau khi back = {btn_text}")
        assert btn_text == "Remove", (
            "TC04 - EXPECTED: Sau khi quay lại trang Products, sản phẩm vẫn ở trạng thái 'Remove' "
            "(giỏ hàng không bị mất dữ liệu).\n"
            f"ACTUAL: button text = '{btn_text}'"
        )

        # Badge vẫn là 1
        count_after_back = cart.get_cart_count()
        print(f"[DEBUG] Cart count sau khi back = {count_after_back}")
        assert count_after_back == 1, (
            "TC03 - EXPECTED: Sau khi Back, giỏ vẫn giữ 1 sản phẩm.\n"
            f"ACTUAL: cart_count = {count_after_back}"
        )
