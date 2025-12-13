import allure
import pytest

from pages.login_page import LoginPage
from conf.config import (bad_password_error, empty_login_error,
                         locked_user_error, main_url,
                         page_title, url_after_login,
                         time_to_wait)


@pytest.fixture(scope="session")
def setup(chromedriver):
    """
    Фикстура для подготовки тестового окружения.

    Открывает главную страницу сайта перед выполнением тестов и возвращает
    инициализированный драйвер браузера.

    Args:
        chromedriver: Экземпляр WebDriver для управления браузером

    Returns:
        WebDriver: Готовый к работе драйвер с открытой главной страницей
    """
    chromedriver.get(main_url)
    return chromedriver

@allure.epic("Сайт Sauce")
@allure.feature("Автор")
@allure.title("Проверка регистрации")
@pytest.mark.parametrize("ok_login, ok_password, bad_password, locked_login, glitch_user", [("standard_user", "secret_sauce", "mfhtrr35252", "locked_out_user", "performance_glitch_user")])
def test_check_python_author_part(chromedriver, setup, ok_login, ok_password, bad_password, locked_login, glitch_user):
    """
    Комплексный тест для проверки различных сценариев авторизации на сайте Sauce Demo.

    Тест включает пять различных сценариев:
    1. Успешная авторизация с корректными учетными данными
    2. Авторизация с неверным паролем
    3. Авторизация заблокированного пользователя
    4. Авторизация с пустым логином
    5. Авторизация пользователя с возможными задержками

    Args:
        chromedriver: Экземпляр WebDriver для управления браузером
        setup: Фикстура для подготовки тестового окружения
        ok_login: Корректное имя пользователя для успешного входа
        ok_password: Корректный пароль для успешного входа
        bad_password: Неверный пароль для тестирования негативного сценария
        locked_login: Имя заблокированного пользователя
        glitch_user: Имя пользователя с возможными задержками при авторизации

    Raises:
        AssertionError: Если какой-либо из проверяемых сценариев не выполняется
    :param author: Автор
    :author: Alex Efimov
    """
    with allure.step("Выполнение захода на сайт"):
        chromedriver.implicitly_wait(time_to_wait)
        login_page = LoginPage(chromedriver)

        assert chromedriver.title == page_title, \
            "Заголовок страницы не совпадает с ожидаемым"

    with allure.step("Тест на корректную авторизацию"):
        login_page.send_text(ok_login, ok_password)
        assert login_page.is_login_field_displayed(time_to_wait), \
            "Переход на сайт не осуществлен"
        login_page.click_login_button()

        assert login_page.is_products_displayed(time_to_wait), \
            "Авторизация не успешна."

        current_url = chromedriver.current_url
        assert current_url == url_after_login, \
            "URL страницы не совпадает с оидаемым"

        chromedriver.get(main_url)
        login_page = LoginPage(chromedriver)

    with allure.step("Тест на не корректную авторизацию"):
        login_page.send_text(ok_login, bad_password)
        assert login_page.is_login_field_displayed(time_to_wait), \
            "Переход на сайт не осуществлен"
        login_page.click_login_button()

        assert login_page.is_error_displayed(timeout=time_to_wait), \
            "Сообщение об ошибке не отображается при неправильном пароле"

        error_text = login_page.get_error_text()
        print(f"Текст ошибки: {error_text}")

        assert bad_password_error in error_text, \
            f"Ожидалась ошибка '{bad_password_error}', но получено: '{error_text}'"

        current_url = chromedriver.current_url
        assert current_url == main_url, \
            f"После ошибки авторизации остаемся на странице логина. URL: {current_url}"

        chromedriver.get(main_url)
        login_page = LoginPage(chromedriver)


    with allure.step("Тест на заблокированного пользователя"):
        login_page.send_text(locked_login, ok_password)
        assert login_page.is_login_field_displayed(time_to_wait), \
            "Переход на сайт не осуществлен"
        login_page.click_login_button()

        assert login_page.is_error_displayed(timeout=time_to_wait), \
            "Сообщение об ошибке не отображается при неправильном пароле"

        error_text = login_page.get_error_text()
        print(f"Текст ошибки: {error_text}")

        assert locked_user_error in error_text, \
            f"Ожидалась ошибка '{locked_user_error}', но получено: '{error_text}'"

        current_url = chromedriver.current_url
        assert current_url == main_url, \
            f"После ошибки авторизации остаемся на странице логина. URL: {current_url}"

        chromedriver.get(main_url)
        login_page = LoginPage(chromedriver)

    with allure.step("Тест на пустой логин"):
        login_page.send_text_only_password(ok_password)
        assert login_page.is_login_field_displayed(time_to_wait), \
            "Переход на сайт не осуществлен"
        login_page.click_login_button()

        assert login_page.is_error_displayed(timeout=time_to_wait), \
            "Сообщение об ошибке не отображается при неправильном пароле"

        error_text = login_page.get_error_text()
        print(f"Текст ошибки: {error_text}")

        assert empty_login_error in error_text, \
            f"Ожидалась ошибка '{empty_login_error}', но получено: '{error_text}'"

        current_url = chromedriver.current_url
        assert current_url == main_url, \
            f"После ошибки авторизации остаемся на странице логина. URL: {current_url}"

        chromedriver.get(main_url)
        login_page = LoginPage(chromedriver)

    with allure.step("Тест на пользователя с ожиданием"):
        login_page.send_text(glitch_user, ok_password)
        assert login_page.is_login_field_displayed(time_to_wait), \
            "Переход на сайт не осуществлен"
        login_page.click_login_button()

        assert login_page.is_products_displayed(), \
            "Переход на страницу не осуществялется."

        current_url = chromedriver.current_url
        assert current_url == url_after_login, \
            "URL страницы не совпадает с оидаемым"
