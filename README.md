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

# ЗАПУСК ТЕСТОВ ИЗ ОБРАЗА:
# 1. СБОРКА ОБРАЗА: 
ВАЖНО: Dockerfile и файл: run_tests.sh, должны находится в корне проекта.
Сборка образа:
# Перейти в директорию проекта
cd ~/PycharmProjects/EffectiveMobile
# Очистить кэш сборки (если были проблемы)
docker builder prune -f
# Удалить старый образ
docker rmi effective-mobile-tests 2>/dev/null || true
# Собрать образ (без кэша для гарантии)
docker build --no-cache -t effective-mobile-tests .
# Проверить список образов
docker images

# 2. БАЗОВЫЕ КОМАНДЫ запуска тестов:
# Запуск всех тестов в headless режиме (по умолчанию)
docker run -v $(pwd):/app effective-mobile-tests

# Запуск всех тестов с видимым браузером
docker run -v $(pwd):/app effective-mobile-tests pytest --headed

# Запуск конкретного файла с видимым браузером
docker run -v $(pwd):/app effective-mobile-tests pytest tests/test_home_page.py --headed

# Запуск конкретного класса с видимым браузером
docker run -v $(pwd):/app effective-mobile-tests pytest tests/test_home_page.py::TestHomePage --headed

# 3. ЗАПУСК С ALLURE ОТЧЕТАМИ:
# Создание простого HTML отчета
docker run -v $(pwd):/app effective-mobile-tests python -m pytest --html=test_report.html --self-contained-html

# Запуск с генерацией Allure результатов
docker run -v $(pwd):/app effective-mobile-tests pytest --alluredir=/app/allure-results

# Запуск с видимым браузером и Allure
docker run -v $(pwd):/app effective-mobile-tests pytest --headed --alluredir=/app/allure-results

# Просмотр Allure отчета (запускает веб-сервер на порту 8080)
docker run -p 8080:8080 -v $(pwd)/allure-report:/app/allure-report --entrypoint allure effective-mobile-tests serve /app/allure-report

# 4. ЗАПУСК ПО МАРКЕРАМ:
# Responsive тесты (headless режим)
docker run -v $(pwd):/app effective-mobile-tests pytest -m responsive

# Responsive тесты с видимым браузером
docker run -v $(pwd):/app effective-mobile-tests pytest -m responsive --headed

# Accessibility тесты с видимым браузером
docker run -v $(pwd):/app effective-mobile-tests pytest -m accessibility --headed

# Slow тесты с видимым браузером
docker run -v $(pwd):/app effective-mobile-tests pytest -m slow --headed

# Critical тесты с видимым браузером
docker run -v $(pwd):/app effective-mobile-tests pytest -m critical --headed

# Smoke тесты с видимым браузером
docker run -v $(pwd):/app effective-mobile-tests pytest -m smoke --headed

# 5. ЗАПУСК ПО МАРКЕРАМ С ALLURE:
# Мобильные тесты с Allure
docker run -v $(pwd):/app effective-mobile-tests pytest -m mobile --headed --alluredir=/app/allure-results

# Десктопные тесты с Allure
docker run -v $(pwd):/app effective-mobile-tests pytest -m desktop --headed --alluredir=/app/allure-results

# 6. ОТЛАДОЧНЫЕ РЕЖИМЫ:
# Запуск в debug режиме
docker run -v $(pwd):/app effective-mobile-tests pytest --debug --headed

# Запуск с замедлением 1 секунда
docker run -v $(pwd):/app effective-mobile-tests pytest --headed --slowmo=1000

# Запуск с паузой при ошибке
docker run -v $(pwd):/app effective-mobile-tests pytest --headed --pause-on-failure

# 7. ОТЛАДОЧНЫЕ РЕЖИМЫ С ALLURE:
# Debug с Allure
docker run -v $(pwd):/app effective-mobile-tests pytest --debug --headed --alluredir=/app/allure-results

# Замедление с Allure
docker run -v $(pwd):/app effective-mobile-tests pytest --headed --slowmo=1000 --alluredir=/app/allure-results

# АЛЬТЕРНАТИВНЫЕ ОТЧЕТЫ (БЕЗ ALLURE):
# Генерация HTML отчета
docker run -v $(pwd):/app effective-mobile-tests pytest --headed --html=/app/report.html

# HTML отчет со скриншотами
docker run -v $(pwd):/app effective-mobile-tests pytest --headed --html=/app/report.html --self-contained-html

# JUnit XML отчет для CI/CD
docker run -v $(pwd):/app effective-mobile-tests pytest --headed --junitxml=/app/report.xml

# 8. АЛЬТЕРНАТИВНЫЕ ОТЧЕТЫ (БЕЗ ALLURE):
# Генерация HTML отчета
docker run -v $(pwd):/app effective-mobile-tests pytest --headed --html=/app/report.html
