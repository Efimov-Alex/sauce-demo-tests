import allure
import pytest

from pages.login_page import LoginPage
from conf.config import (
    bad_password_error,
    empty_login_error,
    locked_user_error,
    main_url,
    page_title,
    url_after_login,
    time_to_wait,
)


@pytest.fixture(scope="function")
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
            chromedriver.get(main_url)
            login_page = LoginPage(chromedriver)
            assert chromedriver.title == page_title, (
                f"Заголовок страницы должен быть '{page_title}'"
            )

        with allure.step("2. Проверить, что кнопка Login доступна"):
            assert login_page.is_login_button_clickable(time_to_wait), (
                "Кнопка Login должна быть кликабельной"
            )

        with allure.step(f"3. Ввести логин '{username}' и пароль '{password}'"):
            login_page.send_text(username, password)

        with allure.step("4. Нажать кнопку Login"):
            login_page.click_login_button()

        with allure.step("5. Проверить успешную авторизацию"):
            current_url = chromedriver.current_url
            assert current_url == url_after_login, (
                f"После успешного входа URL должен быть '{url_after_login}'"
            )

            assert login_page.is_products_displayed(
                timeout=time_to_wait
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
            chromedriver.get(main_url)
            login_page = LoginPage(chromedriver)

        with allure.step("2. Ввести правильный логин и неправильный пароль"):
            login_page.send_text(username, password)

        with allure.step("3. Нажать кнопку Login"):
            login_page.click_login_button()

        with allure.step("4. Проверить сообщение об ошибке"):
            assert login_page.is_error_displayed(
                timeout=time_to_wait
            ), "При неверном пароле должно отображаться сообщение об ошибке"

            error_text = login_page.get_error_text()
            print(f"Текст ошибки: {error_text}")

            assert bad_password_error in error_text, (
                f"Текст ошибки должен содержать: '{bad_password_error}'"
            )

        with allure.step("5. Проверить, что остались на странице логина"):
            current_url = chromedriver.current_url
            assert current_url == main_url, (
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
            chromedriver.get(main_url)
            login_page = LoginPage(chromedriver)

        with allure.step("2. Ввести данные заблокированного пользователя"):
            login_page.send_text(username, password)

        with allure.step("3. Нажать кнопку Login"):
            login_page.click_login_button()

        with allure.step("4. Проверить сообщение об ошибке блокировки"):
            assert login_page.is_error_displayed(
                timeout=time_to_wait
            ), "Для заблокированного пользователя должно отображаться сообщение об ошибке"

            error_text = login_page.get_error_text()
            print(f"Текст ошибки: {error_text}")

            assert locked_user_error in error_text, (
                f"Текст ошибки должен содержать: '{locked_user_error}'"
            )

        with allure.step("5. Проверить, что остались на странице логина"):
            current_url = chromedriver.current_url
            assert current_url == main_url, (
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
            chromedriver.get(main_url)
            login_page = LoginPage(chromedriver)

        with allure.step("2. Ввести только пароль"):
            login_page.send_text_only_password(password)

        with allure.step("3. Нажать кнопку Login"):
            login_page.click_login_button()

        with allure.step("4. Проверить сообщение об ошибке"):
            assert login_page.is_error_displayed(
                timeout=time_to_wait
            ), "При пустом логине должно отображаться сообщение об ошибке"

            error_text = login_page.get_error_text()
            print(f"Текст ошибки: {error_text}")

            assert empty_login_error in error_text, (
                f"Текст ошибки должен содержать: '{empty_login_error}'"
            )

        with allure.step("5. Проверить, что остались на странице логина"):
            current_url = chromedriver.current_url
            assert current_url == main_url, (
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
            chromedriver.get(main_url)
            login_page = LoginPage(chromedriver)

        with allure.step("2. Ввести данные пользователя с задержками"):
            login_page.send_text(username, password)

        with allure.step("3. Нажать кнопку Login"):
            login_page.click_login_button()

        with allure.step("4. Проверить успешную авторизацию с учетом задержек"):
            assert login_page.is_products_displayed(time_to_wait), (
                "Заголовок 'Products' должен отображаться, несмотря на задержки"
            )

            current_url = chromedriver.current_url
            assert current_url == url_after_login, (
                f"После успешного входа URL должен быть '{url_after_login}'"
            )

            assert "Products" in chromedriver.page_source, (
                "На странице должен быть текст 'Products'"
            )

            allure.attach(
                chromedriver.get_screenshot_as_png(),
                name="performance_glitch_user_login",
                attachment_type=allure.attachment_type.PNG,
            )
