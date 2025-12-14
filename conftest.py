import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


@allure.title("Подготовка драйвера")
@pytest.fixture(scope="function")
def chromedriver():
    """
    Фикстура для инициализации и закрытия браузера.
    """
    chrome_options = Options()

    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--disable-infobars')
    chrome_options.add_argument('--disable-browser-side-navigation')
    chrome_options.add_argument('--disable-features=VizDisplayCompositor')
    chrome_options.add_argument('--remote-debugging-port=9222')
    chrome_options.add_argument('--window-size=1920,1080')

    chrome_options.add_argument('--ignore-certificate-errors-spki-list')
    chrome_options.add_argument('--ignore-ssl-errors')

    chrome_options.add_argument('--disable-software-rasterizer')
    chrome_options.add_argument('--disable-features=IsolateOrigins,site-per-process')
    chrome_options.add_argument('--disable-background-networking')
    chrome_options.add_argument('--disable-default-apps')
    chrome_options.add_argument('--disable-sync')
    chrome_options.add_argument('--metrics-recording-only')
    chrome_options.add_argument('--disable-client-side-phishing-detection')
    chrome_options.add_argument('--disable-popup-blocking')
    chrome_options.add_argument('--disable-hang-monitor')
    chrome_options.add_argument('--disable-prompt-on-repost')
    chrome_options.add_argument('--disable-web-resources')
    chrome_options.add_argument('--enable-automation')

    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    chrome_options.add_argument(
        'user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36')

    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.implicitly_wait(10)

        driver.set_window_size(1920, 1080)

        yield driver
        driver.quit()
    except Exception as e:
        print(f"Ошибка при инициализации драйвера: {e}")
        raise