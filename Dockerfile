# Стадия сборки
FROM python:3.10-slim as builder

WORKDIR /tests
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Финальная стадия
FROM python:3.10-slim

WORKDIR /tests

# Копируем установленные пакеты из стадии сборки
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Устанавливаем системные зависимости включая Java для Allure
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    openjdk-17-jre-headless \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Playwright
RUN pip install playwright && playwright install chromium

# Устанавливаем Allure Commandline
RUN wget https://github.com/allure-framework/allure2/releases/download/2.27.0/allure-2.27.0.tgz \
    && tar -zxvf allure-2.27.0.tgz -C /opt/ \
    && ln -s /opt/allure-2.27.0/bin/allure /usr/bin/allure \
    && rm allure-2.27.0.tgz

COPY . .

# Команда для запуска тестов и генерации отчета
CMD ["sh", "-c", "pytest tests/ --alluredir=allure-results -v && allure generate allure-results -o allure-report --clean"]