import os.path
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from wallet.selenium import TelegramDriver


class Client:
    def __init__(self, headless=True, profile='main', temp_dir_path=None):

        full_dir_path = '_temp/profile_' + str(profile)
        if not os.path.isdir(full_dir_path):
            os.makedirs(full_dir_path)
            self.auth(profile=profile, temp_dir_path=temp_dir_path)

        self.tgd = TelegramDriver(profile=profile, is_headless=headless, temp_dir_path=temp_dir_path)
        self.driver = self.tgd.driver
        self.driver.get('https://web.telegram.org/a/#1985737506')

    @classmethod
    def auth(cls, profile, temp_dir_path=None):
        c = Client(headless=False, profile=profile, temp_dir_path=temp_dir_path)
        print('[!] Connect Telegram Account')

        while True:
            if c.driver.current_url == 'https://web.telegram.org/a/#1985737506':
                return c
            else:
                time.sleep(1)

    def get_token(self) -> str:
        print('[*] Starting parse wallet authorization token...')
        self.driver.find_element(By.CLASS_NAME, 'middle-column-footer').find_element(By.CLASS_NAME, 'mounted')\
            .find_element(By.CLASS_NAME, 'message-input-wrapper').find_element(By.TAG_NAME, 'button').click()

        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, 'iframe'))
            )
        except Exception as e:
            raise Exception('[!] Iframe not find! Try start client with attr "headless"=True to recognize problem')

        self.driver.switch_to.frame(self.driver.find_element(By.TAG_NAME, 'iframe'))

        time.sleep(2)

        for request in self.driver.requests:
            if 'walletbot.me' in request.url:
                if 'authorization' in request.headers:
                    token = request.headers['authorization']

                    if 'Bearer' in token:
                        token = token.split()[1]

                    print(f'[*] Token find: {token}')
                    return token
