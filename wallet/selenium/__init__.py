import os

from selenium.webdriver import ChromeOptions
from seleniumwire import webdriver

MAX_ATTEMPTS = 10
DELAY = 0.5


class TelegramDriver:
    def __init__(self, profile, is_headless=False, temp_dir_path=None):
        self.base_inline = None
        if temp_dir_path is None:
            temp_dir_path = os.getcwd() + '\\_temp\\' + 'profile_' + str(profile)

        os.makedirs(temp_dir_path, exist_ok=True)

        options = ChromeOptions()
        options.add_argument(f"--user-data-dir={temp_dir_path}")

        if is_headless:
            options.add_argument('--headless')

        self.driver = webdriver.Chrome(chrome_options=options)

        self.driver.implicitly_wait(7)
