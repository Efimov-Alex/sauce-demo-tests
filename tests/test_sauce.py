import allure
import pytest

from pages.login_page import LoginPage


main_url = 'https://www.saucedemo.com/'


@pytest.fixture(scope="session")
def setup(chromedriver):
    chromedriver.get(main_url)
    return chromedriver

@allure.epic("Сайт Sauce")
@allure.feature("Автор")
@allure.title("Проверка регистрации")
@pytest.mark.parametrize("ok_login, ok_password, bad_password, locked_login", [("standard_user", "secret_sauce", "123", "locked_out_user")])
def test_check_python_author_part(chromedriver, setup, ok_login, ok_password, bad_password, locked_login):
    """
    :param author: Автор
    :author: Alex Efimov
    """
    with allure.step("Выполнение захода на сайт"):
        chromedriver.implicitly_wait(30)
        login_page = LoginPage(chromedriver)
        assert chromedriver.title == "Swag Labs", \
            "Заголовок страницы не совпадает с оидаемым"

    with allure.step("Тест на корректную авторизацию"):
        login_page.send_text(ok_login, ok_password)
        chromedriver.implicitly_wait(10)
        login_page.click_login_button()
        chromedriver.implicitly_wait(15)
        current_url = chromedriver.current_url
        assert current_url == "https://www.saucedemo.com/inventory.html", \
            "URL страницы не совпадает с оидаемым"

        chromedriver.get(main_url)
        login_page = LoginPage(chromedriver)

    with allure.step("Тест на не корректную авторизацию"):
        login_page.send_text(ok_login, bad_password)
        chromedriver.implicitly_wait(10)
        login_page.click_login_button()
        chromedriver.implicitly_wait(15)

        assert login_page.is_error_displayed(timeout=5), \
            "Сообщение об ошибке не отображается при неправильном пароле"

        error_text = login_page.get_error_text()
        print(f"Текст ошибки: {error_text}")

        expected_error = "Username and password do not match any user in this service"
        assert expected_error in error_text, \
            f"Ожидалась ошибка '{expected_error}', но получено: '{error_text}'"

        current_url = chromedriver.current_url
        assert current_url == main_url, \
            f"После ошибки авторизации остаемся на странице логина. URL: {current_url}"

        chromedriver.get(main_url)
        login_page = LoginPage(chromedriver)


    with allure.step("Тест на заблокированного пользователя"):
        login_page.send_text(locked_login, ok_password)
        chromedriver.implicitly_wait(10)
        login_page.click_login_button()
        chromedriver.implicitly_wait(15)

        assert login_page.is_error_displayed(timeout=5), \
            "Сообщение об ошибке не отображается при неправильном пароле"

        error_text = login_page.get_error_text()
        print(f"Текст ошибки: {error_text}")

        expected_error = "Epic sadface: Sorry, this user has been locked out."
        assert expected_error in error_text, \
            f"Ожидалась ошибка '{expected_error}', но получено: '{error_text}'"

        current_url = chromedriver.current_url
        assert current_url == main_url, \
            f"После ошибки авторизации остаемся на странице логина. URL: {current_url}"

        chromedriver.get(main_url)
        login_page = LoginPage(chromedriver)
