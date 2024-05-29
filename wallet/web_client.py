import datetime
import json
import os.path
import threading
import time

from selenium.common import TimeoutException
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from seleniumwire import webdriver


class Client:
    def __init__(self, headless: bool = True, profile: str = 'main', temp_dir_path: str = None,
                 page_load_strategy='none'):
        """

        :param headless: hide or open browser
        :param profile: chrome profile
        :param temp_dir_path: profiles directory
        :param page_load_strategy: https://www.selenium.dev/documentation/webdriver/drivers/options/
        """
        self.receiver_id = None

        full_dir_path = '_temp/profile_' + str(profile)
        if not os.path.isdir(full_dir_path):
            os.makedirs(full_dir_path)
            self.auth(profile=profile, temp_dir_path=temp_dir_path)
        if temp_dir_path is None:
            temp_dir_path = os.getcwd() + '\\_temp\\' + 'profile_' + str(profile)
        os.makedirs(temp_dir_path, exist_ok=True)

        options = ChromeOptions()
        options.add_argument(f"--user-data-dir={temp_dir_path}")
        options.page_load_strategy = page_load_strategy
        if headless:
            options.add_argument('--headless=new')

        self.driver = webdriver.Chrome(chrome_options=options)
        self.driver.implicitly_wait(7)

    @classmethod
    def auth(cls, profile, temp_dir_path=None):
        c = Client(headless=False, profile=profile, temp_dir_path=temp_dir_path)
        start_page = "https://web.telegram.org/a/#1985737506"
        c.driver.get(start_page)
        print("Connect Telegram Account")

        try:
            WebDriverWait(c.driver, 5).until(
                EC.presence_of_element_located((By.ID, 'auth-qr-form'))
            )
            print('Auth by QR')

            while True:
                if c.driver.current_url == start_page:
                    return c
                else:
                    time.sleep(1)

        except Exception as e:
            pass

    def _parse_token(self, wallet_endpoint):
        try:
            iframe = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, 'iframe'))
            )
        except Exception as e:
            raise Exception('Iframe not find! Try start client with attr "headless"=True to recognize problem')

        self.driver.switch_to.frame(iframe)

        check_limit = 10
        start_t = time.time()
        while start_t + check_limit > time.time():
            for request in self.driver.requests:
                if wallet_endpoint in request.url:
                    if 'v1/users/auth/' in request.url:
                        init_data = json.loads(request.body.decode('utf-8'))
                        self.receiver_id = init_data['web_view_init_data']['receiver']['id']
                    if 'authorization' in request.headers:
                        token = request.headers['authorization']
                        if 'Bearer' in token:
                            token = token.split()[1]
                        if not token:
                            raise Exception('Token not find')
                        return token
            time.sleep(0.5)
        raise Exception('Token not find')

    def get_token(self, username: str = 'wallet', wallet_endpoint='walletbot.me') -> str:
        self._log('Start parse token')
        start_t = time.time()

        self.driver.get(
            f"https://web.telegram.org/k/#?tgaddr=tg%3A%2F%2Fresolve%3Fdomain%3D{username}%26attach%3Dwallet")
        threading.Thread(target=self._confirm_popup, daemon=False).start()

        token = self._parse_token(wallet_endpoint)
        self._log(f'Token find. Time spent: {round(time.time() - start_t, 2)} sec')
        return token

    @staticmethod
    def _log(m):
        print(f"[{datetime.datetime.now()}] {m}")

    def _confirm_popup(self):
        try:
            element = WebDriverWait(self.driver, 2).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'popup-button')))
            if element:
                element.click()
        except TimeoutException:
            pass

    def stop(self):
        self.driver.quit()
