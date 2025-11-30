# Dockerfile для запуска тестов с поддержкой всех команд из README.md
# Использует multi-stage сборку для оптимизации размера образа

# Стадия сборки зависимостей
FROM python:3.10-slim as builder

WORKDIR /app

# Копируем только requirements для кэширования слоя
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Финальная стадия
FROM python:3.10-slim

WORKDIR /app

# Копируем установленные пакеты из стадии сборки
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Устанавливаем системные зависимости для работы браузера, Allure и отчетов
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    ca-certificates \
    openjdk-17-jre-headless \
    libgbm1 \
    libxshmfence1 \
    libasound2 \
    libdrm2 \
    libxkbcommon0 \
    libpango-1.0-0 \
    libcairo2 \
    libatspi2.0-0 \
    libgtk-3-0 \
    libnotify4 \
    libnss3 \
    libxss1 \
    libxtst6 \
    xdg-utils \
    libgbm-dev \
    libgl1 \
    libgl1-mesa-dri \
    fonts-noto \
    fonts-liberation \
    ttf-mscorefonts-installer \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Google Chrome (без ошибок с пробелами в URL)
RUN wget -q https://dl.google.com/linux/linux_signing_key.pub -O /tmp/google_signing_key.pub \
    && echo "deb [arch=amd64 signed-by=/tmp/google_signing_key.pub] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/* /tmp/google_signing_key.pub \
    && google-chrome --version

# Устанавливаем Playwright и браузеры
RUN pip install playwright==1.56.0 && \
    playwright install chromium && \
    playwright install-deps

# Устанавливаем Allure Commandline (без ошибок с пробелами в URL)
RUN wget https://github.com/allure-framework/allure2/releases/download/2.30.0/allure-2.30.0.tgz \
    && tar -zxvf allure-2.30.0.tgz -C /opt/ \
    && ln -s /opt/allure-2.30.0/bin/allure /usr/bin/allure \
    && rm allure-2.30.0.tgz

# Устанавливаем зависимости для HTML отчетов
RUN pip install pytest-html==4.1.1 pytest-metadata==3.1.1

# Копируем исходный код проекта
COPY . .

# Создаем директории для отчетов (чтобы избежать проблем с правами)
RUN mkdir -p allure-results allure-report reports screenshots \
    && chmod -R 777 allure-results allure-report reports screenshots

# ENV переменные для настройки браузера
ENV CHROMIUM_PATH=/usr/bin/chromium
ENV CHROME_BIN=/usr/bin/google-chrome

# Скрипт для запуска тестов с поддержкой всех команд из README.md
RUN echo '#!/bin/sh\n\
set -e\n\
\n\
# По умолчанию запускаем все тесты в headless режиме\n\
TEST_COMMAND=${TEST_COMMAND:-"pytest"}\n\
TEST_ARGS=${TEST_ARGS:-""}\n\
REPORT_DIR=${REPORT_DIR:-"/app/reports"}\n\
\n\
# Создаем директории для отчетов\n\
mkdir -p "$REPORT_DIR" /app/allure-results /app/allure-report /app/screenshots\n\
\n\
# Функция для генерации Allure отчета\n\
generate_allure_report() {\n\
    if [ -d "/app/allure-results" ] && [ "$(ls -A /app/allure-results)" ]; then\n\
        echo "Генерация Allure отчета..."\n\
        allure generate /app/allure-results -o /app/allure-report --clean\n\
        echo "Allure отчет сгенерирован в /app/allure-report"\n\
    fi\n\
}\n\
\n\
# Запускаем тесты в зависимости от переданных параметров\n\
echo "Запуск тестов с командой: $TEST_COMMAND $TEST_ARGS"\n\
\n\
# Если переданы конкретные аргументы через командную строку\n\
if [ $# -gt 0 ]; then\n\
    exec "$@"\n\
fi\n\
\n\
# Если используются переменные окружения\n\
case "$TEST_COMMAND" in\n\
    "smoke")\n\
        pytest -m smoke --alluredir=/app/allure-results $TEST_ARGS\n\
        ;;\n\
    "regression")\n\
        pytest -m "not smoke" --alluredir=/app/allure-results $TEST_ARGS\n\
        ;;\n\
    "mobile")\n\
        pytest -m mobile --alluredir=/app/allure-results $TEST_ARGS\n\
        ;;\n\
    "desktop")\n\
        pytest -m desktop --alluredir=/app/allure-results $TEST_ARGS\n\
        ;;\n\
    "responsive")\n\
        pytest -m responsive --alluredir=/app/allure-results $TEST_ARGS\n\
        ;;\n\
    "accessibility")\n\
        pytest -m accessibility --alluredir=/app/allure-results $TEST_ARGS\n\
        ;;\n\
    "critical")\n\
        pytest -m critical --alluredir=/app/allure-results $TEST_ARGS\n\
        ;;\n\
    "allure-only")\n\
        pytest --alluredir=/app/allure-results $TEST_ARGS\n\
        ;;\n\
    "html-report")\n\
        pytest --html=$REPORT_DIR/report.html --self-contained-html $TEST_ARGS\n\
        ;;\n\
    "combined")\n\
        pytest --alluredir=/app/allure-results --html=$REPORT_DIR/report.html --self-contained-html $TEST_ARGS\n\
        ;;\n\
    *)\n\
        # По умолчанию запускаем все тесты\n\
        eval "$TEST_COMMAND $TEST_ARGS"\n\
        ;;\n\
esac\n\
\n\
# Генерируем Allure отчет если были тесты\n\
generate_allure_report\n\
\n\
echo "Тесты успешно завершены. Отчеты сохранены в:"\n\
echo "Allure: /app/allure-report"\n\
echo "HTML: $REPORT_DIR/report.html"\n\
echo "Скриншоты: /app/screenshots"\n\
' > /app/run_tests.sh && chmod +x /app/run_tests.sh

# Порт для Allure отчета
EXPOSE 8080

# Команда по умолчанию - запуск всех тестов в headless режиме
CMD ["/app/run_tests.sh"]

# Примеры использования:
#
# 1. Запуск всех тестов в headless режиме (по умолчанию):
#    docker run -v $(pwd):/app effective-mobile-tests
#
# 2. Запуск с видимым браузером:
#    docker run -v $(pwd):/app -e TEST_ARGS="--headed" effective-mobile-tests
#
# 3. Запуск smoke тестов:
#    docker run -v $(pwd):/app -e TEST_COMMAND="smoke" -e TEST_ARGS="--headed" effective-mobile-tests
#
# 4. Запуск с генерацией Allure и HTML отчетов:
#    docker run -v $(pwd):/app -e TEST_COMMAND="combined" -e TEST_ARGS="--headed" effective-mobile-tests
#
# 5. Запуск конкретного файла:
#    docker run -v $(pwd):/app effective-mobile-tests pytest tests/test_home_page.py --headed
#
# 6. Запуск в debug режиме с паузой при ошибке:
#    docker run -v $(pwd):/app -e TEST_ARGS="--debug --headed --pause-on-failure" effective-mobile-tests
#
# 7. Просмотр Allure отчета:
#    docker run -p 8080:8080 -v $(pwd)/allure-report:/app/allure-report effective-mobile-tests \
#        allure serve /app/allure-report
