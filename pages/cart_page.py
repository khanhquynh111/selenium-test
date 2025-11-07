import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CartPage:
    CART_ICON = (By.CLASS_NAME, "shopping_cart_link")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    BACK_BTN = (By.ID, "continue-shopping")
    CHECKOUT_BTN = (By.ID, "checkout")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def _pause(self, seconds=2):
        """Tạo nhịp nghỉ ngắn giữa các thao tác"""
        time.sleep(seconds)

    def add_product_to_cart(self, product_name):
        """Thêm sản phẩm theo tên"""
        items = self.driver.find_elements(By.CLASS_NAME, "inventory_item")
        for item in items:
            name = item.find_element(By.CLASS_NAME, "inventory_item_name").text.strip()
            if name == product_name:
                btn = item.find_element(By.TAG_NAME, "button")
                btn.click()
                self._pause(1)

                # Đợi badge xuất hiện
                try:
                    self.wait.until(EC.presence_of_element_located(self.CART_BADGE))
                except:
                    pass
                return
        raise Exception(f"Không tìm thấy sản phẩm: {product_name}")


    def get_button_text(self, product_name):
        """Lấy trạng thái nút Add to cart / Remove"""
        items = self.driver.find_elements(By.CLASS_NAME, "inventory_item")
        for item in items:
            name = item.find_element(By.CLASS_NAME, "inventory_item_name").text.strip()
            if name == product_name:
                return item.find_element(By.TAG_NAME, "button").text
        return None

    def get_cart_count(self):
        """Lấy số hiển thị trên biểu tượng giỏ hàng"""
        try:
            badge = self.driver.find_element(*self.CART_BADGE)
            return int(badge.text.strip())
        except:
            return 0

    def open_cart(self):
        """Click vào biểu tượng giỏ hàng"""
        self.driver.find_element(*self.CART_ICON).click()
        self.wait.until(EC.url_contains("cart"))
        self._pause(1)

    def click_back_to_products(self):
        """Từ trang giỏ hàng → quay lại danh sách sản phẩm"""
        self.driver.find_element(*self.BACK_BTN).click()
        self.wait.until(EC.url_contains("inventory"))
        self._pause(1)

    def is_cart_page_displayed(self):
        """Kiểm tra có đang ở trang cart không"""
        return "cart" in self.driver.current_url
