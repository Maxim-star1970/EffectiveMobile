import pytest
import re
import allure
from playwright.sync_api import Page, expect
from utils.device_config import DeviceConfig


class TestHomePage:

    @pytest.mark.critical
    @pytest.mark.smoke
    @allure.feature("Hero Section")
    @allure.story("Responsive Design")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_hero_section_basic(self, home_page):
        # Базовый тест hero-секции
        home_page_obj, device_config = home_page

        with allure.step(f"Запуск теста на устройстве {device_config['name']}"):
            allure.attach(
                f"Разрешение: {device_config['width']}x{device_config['height']}",
                name="Device Info"
            )

        with allure.step("Выполнение базовых проверок hero-секции"):
            home_page_obj.verify_hero_section_visible()
            home_page_obj.verify_logo_visible()
            home_page_obj.verify_headlines_visible()
            home_page_obj.verify_description_visible()
            home_page_obj.verify_buttons_visible_and_enabled()

    @pytest.mark.responsive
    @pytest.mark.slow
    @allure.feature("Mobile Layout")
    @allure.story("Mobile Specific Tests")
    @allure.severity(allure.severity_level.NORMAL)
    def test_mobile_specific_layout(self, mobile_home_page):
        # Тесты специфичные для мобильных устройств
        home_page_obj, device_config = mobile_home_page

        with allure.step(f"Тестируем мобильную версию на {device_config['name']}"):
            with allure.step("Проверяем вертикальное расположение кнопок"):
                buttons_container = home_page_obj.page.locator(
                    home_page_obj.locators.BUTTONS_CONTAINER
                )
                expect(buttons_container).to_have_class(re.compile(r'flex-col'))

    @pytest.mark.responsive
    @pytest.mark.slow
    @allure.feature("Desktop Layout")
    @allure.story("Desktop Specific Tests")
    @allure.severity(allure.severity_level.NORMAL)
    def test_desktop_specific_layout(self, desktop_home_page):
        # Тесты специфичные для десктопных устройств
        home_page_obj, device_config = desktop_home_page

        with allure.step(f"Тестируем десктопную версию на {device_config['name']}"):
            with allure.step("Проверяем горизонтальное расположение кнопок"):
                buttons_container = home_page_obj.page.locator(
                    home_page_obj.locators.BUTTONS_CONTAINER
                )
                expect(buttons_container).to_have_class(re.compile(r'sm:flex-row'))

    @pytest.mark.critical
    @pytest.mark.smoke
    @allure.feature("Functionality")
    @allure.story("Button Actions")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_apply_button_functionality(self, home_page):
        # Тест функциональности кнопки 'Оставить заявку'
        home_page_obj, _ = home_page

        with allure.step("Кликаем на кнопку 'Оставить заявку' и проверяем результат"):
            # Сохраняем текущий URL для проверки изменений
            initial_url = home_page_obj.page.url

            home_page_obj.click_apply_button()

            # Ждем навигации или изменений на странице
            home_page_obj.page.wait_for_load_state('networkidle')

            # Проверяем, что произошло изменение (новая страница, модальное окно и т.д.)
            current_url = home_page_obj.page.url
            assert current_url != initial_url or home_page_obj.page.locator(
                '[data-testid="modal"], [role="dialog"], form'
            ).first.is_visible(), "После клика на кнопку не произошло ожидаемых изменений"

    @pytest.mark.slow
    @allure.feature("Navigation")
    @allure.story("External Links")
    @allure.severity(allure.severity_level.NORMAL)
    def test_vacancies_button_navigation(self, home_page):
        # Тест навигации по кнопке вакансий
        home_page_obj, _ = home_page

        with allure.step("Кликаем на кнопку 'Актуальные вакансии' и проверяем открытие новой вкладки"):
            with home_page_obj.page.expect_popup() as popup_info:
                home_page_obj.click_vacancies_button()

            new_page = popup_info.value

            # Ждем полной загрузки новой страницы
            new_page.wait_for_load_state('networkidle')

            # Проверяем URL новой вкладки
            expect(new_page).to_have_url(re.compile(r".*ai-hunt\.ru/vacancies.*"))

            # Закрываем новую вкладку
            new_page.close()

    @pytest.mark.slow
    @allure.feature("UI Elements")
    @allure.story("Logo Testing")
    @allure.severity(allure.severity_level.NORMAL)
    def test_svg_logo_content(self, home_page):
        # Тест содержимого SVG логотипа
        home_page_obj, _ = home_page

        with allure.step("Проверяем SVG логотип"):
            # Используем локаторы из HomeLocators
            svg_logo = home_page_obj.page.locator(home_page_obj.locators.LOGO_SVG)
            expect(svg_logo).to_be_visible()

            with allure.step("Проверяем текстовое содержимое SVG"):
                logo_text = home_page_obj.page.locator(home_page_obj.locators.SVG_LOGO_TEXT)
                expect(logo_text).to_have_text('EM')

            with allure.step("Проверяем элементы пути"):
                svg_paths = home_page_obj.page.locator(home_page_obj.locators.SVG_LOGO_PATHS)
                expect(svg_paths.first).to_be_visible()
                path_count = svg_paths.count()
                assert path_count > 0, f"Ожидали хотя бы 1 элемент пути, но найдено {path_count}"

    @pytest.mark.slow
    @allure.feature("Visual Testing")
    @allure.story("Screenshots")
    @allure.severity(allure.severity_level.MINOR)
    def test_screenshot_comparison(self, home_page):
        # Тест со скриншотами для визуальной проверки
        home_page_obj, device_config = home_page

        with allure.step(f"Создаем скриншот для {device_config['name']}"):
            # Создать скриншот для регрессионного тестирования
            screenshot_path = home_page_obj.take_screenshot(
                f"hero_section_{device_config['name']}"
            )

            # Прикрепляем скриншот к Allure отчету
            allure.attach.file(
                screenshot_path,
                name=f"Screenshot_{device_config['name']}",
                attachment_type=allure.attachment_type.PNG
            )


