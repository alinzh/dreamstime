from selenium import webdriver
import time
import random
import pickle
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import yaml

class Dreamstime():
    """
    This class is designed to work with a photo-bank site.
    """
    def __init__(self):
        self.user_agents = [
            "Mozilla/5.0 (Linux; U; Android 4.2.2; he-il; NEO-X5-116A Build/JDQ39) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Safari/534.30",
            "Mozilla/5.0 (PlayStation; PlayStation 5/2.26) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0 Safari/605.1.15",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36",
            "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1",
            "Mozilla/5.0 (Linux; Android 5.0.2; SAMSUNG SM-T550 Build/LRX22G) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/3.3 Chrome/38.0.2125.102 Safari/537.36"
        ]
        with open('config.yaml') as f:
            personal_data = yaml.safe_load(f)
        print(f"Your login is: {personal_data['login']}, password: {personal_data['password']}")
        self.random_user_agent = random.choice(self.user_agents)
        self.login = personal_data['login']
        self.password = personal_data['password']
        self.options = webdriver.ChromeOptions()
        self.options.add_argument(f"user-agent={self.random_user_agent}")
        self.browser = webdriver.Chrome(options=self.options)

    def autorization(self):
        """
        Performs authorization.
        The function opens the photo-bank page. Enters personal data.
        Usually, after an authorization attempt, a captcha page appears.
        """
        try:
            self.browser.get('https://dreamstime.com/')
            time.sleep(7)

            wait = WebDriverWait(self.browser, 9)

            entry_button = wait.until(EC.presence_of_element_located((
                By.CSS_SELECTOR,
                'body > header > div.h-top.js-header-top > div > div > div > '
                'a.h-login__btn.h-login__btn--sign-in.js-loginform-trigger'
            )))
            entry_button.click()
            time.sleep(6)
            login_field = wait.until(EC.presence_of_element_located((
                By.CSS_SELECTOR, '#loginfrm > div.login-form__row.login-form__row--user > input'
            )))
            login_field.clear()
            login_field.send_keys(self.login)
            time.sleep(5)

            password_field = wait.until(EC.presence_of_element_located((
                By.CSS_SELECTOR, '#loginfrm > div.login-form__row.login-form__row--pass > input'
            )))
            password_field.clear()
            password_field.send_keys(self.password)
            time.sleep(2)

            loginin_button = wait.until(EC.presence_of_element_located((
                By.CSS_SELECTOR, '#loginfrm > button'
            )))
            loginin_button.click()
            time.sleep(4)

            # Here is saved cookies.
            pickle.dump(self.browser.get_cookies(), open("personal_data_cookies", "wb"))
            print('Authorization is success')
            self.browser.close()
            self.browser.quit()

        except Exception:
            print('Authorization failed. Reason: captcha.')

    def check_ip(self):
        """
        Checks ip-addresses.
        """
        self.browser.get('https://2ip.ru')
        time.sleep(20)

    def loader(self, pictures):
        """
        Not implemented.
        This function is supposed to do the loading of images.
        The function must be called after authorization.
        """
        time.sleep(5)
        wait = WebDriverWait(self.browser, 10)
        self.browser.get('https://dreamstime.com/upload')
        loader_field = wait.until(EC.presence_of_element_located((
            By.CSS_SELECTOR, '#js-uploadbox'
        )))
        loader_field.send_keys(pictures)
        time.sleep(30)

dt = Dreamstime()
dt.autorization()