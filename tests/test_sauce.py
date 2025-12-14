import allure
import pytest

from pages.login_page import LoginPage
from conf.config import (
    BAD_PASSWORD_ERROR,
    EMPTY_LOGIN_ERROR,
    LOCKED_USER_ERROR,
    MAIN_URL,
    PAGE_TITLE,
    URL_AFTER_LOGIN,
    TIME_TO_WAIT,
)


@allure.epic("Сайт Sauce Demo")
@allure.feature("Авторизация пользователей")
class TestLogin:
    @allure.title("1. Успешная авторизация стандартного пользователя")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.description("""
    Проверка успешной авторизации с корректными учетными данными.
    Ожидается переход на страницу товаров и отображение элементов интерфейса.
    """)
    @pytest.mark.parametrize(
        "username,password",
        [("standard_user", "secret_sauce")]
    )
    def test_successful_login(self, chromedriver, username, password):
        """
        Тест успешной авторизации пользователя standard_user.

        Args:
            driver: Экземпляр WebDriver
            username: Имя пользователя
            password: Пароль
        """
        with allure.step("1. Открыть главную страницу"):
            chromedriver.get(MAIN_URL)
            login_page = LoginPage(chromedriver)
            assert chromedriver.title == PAGE_TITLE, (
                f"Заголовок страницы должен быть '{PAGE_TITLE}'"
            )

        with allure.step("2. Проверить, что кнопка Login доступна"):
            assert login_page.is_login_button_clickable(TIME_TO_WAIT), (
                "Кнопка Login должна быть кликабельной"
            )

        with allure.step(f"3. Ввести логин '{username}' и пароль '{password}'"):
            login_page.send_text(username, password)

        with allure.step("4. Нажать кнопку Login"):
            login_page.click_login_button()

        with allure.step("5. Проверить успешную авторизацию"):
            current_url = chromedriver.current_url
            assert current_url == URL_AFTER_LOGIN, (
                f"После успешного входа URL должен быть '{URL_AFTER_LOGIN}'"
            )

            assert login_page.is_products_displayed(
                timeout=TIME_TO_WAIT
            ), "После успешного входа должен отображаться заголовок 'Products'"

            assert "inventory.html" in chromedriver.current_url, (
                "URL должен содержать 'inventory.html'"
            )

            allure.attach(
                chromedriver.get_screenshot_as_png(),
                name="successful_login",
                attachment_type=allure.attachment_type.PNG,
            )

    @allure.title("2. Авторизация с неверным паролем")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("""
    Проверка авторизации с правильным логином, но неправильным паролем.
    Ожидается сообщение об ошибке и отсутствие перехода на страницу товаров.
    """)
    @pytest.mark.parametrize(
        "username,password",
        [("standard_user", "wrong_password_123")]
    )
    def test_wrong_password_login(self, chromedriver, username, password):
        """Тест авторизации с неверным паролем."""
        with allure.step("1. Открыть главную страницу"):
            chromedriver.get(MAIN_URL)
            login_page = LoginPage(chromedriver)

        with allure.step("2. Ввести правильный логин и неправильный пароль"):
            login_page.send_text(username, password)

        with allure.step("3. Нажать кнопку Login"):
            login_page.click_login_button()

        with allure.step("4. Проверить сообщение об ошибке"):
            assert login_page.is_error_displayed(
                timeout=TIME_TO_WAIT
            ), "При неверном пароле должно отображаться сообщение об ошибке"

            error_text = login_page.get_error_text()
            print(f"Текст ошибки: {error_text}")

            assert BAD_PASSWORD_ERROR in error_text, (
                f"Текст ошибки должен содержать: '{BAD_PASSWORD_ERROR}'"
            )

        with allure.step("5. Проверить, что остались на странице логина"):
            current_url = chromedriver.current_url
            assert current_url == MAIN_URL, (
                f"После ошибки должны оставаться на странице логина. "
                f"URL: {current_url}"
            )

            allure.attach(
                chromedriver.get_screenshot_as_png(),
                name="wrong_password_error",
                attachment_type=allure.attachment_type.PNG,
            )

    @allure.title("3. Авторизация заблокированного пользователя")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("""
    Проверка авторизации пользователя locked_out_user.
    Ожидается сообщение об ошибке блокировки.
    """)
    @pytest.mark.parametrize(
        "username,password",
        [("locked_out_user", "secret_sauce")]
    )
    def test_locked_user_login(self, chromedriver, username, password):
        """Тест авторизации заблокированного пользователя."""
        with allure.step("1. Открыть главную страницу"):
            chromedriver.get(MAIN_URL)
            login_page = LoginPage(chromedriver)

        with allure.step("2. Ввести данные заблокированного пользователя"):
            login_page.send_text(username, password)

        with allure.step("3. Нажать кнопку Login"):
            login_page.click_login_button()

        with allure.step("4. Проверить сообщение об ошибке блокировки"):
            assert login_page.is_error_displayed(
                timeout=TIME_TO_WAIT
            ), "Для заблокированного пользователя должно отображаться сообщение об ошибке"

            error_text = login_page.get_error_text()
            print(f"Текст ошибки: {error_text}")

            assert LOCKED_USER_ERROR in error_text, (
                f"Текст ошибки должен содержать: '{LOCKED_USER_ERROR}'"
            )

        with allure.step("5. Проверить, что остались на странице логина"):
            current_url = chromedriver.current_url
            assert current_url == MAIN_URL, (
                "После ошибки должны оставаться на странице логина"
            )

    @allure.title("4. Авторизация с пустым логином")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("""
    Проверка авторизации с пустым полем логина.
    Ожидается сообщение об ошибке 'Username is required'.
    """)
    @pytest.mark.parametrize("password", ["secret_sauce"])
    def test_empty_login(self, chromedriver, password):
        """Тест авторизации с пустым логином."""
        with allure.step("1. Открыть главную страницу"):
            chromedriver.get(MAIN_URL)
            login_page = LoginPage(chromedriver)

        with allure.step("2. Ввести только пароль"):
            login_page.send_text_only_password(password)

        with allure.step("3. Нажать кнопку Login"):
            login_page.click_login_button()

        with allure.step("4. Проверить сообщение об ошибке"):
            assert login_page.is_error_displayed(
                timeout=TIME_TO_WAIT
            ), "При пустом логине должно отображаться сообщение об ошибке"

            error_text = login_page.get_error_text()
            print(f"Текст ошибки: {error_text}")

            assert EMPTY_LOGIN_ERROR in error_text, (
                f"Текст ошибки должен содержать: '{EMPTY_LOGIN_ERROR}'"
            )

        with allure.step("5. Проверить, что остались на странице логина"):
            current_url = chromedriver.current_url
            assert current_url == MAIN_URL, (
                "После ошибки должны оставаться на странице логина"
            )

    @allure.title("5. Авторизация пользователя с задержками")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("""
    Проверка авторизации пользователя performance_glitch_user.
    Ожидается успешный вход, несмотря на возможные задержки при загрузке.
    """)
    @pytest.mark.parametrize(
        "username,password",
        [("performance_glitch_user", "secret_sauce")]
    )
    def test_performance_glitch_user(self, chromedriver, username, password):
        """Тест авторизации пользователя с возможными задержками."""
        with allure.step("1. Открыть главную страницу"):
            chromedriver.get(MAIN_URL)
            login_page = LoginPage(chromedriver)

        with allure.step("2. Ввести данные пользователя с задержками"):
            login_page.send_text(username, password)

        with allure.step("3. Нажать кнопку Login"):
            login_page.click_login_button()

        with allure.step("4. Проверить успешную авторизацию с учетом задержек"):
            assert login_page.is_products_displayed(TIME_TO_WAIT), (
                "Заголовок 'Products' должен отображаться, несмотря на задержки"
            )

            current_url = chromedriver.current_url
            assert current_url == URL_AFTER_LOGIN, (
                f"После успешного входа URL должен быть '{URL_AFTER_LOGIN}'"
            )

            assert "Products" in chromedriver.page_source, (
                "На странице должен быть текст 'Products'"
            )

            allure.attach(
                chromedriver.get_screenshot_as_png(),
                name="performance_glitch_user_login",
                attachment_type=allure.attachment_type.PNG,
            )
