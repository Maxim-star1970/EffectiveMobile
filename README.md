Выполненное тестовое задания.


# БАЗОВЫЕ КОМАНДЫ
pytest                                                          # Запуск всех тестов в headless режиме
pytest --headed                                                 # Запуск всех тестов с видимым браузером
pytest tests/test_home_page.py --headed                         # Запуск конкретного файла с видимым браузером
pytest tests/test_home_page.py::TestHomePage --headed           # Запуск конкретного класса с видимым браузером


# ЗАПУСК С ALLURE ОТЧЕТАМИ
python -m pytest --html=test_report.html --self-contained-html  # Создание простого HTML отчета
pytest --alluredir=allure-results                               # Запуск с генерацией Allure результатов
pytest --headed --alluredir=allure-results                      # Запуск с видимым браузером и Allure

# ЗАПУСК ПО МАРКЕРАМ
pytest -m responsive --headed                                   # Без --headed в headless режиме
pytest -m accessibility --headed                                 
pytest -m slow --headed
pytest -m critical --headed
pytest -m smoke --headed

# ЗАПУСК ПО МАРКЕРАМ С ALLURE
pytest -m mobile --headed --alluredir=allure-results            # Мобильные тесты с Allure
pytest -m desktop --headed --alluredir=allure-results           # Десктопные тесты с Allure

# ОТЛАДОЧНЫЕ РЕЖИМЫ
pytest --debug --headed                                         # Запуск в debug режиме
pytest --headed --slowmo=1000                                   # Запуск с замедлением 1 секунда
pytest --headed --pause-on-failure                              # Пауза при ошибке

# ОТЛАДОЧНЫЕ РЕЖИМЫ С ALLURE
pytest --debug --headed --alluredir=allure-results              # Debug с Allure
pytest --headed --slowmo=1000 --alluredir=allure-results        # Замедление с Allure

# АЛЬТЕРНАТИВНЫЕ ОТЧЕТЫ (БЕЗ ALLURE)
pytest --headed --html=report.html                              # Генерация HTML отчета
pytest --headed --html=report.html --self-contained-html        # HTML отчет со скриншотами
pytest --headed --junitxml=report.xml                           # JUnit XML отчет для CI/CD

# КОМБИНИРОВАННЫЕ ОТЧЕТЫ
pytest --headed --alluredir=allure-results --html=report.html   # Allure + HTML отчеты


