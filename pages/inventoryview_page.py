# pages/inventory_page_view.py
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class InventoryPageView:
    PRODUCT_TITLE = (By.CLASS_NAME, "inventory_item_name")
    PRODUCT_IMAGE = (By.CLASS_NAME, "inventory_item_img")
    SORT_SELECT = (By.CLASS_NAME, "product_sort_container")
    BACK_BTN = (By.ID, "back-to-products")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def click_product_by_name(self, name="Sauce Labs Backpack"):
        """Nhấn vào tên sản phẩm"""
        product = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, f"//div[text()='{name}']"))
        )
        product.click()
        time.sleep(3)

    def click_product_image(self, alt="Sauce Labs Bike Light"):
        """Nhấn vào hình sản phẩm"""
        image = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, f"//img[@alt='{alt}']"))
        )
        image.click()
        time.sleep(3)

    def click_back_to_products(self):
        """Quay lại trang danh sách sản phẩm"""
        btn = self.wait.until(EC.element_to_be_clickable(self.BACK_BTN))
        btn.click()
        time.sleep(3)

    def select_sort_option(self, option_text):
        """Chọn sắp xếp sản phẩm"""
        select = Select(self.wait.until(EC.element_to_be_clickable(self.SORT_SELECT)))
        select.select_by_visible_text(option_text)
        time.sleep(3)

    def get_all_product_names(self):
        """Trả về danh sách tên sản phẩm"""
        time.sleep(3)
        items = self.driver.find_elements(By.CLASS_NAME, "inventory_item_name")
        return [item.text for item in items]

    def get_all_product_prices(self):
        """Trả về danh sách giá sản phẩm (float)"""
        time.sleep(3)
        prices = self.driver.find_elements(By.CLASS_NAME, "inventory_item_price")
        return [float(price.text.replace("$", "")) for price in prices]
