#!/bin/sh
set -e

# По умолчанию запускаем все тесты в headless режиме
TEST_COMMAND="${TEST_COMMAND:-pytest}"
TEST_ARGS="${TEST_ARGS:-}"
REPORT_DIR="${REPORT_DIR:-/app/reports}"

# Создаем директории для отчетов
mkdir -p "$REPORT_DIR" /app/allure-results /app/allure-report /app/screenshots
chmod -R 777 "$REPORT_DIR" /app/allure-results /app/allure-report /app/screenshots

# Функция для генерации Allure отчета
generate_allure_report() {
    if [ -d "/app/allure-results" ] && [ "$(ls -A /app/allure-results 2>/dev/null)" ]; then
        echo "Генерация Allure отчета..."
        allure generate /app/allure-results -o /app/allure-report --clean
        echo "Allure отчет сгенерирован в /app/allure-report"
    else
        echo "Нет результатов для генерации Allure отчета"
    fi
}

echo "Запуск тестов с командой: $TEST_COMMAND $TEST_ARGS"

# Если переданы конкретные аргументы через командную строку
if [ $# -gt 0 ]; then
    echo "Запуск с аргументами: $*"
    "$@"
else
    echo "Запуск с переменными окружения: $TEST_COMMAND $TEST_ARGS"
    sh -c "$TEST_COMMAND $TEST_ARGS"
fi

# Генерируем Allure отчет если были тесты
generate_allure_report

echo "Тесты успешно завершены. Отчеты сохранены в:"
echo "Allure: /app/allure-report"
echo "HTML: $REPORT_DIR/report.html"
echo "Скриншоты: /app/screenshots"