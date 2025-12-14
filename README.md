# Sauce Demo Automation Tests

Тестовое задание по автоматизация тестирования авторизации на сайте https://www.saucedemo.com/



# Используемые зависимости

1. pytest~=8.3.5
2. allure-pytest~=2.14.0
3. selenium~=4.31.0



# Тестовые сценарии

1. Успешный логин (standard_user / secret_sauce)
2. Логин с неверным паролем
3. Логин заблокированного пользователя (locked_out_user)
4. Логин с пустыми полями
5. Логин пользователем performance_glitch_user 



# Запуск с помощью Docker

## Собрать образ

docker build -t sauce-demo-tests .

## Запустить все тесты 

docker run --rm sauce-demo-tests

## Запустить все тесты с детальным выводом

docker run --rm sauce-demo-tests pytest -v



# Запуск тестов локально

## Установка зависимостей
pip install -r requirements.txt

## Запуск тестов локально
pytest tests/ -v

## Запуск с помощью allure
pytest tests/ --alluredir=allure-results -v

# Автор: Ефимов Алексей