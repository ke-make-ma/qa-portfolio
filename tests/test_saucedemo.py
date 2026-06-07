from selenium import webdriver
from selenium.webdriver.common.by import By
import pytest

@pytest.fixture
def driver():
    driver = webdriver.Firefox()
    driver.get("https://www.saucedemo.com")
    yield driver
    driver.quit()

#Вспомогательные функции
def login(driver):
    driver.find_element(By.ID,"user-name").send_keys("standard_user")
    driver.find_element(By.ID,"password").send_keys("secret_sauce")
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

    #Проверяем, что индикатор у корзины отображает добавление
    cart_badge=driver.find_element(By.CLASS_NAME,"shopping_cart_badge")
    assert int(cart_badge.text) == 1


def test_remove_from_cart(driver):
    login(driver)
    add_backpack_to_cart(driver)
    driver.find_element(By.ID,"remove-sauce-labs-backpack").click()
    badge_elements=driver.find_elements(By.CLASS_NAME,"shopping_cart_badge")
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

    item_in_checkout=driver.find_element(By.CLASS_NAME,"inventory_item_name")
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


#empty: Error: Postal Code is required. "#@&" or "///" - proceeds

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
    
    error_elements=driver.find_elements(By.CSS_SELECTOR,"[data-test='error']")
    if should_error:
        assert len(error_elements) == 1  # ошибка есть
    else:
        assert len(error_elements) == 0  # ошибки нет

