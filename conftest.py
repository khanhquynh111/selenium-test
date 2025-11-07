# conftest.py
import os
import datetime
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")

    # 👇 bắt buộc cho môi trường CI (không có giao diện)
    options.add_argument("--headless=new")       # Chrome headless
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(8)

    yield driver

    driver.quit()


# 📸 Tự động chụp ảnh nếu test fail
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        driver = item.funcargs.get("driver", None)
        if driver:
            os.makedirs("reports", exist_ok=True)

            time_str = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            screenshot_name = f"reports/{item.name}_{time_str}.png"
            driver.save_screenshot(screenshot_name)

            rep.extra = getattr(rep, "extra", [])
            rep.extra.append({
                "name": "screenshot",
                "content": screenshot_name,
                "mime_type": "image/png"
            })




