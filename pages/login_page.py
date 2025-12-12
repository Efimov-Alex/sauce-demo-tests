from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class LoginPage:
    """
    Сайт для регистрации
    """

    login_field = (By.XPATH, "//input[@placeholder='Username']")

    password_field = (By.XPATH, "//input[@placeholder='Password']")

    loging_button = (By.XPATH, "//input[@type='submit']")

    error_head = (By.XPATH, "//h3[@data-test='error']")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

        self.login_field = self.wait.until(
            EC.presence_of_element_located(self.login_field)
        )

        self.password_field = self.wait.until(
            EC.presence_of_element_located(self.password_field)
        )

        self.loging_button = self.wait.until(
            EC.presence_of_element_located(self.loging_button)
        )

    def send_text(self, login, password):
        """
        Отправка текста в поле логина и пароля.
        """
        self.login_field.clear()
        self.login_field.send_keys(login)
        self.password_field.clear()
        self.password_field.send_keys(password)

    def click_login_button(self):
        """
        Нажатие на кнопку Login
        """
        self.loging_button.click()


    def is_error_displayed(self, timeout=10):
        """
        Проверяет, отображается ли сообщение об ошибке

        Args:
            timeout: время ожидания в секундах

        Returns:
            bool: True если ошибка отображается, False в противном случае
        """
        try:
            wait = WebDriverWait(self.driver, timeout)
            error_element = wait.until(
                EC.presence_of_element_located(self.error_head)
            )
            return error_element.is_displayed()
        except:
            return False

    def get_error_text(self, timeout=10):
        """
        Получает текст сообщения об ошибке

        Args:
            timeout: время ожидания в секундах

        Returns:
            str: текст ошибки или пустая строка если ошибка не найдена
        """
        try:
            wait = WebDriverWait(self.driver, timeout)
            error_element = wait.until(
                EC.visibility_of_element_located(self.error_head)
            )
            return error_element.text
        except:
            return ""

    def clear_fields(self):
        """
        Очищает поля логина и пароля
        """
        self.login_field.clear()
        self.password_field.clear()


