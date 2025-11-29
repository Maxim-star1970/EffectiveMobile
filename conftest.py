import pytest
import allure
from playwright.sync_api import Browser, BrowserContext

# Конфигурация устройств для тестирования
DEVICES = [
    {'name': 'mobile', 'width': 375, 'height': 667, 'type': 'mobile'},
    {'name': 'tablet', 'width': 768, 'height': 1024, 'type': 'tablet'},
    {'name': 'desktop', 'width': 1920, 'height': 1080, 'type': 'desktop'},
    {'name': 'desktop_hd', 'width': 1366, 'height': 768, 'type': 'desktop'},
]

@pytest.fixture(params=DEVICES, ids=[device['name'] for device in DEVICES])
def viewport_config(request):
    return request.param

@pytest.fixture
def page_with_size(browser: Browser, viewport_config):
    context = browser.new_context(viewport=viewport_config)
    page = context.new_page()
    yield page, viewport_config
    context.close()

@pytest.fixture
def home_page(page_with_size):
    page, config = page_with_size
    from pages.home_page import HomePage
    home_page = HomePage(page)
    home_page.goto()
    return home_page, config

# Фикстуры для конкретных типов устройств
@pytest.fixture(params=[d for d in DEVICES if d['type'] == 'mobile'])
def mobile_config(request):
    return request.param

@pytest.fixture
def mobile_home_page(browser, mobile_config):
    context = browser.new_context(viewport=mobile_config)
    page = context.new_page()
    from pages.home_page import HomePage
    home_page = HomePage(page)
    home_page.goto()
    yield home_page, mobile_config
    context.close()

@pytest.fixture(params=[d for d in DEVICES if d['type'] == 'desktop'])
def desktop_config(request):
    return request.param

@pytest.fixture
def desktop_home_page(browser, desktop_config):
    context = browser.new_context(viewport=desktop_config)
    page = context.new_page()
    from pages.home_page import HomePage
    home_page = HomePage(page)
    home_page.goto()
    yield home_page, desktop_config
    context.close()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Добавляем скриншоты в Allure при падении тестов"""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        for fixture_name in item.funcargs:
            if "page" in fixture_name:
                page = item.funcargs[fixture_name]
                try:
                    screenshot = page.screenshot()
                    allure.attach(screenshot, name="screenshot", attachment_type=allure.attachment_type.PNG)
                    html = page.content()
                    allure.attach(html, name="page_html", attachment_type=allure.attachment_type.HTML)
                except Exception as e:
                    print(f"Не удалось сделать скриншот: {e}")

