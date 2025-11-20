import pytest
import os
import allure
from playwright.sync_api import Page, sync_playwright
from slugify import slugify

def pytest_addoption(parser):
    parser.addoption("--headless-mode", action="store_true", default=False, help="Run browser in headless mode")
    # Note: --browser option is added automatically by pytest-playwright plugin

@pytest.fixture(scope="function")
def page(request):
    base_url = request.config.getoption("base_url") or "https://www.optibet.lv"
    headless = request.config.getoption("headless_mode")
    
    # Get browser choice from pytest-playwright's built-in option
    try:
        browser_name = request.config.getoption("browser") or "chromium"
    except ValueError:
        browser_name = "chromium"
    
    # Handle potential list type if passed from xdist/matrix
    if isinstance(browser_name, list):
        browser_name = browser_name[0]

    if browser_name == "chrome":
        browser_name = "chromium"

    with sync_playwright() as p:
        if browser_name == "firefox":
            browser_type = p.firefox
        elif browser_name == "webkit":
            browser_type = p.webkit
        else:
            browser_type = p.chromium

        # Launch with custom slow_mo for visibility
        browser = browser_type.launch(headless=headless, slow_mo=1000)
        
        context = browser.new_context(
            base_url=base_url, 
            viewport={"width": 1920, "height": 1080},
            locale="en-GB"
        )
        context.set_default_timeout(20000)
        
        page = context.new_page()
        yield page
        context.close()
        browser.close()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed and "page" in item.funcargs:
        page = item.funcargs["page"]
        screenshot_name = slugify(item.nodeid)
        try:
            allure.attach(page.screenshot(full_page=True), name=f"Failure: {screenshot_name}", attachment_type=allure.attachment_type.PNG)
        except Exception as e:
            print(f"Failed to take screenshot: {e}")