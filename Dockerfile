# Dockerfile для запуска тестов
# Стадия сборки зависимостей
FROM python:3.10-slim AS builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Финальная стадия
FROM python:3.10-slim

WORKDIR /app

# Копируем установленные пакеты из стадии сборки
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    ca-certificates \
    openjdk-21-jre-headless \
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
    chromium \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Allure Commandline
RUN wget -q https://github.com/allure-framework/allure2/releases/download/2.30.0/allure-2.30.0.tgz -O /tmp/allure.tgz && \
    tar -zxvf /tmp/allure.tgz -C /opt/ && \
    ln -s /opt/allure-2.30.0/bin/allure /usr/bin/allure && \
    rm /tmp/allure.tgz

# Устанавливаем зависимости для HTML отчетов
RUN pip install pytest-html==4.1.1 pytest-metadata==3.1.1

# Создаем скрипт для запуска тестов В ОТДЕЛЬНОЙ ДИРЕКТОРИИ
RUN mkdir -p /scripts && \
    echo '#!/bin/sh' > /scripts/run_tests.sh && \
    echo 'set -e' >> /scripts/run_tests.sh && \
    echo '' >> /scripts/run_tests.sh && \
    echo '# Устанавливаем права на директории' >> /scripts/run_tests.sh && \
    echo 'mkdir -p /app/allure-results /app/allure-report /app/reports /app/screenshots' >> /scripts/run_tests.sh && \
    echo 'chmod -R 777 /app/allure-results /app/allure-report /app/reports /app/screenshots' >> /scripts/run_tests.sh && \
    echo '' >> /scripts/run_tests.sh && \
    echo '# Если переданы аргументы - запускаем их напрямую' >> /scripts/run_tests.sh && \
    echo 'if [ $# -gt 0 ]; then' >> /scripts/run_tests.sh && \
    echo '    echo "Запуск с аргументами: $*"' >> /scripts/run_tests.sh && \
    echo '    "$@"' >> /scripts/run_tests.sh && \
    echo 'else' >> /scripts/run_tests.sh && \
    echo '    echo "Запуск всех тестов в headless режиме по умолчанию"' >> /scripts/run_tests.sh && \
    echo '    pytest --alluredir=/app/allure-results -v' >> /scripts/run_tests.sh && \
    echo 'fi' >> /scripts/run_tests.sh && \
    echo '' >> /scripts/run_tests.sh && \
    echo '# Генерируем Allure отчет если есть результаты' >> /scripts/run_tests.sh && \
    echo 'if [ -d "/app/allure-results" ] && [ "$(ls -A /app/allure-results 2>/dev/null)" ]; then' >> /scripts/run_tests.sh && \
    echo '    echo "Генерация Allure отчета..."' >> /scripts/run_tests.sh && \
    echo '    allure generate /app/allure-results -o /app/allure-report --clean' >> /scripts/run_tests.sh && \
    echo '    echo "Allure отчет сгенерирован в /app/allure-report"' >> /scripts/run_tests.sh && \
    echo 'fi' >> /scripts/run_tests.sh && \
    echo '' >> /scripts/run_tests.sh && \
    echo 'echo "Тесты успешно завершены"' >> /scripts/run_tests.sh && \
    chmod +x /scripts/run_tests.sh

# ENV переменные
ENV CHROMIUM_PATH=/usr/bin/chromium
ENV PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=0
ENV PLAYWRIGHT_BROWSERS_PATH=0
ENV NODE_OPTIONS="--max-old-space-size=4096"

COPY . .
RUN pip install playwright==1.56.0 && \
    python -m playwright install-deps && \
    python -m playwright install chromium && \
    python -m playwright --version \

EXPOSE 8080
CMD ["/scripts/run_tests.sh"]
