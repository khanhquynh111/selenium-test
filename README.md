Selenium Web Automation 
Đề tài thực hiện kiểm thử tự động giao diện web bằng Selenium WebDriver với Python.
Ứng dụng demo: https://www.saucedemo.com/
Công nghệ sử dụng: 
- Python 3.x
- Selenium WebDriver
- PyTest
- Page Object Model (POM)
- GitHub Actions (CI/CD)

Cài đặt & chạy test:

1️⃣ Clone source project
git clone https://github.com/<your-account>/selenium-test.git
cd selenium-test

2️⃣ Cài đặt dependency
pip install -r requirements.txt

▶️ Chạy test trên máy local (PyCharm / Terminal)
Chạy toàn bộ test:
pytest
Chạy và xuất báo cáo HTML:
pytest --html=reports/test-report.html
Chạy 1 test cụ thể (ví dụ test đăng nhập hợp lệ) với Github Actions:
pytest -k "test_login_valid"

GitHub Actions (CI/CD)
Tự động chạy test khi push hoặc tạo pull request
Chạy Chrome ở chế độ headless trong GitHub runner
File workflow nằm tại:
.github/workflows/selenium-test.yml
