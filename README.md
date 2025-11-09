# Selenium Web Automation (Python + Selenium + GitHub Actions)

Dự án thực hiện **kiểm thử tự động giao diện web** bằng Selenium WebDriver với Python.
Website demo sử dụng: [https://www.saucedemo.com/](https://www.saucedemo.com/)

---

## 🛠 Công nghệ sử dụng

* Python 3.x
* Selenium WebDriver
* PyTest
* Page Object Model (POM)
* GitHub Actions (CI/CD)

---

## 📦 Cài đặt & chạy test

### 1️⃣ Clone project

```bash
git clone https://github.com/khanhquynh111/selenium-test.git
cd selenium-test
```

### 2️⃣ Cài đặt thư viện

```bash
pip install -r requirements.txt
```

### 3️⃣ Chạy test trên máy local

✅ Chạy toàn bộ test:

```bash
pytest
```

✅ Xuất báo cáo HTML:

```bash
pytest --html=reports/test-report.html
```

✅ Chạy 1 test cụ thể (ví dụ test đăng nhập hợp lệ):

```bash
pytest -k "test_login_valid"
```

---

## ⚙️ GitHub Actions (CI/CD)

* Tự động chạy test mỗi khi **push code** hoặc **tạo pull request**
* Chrome chạy ở chế độ **headless** trên môi trường GitHub runner
* File workflow CI/CD:
  `.github/workflows/selenium-test.yml`
