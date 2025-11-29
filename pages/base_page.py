from playwright.sync_api import Page, expect
import time
import allure


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def goto(self, url: str = None):
        # Переход на страницу
        with allure.step(f"Переход на страницу: {url}"):
            if url is None:
                url = self.BASE_URL
            self.page.goto(url)
            self.page.wait_for_load_state('networkidle')

    def take_screenshot(self, name: str, full_page: bool = True):
        # Сделать скриншот
        with allure.step(f"Создание скриншота: {name}"):
            path = f"screenshots/{name}_{int(time.time())}.png"
            self.page.screenshot(path=path, full_page=full_page)

            # Прикрепляем скриншот к Allure отчету
            allure.attach.file(path, name=name, attachment_type=allure.attachment_type.PNG)

            return path

    def wait_for_element(self, locator: str, timeout: int = 10000):
        # Ждать появления элемента
        self.page.wait_for_selector(locator, timeout=timeout)

    def is_element_visible(self, locator: str) -> bool:
        # Проверить видимость элемента
        try:
            return self.page.is_visible(locator)
        except:
            return False