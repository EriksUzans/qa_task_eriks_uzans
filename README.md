# Optibet Automation Test Assignment

This repository contains an automated test suite for Optibet.lv, built using **Python**, **Pytest**, and **Playwright**. It demonstrates a robust, maintainable Page Object Model (POM) architecture for UI automation.

##  Getting Started

### Prerequisites

* **Python 3.8+**: Ensure Python is installed and added to your system PATH.
* **Docker (Optional)**: Required only if you wish to run tests in a containerized environment.

### 📦 Installation (Local)

1.  **Clone the repository (or extract the archive):**
    ```bash
    git clone <repository-url>
    cd optibet-automation
    ```

2.  **Set up a Virtual Environment:**
    * **Windows:**
        ```bash
        python -m venv venv
        .env\Scriptsctivate
        ```
    

3.  **Install Python Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Install Playwright Browsers:**
    ```bash
    playwright install
    ```

---

## 🧪 Running Tests

### Run Locally

**Execute all tests:**
```bash
pytest
```

**Run with Allure Reports:**
To generate and view a detailed HTML test report:
```bash
pytest --alluredir=allure-results
allure serve allure-results
```
*(Note: Requires Allure command-line tool installed on your system)*

**Run Specific Scenarios:**
```bash
# Header language switch
pytest -k "test_header_language_switching"

# Registration negative tests
pytest -k "test_registration_validation"
```

### Parallel Execution ⚡

To speed up test execution, you can run tests in parallel using `pytest-xdist`.

```bash
# Run tests using as many workers as available CPUs

python -m pytest -n auto -s --browser=chromium tests/test_scenarios.py::test_promotions_filtering --alluredir=allure-results
```

### Run via Docker 🐳

This project includes a `Dockerfile` to run tests in a consistent, headless Linux environment.

1.  **Build the Docker Image:**
    ```bash
    docker build -t optibet-tests .
    ```

2.  **Run Tests Inside Container:**
    ```bash
    docker run optibet-tests
    ```
    *The container will execute `pytest` and output the results to the console.*

---

## ✅ Test Coverage & Scenarios

The following scenarios from the assignment have been implemented:

| Scenario | Description | Status | Notes |
| :--- | :--- | :--- | :--- |
| **2.1 Header & Language** | Verify logo visibility, menu items, and language switching (RU ↔ LV ↔ EN). Checks URL updates and active state. | 
| **2.2 Promotions** | Verify promotions list loads, filters work (Casino/Sports), and cards contain titles/links. Checks detailed page opens correctly. | ✅ Covered | Handles async loading of cards. Includes detailed verification of internal page elements (`.main-title-OB`). |
| **2.3 Registration (Negative)** | Validate form behavior with invalid inputs: Invalid Email, Weak Password, Empty Fields.|✅ Covered  | Uses `pytest.mark.parametrize` . Checks for specific error messages and field validation states. |
| **2.4 Login (Negative)** | Verify login fails  with non-existent credentials. |✅ Covered  | Checks for the specific error message "The username or password is incorrect". |

### ⚠️ Limitations
* **CAPTCHA / Bot Detection:** Automated login/registration tests on public production sites often trigger CAPTCHA or Cloudflare protections. This suite uses `playwright-stealth` and `slow_mo` to mitigate this.


---

##  Test Rationale

### Why these scenarios?
These specific scenarios were selected because they cover critical features and the most high-risk areas of the application:
1.  **Navigation/Language:** Fundamental for user retention and accessibility. If a user can't navigate or read the site, they leave.
2.  **Promotions:** A key business driver for casinos. Ensuring filters work means users can find relevant offers, directly impacting revenue.
3.  **Registration/Login:**  Negative testing here is crucial to ensure security (no weak passwords) and usability (clear error messages when users make mistakes).

### Future Improvements (With More Time)
If more time were available, the following enhancements would be added:
* **CI/CD Pipeline:** A GitHub Actions workflow to run these tests automatically on every Pull Request.
* **Visual Regression Testing:** Use Playwright's visual comparison tools to detect layout shifts or broken CSS that functional tests might miss.