class TestHomePageAccessibility:
    # Тесты доступности домашней страницы

    @pytest.mark.accessibility
    @pytest.mark.slow
    @allure.feature("Accessibility")
    @allure.story("Keyboard Navigation")
    @allure.severity(allure.severity_level.NORMAL)
    def test_keyboard_navigation(self, home_page):
        # Тест навигации с клавиатуры
        home_page_obj, _ = home_page

        with allure.step("Тестируем навигацию с клавиатуры"):
            # Начинаем с начала страницы
            home_page_obj.page.keyboard.press('Home')

            # Переходим к первому интерактивному элементу
            home_page_obj.page.keyboard.press('Tab')

            # Проверяем, что фокус установлен на кнопке
            apply_button = home_page_obj.page.locator(
                home_page_obj.locators.get_apply_button_locator()
            )
            expect(apply_button).to_be_focused()

    @pytest.mark.accessibility
    @allure.feature("Accessibility")
    @allure.story("Semantic Structure")
    @allure.severity(allure.severity_level.NORMAL)
    def test_semantic_structure(self, home_page):
        # Тест семантической структуры
        home_page_obj, _ = home_page

        with allure.step("Проверяем семантическую структуру страницы"):
            with allure.step("Проверяем наличие заголовков"):
                headings = home_page_obj.page.get_by_role('heading')
                expect(headings.first).to_be_visible()
                headings_count = headings.count()
                assert headings_count >= 1, f"Ожидали хотя бы 1 заголовок, но найдено {headings_count}"

            with allure.step("Проверяем роли кнопок"):
                apply_button = home_page_obj.page.get_by_role(
                    'button',
                    name=home_page_obj.locators.get_apply_button_text()
                )
                expect(apply_button).to_be_visible()