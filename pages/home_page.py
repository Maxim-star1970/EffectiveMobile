from playwright.sync_api import Page, expect
from .base_page import BasePage
from locators.home_locators import HomeLocators
import re


class HomePage(BasePage):
    BASE_URL = "https://www.effective-mobile.ru/"

    def __init__(self, page: Page, language: str = "ru"):
        super().__init__(page)
        self.locators = HomeLocators(language)

    def goto(self, url: str = None):
        # Переход на домашнюю страницу
        if url is None:
            url = self.BASE_URL
        self.page.goto(url)
        self.page.wait_for_load_state('networkidle')
        return self

    def verify_hero_section_visible(self):
        # Проверить видимость hero-секции
        hero_section = self.page.locator(self.locators.HERO_SECTION)
        expect(hero_section).to_be_visible()
        return self

    def verify_logo_visible(self):
        # Проверить видимость логотипа
        logo = self.page.locator(self.locators.LOGO_SVG)
        expect(logo).to_be_visible()
        return self

    def verify_company_name_visible(self):
        # Проверить видимость названия компании
        company_name = self.page.locator(self.locators.COMPANY_NAME_SPAN)
        expect(company_name).to_be_visible()
        return self

    def verify_headlines_visible(self):
        # Проверить видимость заголовков
        main_headline = self.page.get_by_text(self.locators.get_main_headline_text())
        sub_headline = self.page.get_by_text(self.locators.get_sub_headline_text())

        expect(main_headline).to_be_visible()
        expect(sub_headline).to_be_visible()
        return self

    def verify_description_visible(self):
        # Проверить видимость описания
        description = self.page.get_by_text(self.locators.get_description_text(), exact=False)
        expect(description).to_be_visible()
        return self

    def verify_buttons_visible_and_enabled(self):
        # Проверить видимость и доступность кнопок
        button_locators = self.locators.get_all_button_locators()

        for button_locator in button_locators:
            button = self.page.locator(button_locator)
            expect(button).to_be_visible()
            expect(button).to_be_enabled()

        return self

    def click_apply_button(self):
        # Кликнуть на кнопку 'Оставить заявку'
        apply_button = self.page.locator(self.locators.get_apply_button_locator())
        apply_button.click()
        return self

    def click_learn_more_button(self):
        # Кликнуть на кнопку 'Узнать больше'
        learn_more_button = self.page.locator(self.locators.get_learn_more_button_locator())
        learn_more_button.click()
        return self

    def click_vacancies_button(self):
        # Кликнуть на кнопку 'Актуальные вакансии'
        vacancies_button = self.page.locator(self.locators.get_vacancies_button_locator())
        vacancies_button.click()
        return self

    def verify_responsive_layout(self, device_type: str):
        # Проверить адаптивность layout
        buttons_container = self.page.locator(self.locators.BUTTONS_CONTAINER)
        expected_class_pattern = self.locators.get_container_class_pattern(device_type)

        expect(buttons_container).to_have_class(expected_class_pattern)
        return self

    def verify_logo_size(self, device_type: str):
        # Проверить размер логотипа в зависимости от устройства
        logo = self.page.locator(self.locators.LOGO_SVG)
        expected_class_pattern = self.locators.get_logo_class_pattern(device_type)

        expect(logo).to_have_class(expected_class_pattern)
        return self

    def verify_headline_size(self, device_type: str):
        # Проверить размер заголовка в зависимости от устройства
        headline = self.page.locator(self.locators.MAIN_HEADING)
        expected_class_pattern = re.compile(self.locators.get_headline_class_for_device(device_type))

        expect(headline).to_have_class(expected_class_pattern)
        return self

    def verify_no_horizontal_scroll(self):
        # Проверить отсутствие горизонтального скролла
        page_width = self.page.viewport_size['width']
        document_width = self.page.evaluate("document.documentElement.scrollWidth")

        assert document_width <= page_width, "Обнаружен горизонтальный скролл"
        return self

    def verify_text_readability(self):
        # Проверить читаемость текста
        text_elements = self.locators.get_all_text_elements()

        for text in text_elements:
            element = self.page.get_by_text(text, exact=False)
            expect(element).to_be_visible()

            # Проверить, что текст не имеет нулевой размер шрифта
            font_size = element.evaluate("el => window.getComputedStyle(el).fontSize")
            assert font_size != '0px', f"Текст '{text}' имеет нулевой размер шрифта"

        return self

    def run_basic_checks(self, device_type: str = None):
        # Запустить базовые проверки
        return (self.verify_hero_section_visible()
                .verify_logo_visible()
                .verify_company_name_visible()
                .verify_headlines_visible()
                .verify_description_visible()
                .verify_buttons_visible_and_enabled()
                .verify_text_readability()
                .verify_no_horizontal_scroll())