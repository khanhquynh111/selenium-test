# tests/test_inventory.py
import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.login_page import LoginPage
from pages.inventoryview_page import InventoryPageView


class TestViewProduct:

    @pytest.mark.usefixtures("driver")
    def test_view_product_detail(self, driver):
        """TC01: Nhấn vào tên sản phẩm bất kỳ để xem chi tiết"""
        login = LoginPage(driver)
        login.open()
        login.login("standard_user", "secret_sauce")

        # ✅ Chờ có sản phẩm hiển thị (ổn định hơn so với URL)
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "inventory_item_name"))
        )
        view = InventoryPageView(driver)

        view.click_product_by_name("Sauce Labs Backpack")
        assert "inventory-item" in driver.current_url

    def test_back_to_products(self, driver):
        """TC02: Từ trang chi tiết, nhấn “Back to products”"""
        login = LoginPage(driver)
        login.open()
        login.login("standard_user", "secret_sauce")

        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "inventory_item_name"))
        )
        view = InventoryPageView(driver)
        view.click_product_by_name("Sauce Labs Backpack")
        view.click_back_to_products()

        # ✅ Kiểm tra phần tử trên trang products thay vì chỉ URL
        assert EC.presence_of_element_located((By.CLASS_NAME, "inventory_item"))(
            driver
        )

    def test_sort_name_az(self, driver):
        """TC03: Kiểm tra sắp xếp từ A–Z"""
        login = LoginPage(driver)
        login.open()
        login.login("standard_user", "secret_sauce")

        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "product_sort_container"))
        )
        view = InventoryPageView(driver)

        view.select_sort_option("Name (A to Z)")
        names = view.get_all_product_names()
        assert names == sorted(names)

    def test_sort_name_za(self, driver):
        """TC04: Kiểm tra sắp xếp từ Z–A"""
        login = LoginPage(driver)
        login.open()
        login.login("standard_user", "secret_sauce")

        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "product_sort_container"))
        )
        view = InventoryPageView(driver)

        view.select_sort_option("Name (Z to A)")
        names = view.get_all_product_names()
        assert names == sorted(names, reverse=True)

    def test_sort_price_low_high(self, driver):
        """TC05: Kiểm tra sắp xếp theo giá tăng dần"""
        login = LoginPage(driver)
        login.open()
        login.login("standard_user", "secret_sauce")

        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "product_sort_container"))
        )
        view = InventoryPageView(driver)

        view.select_sort_option("Price (low to high)")
        prices = view.get_all_product_prices()
        assert prices == sorted(prices)

    def test_sort_price_high_low(self, driver):
        """TC06: Kiểm tra sắp xếp theo giá giảm dần"""
        login = LoginPage(driver)
        login.open()
        login.login("standard_user", "secret_sauce")

        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "product_sort_container"))
        )
        view = InventoryPageView(driver)

        view.select_sort_option("Price (high to low)")
        prices = view.get_all_product_prices()
        assert prices == sorted(prices, reverse=True)

    def test_click_product_image(self, driver):
        """TC07: Nhấn vào hình sản phẩm"""
        login = LoginPage(driver)
        login.open()
        login.login("standard_user", "secret_sauce")

        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "inventory_item_img"))
        )
        view = InventoryPageView(driver)

        view.click_product_image("Sauce Labs Bike Light")
        assert "inventory-item" in driver.current_url

    def test_direct_url_without_login(self, driver):
        """TC08: Nhập thủ công URL sản phẩm khi chưa login"""
        driver.delete_all_cookies()  # Đảm bảo chưa login
        driver.get("https://www.saucedemo.com/inventory-item.html?id=4")
        time.sleep(2)

        # ✅ Kiểm tra có hiển thị ô login thay vì chỉ URL
        login_box = driver.find_elements(By.ID, "login-button")
        assert len(login_box) > 0, "Không chuyển về trang login khi chưa đăng nhập!"
