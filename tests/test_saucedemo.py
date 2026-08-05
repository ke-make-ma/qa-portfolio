import os
import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from config import get_browser_config

@pytest.fixture(params=["chrome", "firefox", "edge", "yandex"])
def driver(request):
    browser = request.param
    config = get_browser_config(browser)

    if browser == "chrome":
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=config.get("options"))

    elif browser == "firefox":
        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=config.get("options"))

    elif browser == "edge":
        service = EdgeService(EdgeChromiumDriverManager().install())
        driver = webdriver.Edge(service=service, options=config.get("options"))

    elif browser == "yandex":
        options = config.get("options") or ChromeOptions()
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_experimental_option("prefs", {
            "profile.default_content_setting_values.notifications": 2,
            "profile.default_content_setting_values.cookies": 1,
        })
        yandex_path = config.get("binary_path")
        if yandex_path is None or not os.path.exists(yandex_path):
            pytest.skip(f"Yandex browser path not found: {yandex_path}.")

        options = config.get("options") or ChromeOptions()
        options.binary_location = yandex_path

        service = ChromeService(ChromeDriverManager("148.0.7778.960").install())
        driver = webdriver.Chrome(service=service, options=options)

    else:
        raise ValueError(f"Unsupported browser: {browser}")

    driver.get("https://www.saucedemo.com")
    driver.implicitly_wait(5)
    yield driver
    driver.quit()


#Вспомогательные функции
def login(driver):
    time.sleep(1)
    username = driver.find_element(By.ID, "user-name")
    username.click()
    username.send_keys("standard_user")

    password = driver.find_element(By.ID, "password")
    password.click()
    password.send_keys("secret_sauce")

    driver.find_element(By.CSS_SELECTOR,"input[type='submit']").click()

def add_backpack_to_cart(driver):
    driver.find_element(By.ID,"add-to-cart-sauce-labs-backpack").click()

def go_to_cart(driver):
    driver.find_element(By.CLASS_NAME,"shopping_cart_link").click()

#Тесты
def test_login_success(driver):
    login(driver)
    #Проверка успешной авторизации - на сайте должен быть виден заголовок "Products"
    products_header = driver.find_element(By.CLASS_NAME, "title")
    assert products_header.text == "Products"


def test_login_error(driver):
    driver.find_element(By.ID,"user-name").send_keys("Wrong")
    driver.find_element(By.ID,"password").send_keys("Wrong")
    driver.find_element(By.CSS_SELECTOR,"input[type='submit']").click()

    error_message=driver.find_element(By.CSS_SELECTOR,"[data-test='error']")
    assert "Epic sadface: Username and password do not match any user in this service" in error_message.text


@pytest.mark.parametrize("item_id",
    ["add-to-cart-sauce-labs-bolt-t-shirt", 
    "add-to-cart-sauce-labs-fleece-jacket", 
    "add-to-cart-sauce-labs-bike-light"])
def test_add_to_cart(driver, item_id):
    login(driver)
    driver.find_element(By.ID, item_id).click()

    time.sleep(1)
    #Проверяем, что индикатор у корзины отображает добавление
    cart_badge = driver.find_element(By.CLASS_NAME, "shopping_cart_badge")
    assert int(cart_badge.text) == 1


def test_remove_from_cart(driver):
    login(driver)
    add_backpack_to_cart(driver)
    driver.find_element(By.ID,"remove-sauce-labs-backpack").click()

    time.sleep(1)
    badge_elements = driver.find_elements(By.CLASS_NAME, "shopping_cart_badge")
    assert len(badge_elements) == 0


def test_cart_contains_added_item(driver):
    login(driver)
    add_backpack_to_cart(driver)
    go_to_cart(driver)

    item_in_cart=driver.find_element(By.CLASS_NAME,"inventory_item_name")
    assert item_in_cart.text=="Sauce Labs Backpack"


def test_checkout(driver):
    login(driver)
    add_backpack_to_cart(driver)
    go_to_cart(driver)

    driver.find_element(By.ID,"checkout").click()

    driver.find_element(By.ID,"first-name").send_keys("Name")
    driver.find_element(By.ID,"last-name").send_keys("Second name")
    driver.find_element(By.ID,"postal-code").send_keys("Postal code")
    driver.find_element(By.ID,"continue").click()

    item_in_checkout = driver.find_element(By.CLASS_NAME, "inventory_item_name")
    assert item_in_checkout.text=="Sauce Labs Backpack"

    driver.find_element(By.ID,"finish").click()
    
    complete_banner=driver.find_element(By.CLASS_NAME,"complete-header")
    assert complete_banner.text=="Thank you for your order!"

def test_sort_a_to_z(driver):
    login(driver)
    driver.find_element(By.CLASS_NAME,"product_sort_container").click()
    driver.find_element(By.CSS_SELECTOR,"option[value='az']").click()
    inventory_items=driver.find_elements(By.CLASS_NAME,"inventory_item_name")
    item_names=[item.text for item in inventory_items]
    assert item_names == sorted(item_names)

def test_sort_z_to_a(driver):
    login(driver)
    driver.find_element(By.CLASS_NAME,"product_sort_container").click()
    driver.find_element(By.CSS_SELECTOR,"option[value='za']").click()
    inventory_items=driver.find_elements(By.CLASS_NAME,"inventory_item_name")
    item_names=[item.text for item in inventory_items]
    assert item_names == sorted(item_names,reverse=True)

@pytest.mark.parametrize("postal_code, should_error", [
    ("12345",False),    # валидный — ошибки нет
    (" ",False),        # пробел — ошибки нет
    ("@#!///", False),  # спецсимволы — ошибки нет
    ("",True)           # пустой — ошибка есть
    ])
def test_postal_code(driver,postal_code,should_error):
    login(driver)
    add_backpack_to_cart(driver)
    go_to_cart(driver)
    driver.find_element(By.CSS_SELECTOR,"[data-test='checkout']").click()

    driver.find_element(By.ID,"first-name").send_keys("Name")
    driver.find_element(By.ID,"last-name").send_keys("Second name")
    driver.find_element(By.ID,"postal-code").send_keys(postal_code)
    driver.find_element(By.ID,"continue").click()

    error_elements = driver.find_elements(By.CSS_SELECTOR, "[data-test='error']")

    if should_error:
        assert len(error_elements) == 1 # ошибка есть
    else:
        assert len(error_elements) == 0 # ошибки нет
        #assert "checkout-step-two" in driver.current_url