import os
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions

def get_chrome_options():
    chrome_prefs = {
        "profile.password_manager_leak_detection": False,
        "profile.password_manager_enabled": False,
        "credentials_enable_service": False
    }
    options = ChromeOptions()
    options.add_experimental_option("prefs", chrome_prefs)
    return options

def get_browser_config(browser_name):
    yandex_path = os.getenv("YANDEX_BROWSER_PATH")
    
    configs = {
        "chrome": {
            "options": get_chrome_options(),
            "driver_manager": "chromedriver",
            "binary_path": None
        },
        "firefox": {
            "options": FirefoxOptions(),
            "driver_manager": "geckodriver",
            "binary_path": None
        },
        "edge": {
            "options": EdgeOptions(),
            "driver_manager": "msedgedriver",
            "binary_path": None
        },
        "yandex": {
            "options": ChromeOptions(),
            "driver_manager": "chromedriver",
            "binary_path": yandex_path
}
    }
    return configs.get(browser_name)