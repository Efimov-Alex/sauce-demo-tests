from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class LoginPage:
    """
    Page Object Model для страницы авторизации сайта Sauce Demo.

    Этот класс инкапсулирует все взаимодействия с элементами страницы логина,
    предоставляя методы для ввода данных, нажатия кнопок и проверки состояния
    элементов.

    Attributes:
        driver: Экземпляр WebDriver для управления браузером
        wait: Объект WebDriverWait для явных ожиданий
        login_field: Локатор поля для ввода имени пользователя
        password_field: Локатор поля для ввода пароля
        login_button: Локатор кнопки входа
        error_head: Локатор элемента с сообщением об ошибке
        products_title: Локатор заголовка страницы товаров

    """

    login_field = (By.XPATH, "//input[@placeholder='Username']")
    password_field = (By.XPATH, "//input[@placeholder='Password']")
    login_button = (By.XPATH, "//input[@type='submit']")
    error_head = (By.XPATH, "//h3[@data-test='error']")
    products_title = (By.XPATH, "//span[@class='title' and text()='Products']")

    def __init__(self, driver):
        """
        Инициализирует объект LoginPage и ожидает загрузки основных элементов.

        При создании экземпляра класса автоматически ожидает появления
        и инициализирует основные элементы страницы: поля логина, пароля
        и кнопку входа.

        Args:
            driver: Экземпляр WebDriver для управления браузером

        Raises:
            TimeoutException: Если какой-либо из элементов не появился
                              в течение заданного времени ожидания
        """
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

    def send_text(self, login, password):
        """
        Вводит данные в поля логина и пароля.

        Очищает поля и вводит указанные значения. Этот метод используется
        для стандартного сценария авторизации с заполнением обоих полей.

        Args:
            login: Имя пользователя для входа
            password: Пароль для входа

        Returns:
            None
        """
        username_field = self.wait.until(
            EC.visibility_of_element_located(self.login_field)
        )
        username_field.clear()
        username_field.send_keys(login)

        password_field = self.wait.until(
            EC.visibility_of_element_located(self.password_field)
        )
        password_field.clear()
        password_field.send_keys(password)

    def send_text_only_password(self, password):
        """
        Вводит только пароль, оставляя поле логина пустым.

        Используется для тестирования сценария авторизации с пустым логином.

        Args:
            password: Пароль для ввода

        Returns:
            None
        """
        password_field = self.wait.until(
            EC.visibility_of_element_located(self.password_field)
        )
        password_field.clear()
        password_field.send_keys(password)

    def click_login_button(self):
        """
        Нажимает на кнопку входа (Login).

        Выполняет клик по кнопке авторизации после заполнения полей
        или для проверки поведения при пустых полях.

        Returns:
            None
        """
        login_button = self.wait.until(
            EC.element_to_be_clickable(self.login_button)
        )
        login_button.click()

    def is_error_displayed(self, timeout=10):
        """
        Проверяет, отображается ли сообщение об ошибке авторизации.

        Ожидает появления элемента с сообщением об ошибке в течение
        указанного времени и проверяет его видимость.

        Args:
            timeout: Максимальное время ожидания появления элемента в секундах.
                     По умолчанию 10 секунд.

        Returns:
            bool: True если элемент ошибки отображается, False в противном случае
                  или если элемент не появился в течение timeout.
        """
        try:
            wait = WebDriverWait(self.driver, timeout)
            error_element = wait.until(
                EC.presence_of_element_located(self.error_head)
            )
            return error_element.is_displayed()
        except Exception:
            return False

    def get_error_text(self, timeout=10):
        """
        Получает текст сообщения об ошибке авторизации.

        Ожидает появления и видимости элемента с ошибкой, затем возвращает
        его текстовое содержимое.

        Args:
            timeout: Максимальное время ожидания появления элемента в секундах.
                     По умолчанию 10 секунд.

        Returns:
            str: Текст сообщения об ошибке или пустая строка, если элемент
                 не найден или не стал видимым в течение timeout.
        """
        try:
            wait = WebDriverWait(self.driver, timeout)
            error_element = wait.until(
                EC.visibility_of_element_located(self.error_head)
            )
            return error_element.text
        except Exception:
            return ""

    def clear_fields(self):
        """
        Очищает поля логина и пароля.

        Удаляет любой текст, введенный в поля ввода. Полезно для подготовки
        к следующему тестовому сценарию без перезагрузки страницы.

        Returns:
            None
        """
        username_field = self.wait.until(
            EC.visibility_of_element_located(self.login_field)
        )
        username_field.clear()

        password_field = self.wait.until(
            EC.visibility_of_element_located(self.password_field)
        )
        password_field.clear()

    def is_products_displayed(self, timeout=30):
        """
        Проверяет, отображается ли заголовок 'Products' после успешного входа.

        Используется для подтверждения успешной авторизации и перехода
        на страницу товаров. Ожидает появления элемента с заголовком
        в течение указанного времени.

        Args:
            timeout: Максимальное время ожидания появления элемента в секундах.
                     По умолчанию 30 секунд для учета возможных задержек.

        Returns:
            bool: True если заголовок 'Products' отображается, False в противном случае
                  или если элемент не появился в течение timeout.
        """
        try:
            wait = WebDriverWait(self.driver, timeout)
            error_element = wait.until(
                EC.presence_of_element_located(self.products_title)
            )
            return error_element.is_displayed()
        except Exception:
            return False

    def is_login_button_clickable(self, timeout=30):
        """
        Проверяет, отображается ли и доступно ли поле логина для ввода.

        Ожидает, пока кнопка входа (Login) станет кликабельной, что является
        индикатором готовности страницы к взаимодействию.

        Args:
            timeout: Максимальное время ожидания кликабельности элемента в секундах.
                     По умолчанию 30 секунд.

        Returns:
            bool: True если кнопка Login отображается и активна, False в противном случае
                  или если элемент не стал кликабельным в течение timeout.

        Raises:
            Exception: Логирует информацию об ошибке, если таймаут истек
        """
        try:
            wait = WebDriverWait(self.driver, timeout)
            login_btn = wait.until(
                EC.element_to_be_clickable(self.login_button)
            )
            return login_btn.is_displayed() and login_btn.is_enabled()
        except Exception as e:
            print(
                f"Поле логина не стало кликабельным за {timeout} секунд: {e}"
            )
            return False

