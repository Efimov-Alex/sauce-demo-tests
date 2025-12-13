import allure
import pytest
from selenium import webdriver


@allure.title("Подготовка драйвера")
@pytest.fixture(scope="function")
def chromedriver():
    """
    Фикстура для инициализации и закрытия браузера.
    """
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors-spki-list')
    options.add_argument('--ignore-ssl-errors')

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    driver.maximize_window()

    yield driver
    driver.quit()
