from typing import Dict, List, Pattern
import re


class HomeLocators:
    # Класс для хранения и управления локаторами домашней страницы.
    # Инкапсулирует все селекторы и предоставляет методы для работы с ними.


    def __init__(self, language: str = "ru"):
    # Инициализация локаторов
    # Args:
    # language: Язык интерфейса ('ru', 'en' и т.д.)

        self.language = language
        self._init_locators()

    def _init_locators(self):
        #Инициализировать все локаторы в зависимости от языка
        # Тексты в зависимости от языка
        if self.language == "ru":
            self._init_russian_locators()
        elif self.language == "en":
            self._init_english_locators()
        else:
            # По умолчанию русский
            self._init_russian_locators()

        # Общие CSS-локаторы (не зависят от языка)
        self._init_common_locators()

        # Классы для проверки адаптивности
        self._init_responsive_classes()

    def _init_russian_locators(self):
        # Инициализировать русскоязычные текстовые локаторы
        self.TEXTS = {
            "company_name": "Effective Mobile",
            "main_headline": "Ваша карьера в IT",
            "sub_headline": "начинается здесь",
            "description": "Помогаем IT-специалистам найти идеальный проект",
            "apply_button": "Оставить заявку",
            "learn_more_button": "Узнать больше",
            "vacancies_button": "Актуальные вакансии"
        }

    def _init_english_locators(self):
        # Инициализировать англоязычные текстовые локаторы
        self.TEXTS = {
            "company_name": "Effective Mobile",
            "main_headline": "Your IT Career",
            "sub_headline": "Starts Here",
            "description": "Helping IT specialists find the perfect project",
            "apply_button": "Apply Now",
            "learn_more_button": "Learn More",
            "vacancies_button": "Current Vacancies"
        }

    def _init_common_locators(self):
        # Инициализировать общие CSS-локаторы
        # Основные секции
        self.HERO_SECTION = 'section.relative.min-h-screen'
        self.CONTENT_CONTAINER = '.relative.z-10'
        self.BACKGROUND_PATTERN = 'div.absolute.inset-0'

        # Логотип и бренд
        self.LOGO_SVG = 'svg.w-24.h-24'
        self.LOGO_CONTAINER = 'div.mb-8.flex.justify-center'

        # УТОЧНЕННЫЙ локатор для названия компании - только заголовок в hero секции
        self.COMPANY_NAME_SPAN = 'div.mb-6 span.text-brand-primary.text-2xl'

        # Заголовки
        self.MAIN_HEADING = 'h1'
        self.GRADIENT_TEXT_SPAN = 'span.bg-gradient-to-r'

        # Кнопки и контейнеры
        self.BUTTONS_CONTAINER = 'div.flex.flex-col.sm\\:flex-row'
        self.SCROLL_INDICATOR = 'div.absolute.bottom-8'

        # Декоративные элементы
        self.BLUR_CIRCLE = 'div.absolute.top-1\\/4.left-1\\/2.-translate-x-1\\/2.w-\\[600px\\].h-\\[600px\\]'

        # SVG элементы логотипа
        self.SVG_LOGO_GROUP = 'svg g'
        self.SVG_LOGO_TEXT = 'svg text'
        self.SVG_LOGO_PATHS = 'svg path'

    def _init_responsive_classes(self):
        #Инициализировать классы для проверки адаптивности
        self.LOGO_CLASSES = {
            'desktop': 'lg:w-36',
            'tablet': 'md:w-32',
            'mobile': 'w-24'
        }

        self.HEADLINE_CLASSES = {
            'desktop': 'lg:text-7xl',
            'tablet': 'md:text-6xl',
            'mobile': 'text-5xl'
        }

        self.CONTAINER_CLASSES = {
            'mobile': 'flex-col',
            'tablet': 'sm:flex-row',
            'desktop': 'sm:flex-row'
        }

    def get_company_name_text(self) -> str:
        # Получить текст названия компании
        return self.TEXTS["company_name"]

    def get_main_headline_text(self) -> str:
        # Получить текст основного заголовка
        return self.TEXTS["main_headline"]

    def get_sub_headline_text(self) -> str:
        # Получить текст подзаголовка
        return self.TEXTS["sub_headline"]

    def get_description_text(self) -> str:
        # Получить текст описания
        return self.TEXTS["description"]

    def get_apply_button_text(self) -> str:
        # Получить текст кнопки 'Оставить заявку'
        return self.TEXTS["apply_button"]

    def get_learn_more_button_text(self) -> str:
        # Получить текст кнопки 'Узнать больше'
        return self.TEXTS["learn_more_button"]

    def get_vacancies_button_text(self) -> str:
        # Получить текст кнопки 'Актуальные вакансии'
        return self.TEXTS["vacancies_button"]

    def get_logo_class_for_device(self, device_type: str) -> str:
        # Получить CSS класс логотипа для конкретного устройства
        #
        # Args:
        #     device_type: Тип устройства ('mobile', 'tablet', 'desktop')
        #
        # Returns:
        #     CSS класс для проверки
        return self.LOGO_CLASSES.get(device_type, 'w-24')

    def get_headline_class_for_device(self, device_type: str) -> str:
        # Получить CSS класс заголовка для конкретного устройства
        #
        # Args:
        #     device_type: Тип устройства ('mobile', 'tablet', 'desktop')
        #
        # Returns:
        #     CSS класс для проверки
        return self.HEADLINE_CLASSES.get(device_type, 'text-5xl')

    def get_container_class_for_device(self, device_type: str) -> str:
        # Получить CSS класс контейнера для конкретного устройства
        #
        # Args:
        #     device_type: Тип устройства ('mobile', 'tablet', 'desktop')
        #
        # Returns:
        #     CSS класс для проверки
        return self.CONTAINER_CLASSES.get(device_type, 'flex-col')

    def get_all_button_texts(self) -> List[str]:
        # Получить все тексты кнопок для проверки
        return [
            self.get_apply_button_text(),
            self.get_learn_more_button_text(),
            self.get_vacancies_button_text()
        ]

    def get_all_text_elements(self) -> List[str]:
        # Получить все текстовые элементы для проверки читаемости
        return [
            self.get_company_name_text(),
            self.get_main_headline_text(),
            self.get_sub_headline_text(),
            self.get_description_text()
        ]

    def get_apply_button_locator(self) -> str:
        # Получить локатор кнопки 'Оставить заявку'
        return f'button:has-text("{self.get_apply_button_text()}")'

    def get_learn_more_button_locator(self) -> str:
        # Получить локатор кнопки 'Узнать больше'
        return f'button:has-text("{self.get_learn_more_button_text()}")'

    def get_vacancies_button_locator(self) -> str:
        # Получить локатор кнопки 'Актуальные вакансии'
        return f'a:has-text("{self.get_vacancies_button_text()}")'

    def get_all_button_locators(self) -> List[str]:
        # Получить все локаторы кнопок
        return [
            self.get_apply_button_locator(),
            self.get_learn_more_button_locator(),
            self.get_vacancies_button_locator()
        ]

    def get_main_headline_locator(self) -> str:
        # Получить локатор основного заголовка
        return f'text="{self.get_main_headline_text()}"'

    def get_sub_headline_locator(self) -> str:
        # Получить локатор подзаголовка
        return f'text="{self.get_sub_headline_text()}"'

    def get_company_name_locator(self) -> str:
        # Получить локатор названия компании
        return f'text="{self.get_company_name_text()}"'

    def get_description_locator(self) -> str:
        # Получить локатор описания
        return f'text="{self.get_description_text()}"'

    def get_logo_class_pattern(self, device_type: str) -> Pattern:
        # Получить regex pattern для проверки класса логотипа
        #
        # Args:
        #     device_type: Тип устройства
        #
        # Returns:
        #     Regex pattern для проверки
        logo_class = self.get_logo_class_for_device(device_type)
        return re.compile(logo_class)

    def get_container_class_pattern(self, device_type: str) -> Pattern:
        # Получить regex pattern для проверки класса контейнера
        #
        # Args:
        #     device_type: Тип устройства
        #
        # Returns:
        #     Regex pattern для проверки
        container_class = self.get_container_class_for_device(device_type)
        return re.compile(container_class)

    def get_svg_logo_attributes(self) -> Dict[str, str]:
        # Получить атрибуты SVG логотипа для проверки
        #
        # Returns:
        #     Словарь с атрибутами и их значениями
        return {
            "viewBox": "300 300 380 320",
            "xmlns": "http://www.w3.org/2000/svg"
        }

    def get_expected_svg_text_content(self) -> str:
        # Получить ожидаемое текстовое содержимое SVG
        return "EM"

    def get_background_elements(self) -> List[str]:
        # Получить локаторы фоновых элементов
        return [
            self.BACKGROUND_PATTERN,
            self.BLUR_CIRCLE
        ]

    def change_language(self, language: str):
        #Изменить язык локаторов

        #Args:
        #    language: Новый язык ('ru', 'en')
        if language != self.language:
            self.language = language
            self._init_locators()

    def __str__(self) -> str:
        # Строковое представление объекта
        return f"HomeLocators(language='{self.language}')"

    def __repr__(self) -> str:
        # Представление объекта для отладки
        return f"HomeLocators(language='{self.language}', texts={list(self.TEXTS.keys())})"