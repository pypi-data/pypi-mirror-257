import os
import json
import logging
import pickle
import time
import datetime
import dotenv
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from seleniumbase import Driver
from selenium.webdriver.support import expected_conditions as EC
from .exceptions import APIError
dotenv_file = os.path.join(os.path.dirname(__file__), '.env')


class Login:
    load_dotenv()
    def __init__(self, email=None, password=None):
        self.url = 'https://aitestkitchen.withgoogle.com/experiments/music-lm'
        self.email = email or os.environ.get("EMAIL")
        self.password = password or os.environ.get("PASSWORD")
        if os.environ.get("TOKEN") == "":
            self.token = self.get_token()
        elif self.token_refresh():
            self.token = self.get_token()
        else:
            self.token = os.environ.get("TOKEN")

    def save_cookies(self, driver, filename):
        pickle.dump(driver.get_cookies(), open(filename, 'wb'))
        print("Cookies saved successfully")

    def add_cookies(self, driver, filename):
        cookies = pickle.load(open(filename, 'rb'))

        # Enables network tracking so we may use Network.setCookie method
        driver.execute_cdp_cmd('Network.enable', {})

        # Iterate through pickle dict and add all the cookies
        for cookie in cookies:
            # Fix issue Chrome exports 'expiry' key but expects 'expire' on import
            if 'expiry' in cookie:
                cookie['expires'] = cookie['expiry']
                del cookie['expiry']

            # Set the actual cookie
            driver.execute_cdp_cmd('Network.setCookie', cookie)

        # Disable network tracking
        driver.execute_cdp_cmd('Network.disable', {})

        print("Cookies added successfully")
        return True

    def get_token(self):
        driver = Driver(uc=True)
        try:
            driver.get(self.url)
            if os.path.exists("cookies.pkl"):
                self.add_cookies(driver, "cookies.pkl")
                print("Added Cookies successfully.")
            try:
                WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//span[text()='Sign in with Google']"))).click()
                WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//span[text()='Sign in']"))).click()

                # driver.switch_to.window(driver.window_handles[1])
                logging.info('Logging in...')
                time.sleep(2)
                print(driver.current_url)
                if driver.current_url=="https://aitestkitchen.withgoogle.com/api/auth/signin?error=Callback":
                    print("Got error...")
                    driver.delete_all_cookies()
                    print("deleted all cookies!")
                    driver.get(self.url)
                    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//span[text()='Sign in with Google']"))).click()
                    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//span[text()='Sign in']"))).click()
                    logging.info('Retrying login...')
                WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.NAME, 'identifier'))).send_keys(f'{self.email}\n')
                WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.NAME, 'Passwd'))).send_keys(f'{self.password}\n')
                logging.info('Successfully logged in')

                # driver.switch_to.window(driver.window_handles[0])
                time.sleep(20) #20 seconds for two factor authentication
            except Exception as e:
                logging.error("An error occurred while interacting with the webpage, details: " + str(e))
                raise Exception("Unable to fetch token due to Selenium interaction error")
            time.sleep(2)
            logging.info('Getting OAuth 2.0 token')
            cookies = driver.get_cookies()
            self.save_cookies(driver, "cookies.pkl")
            #print(cookies)
            driver.get("https://aitestkitchen.withgoogle.com/api/auth/session")
            jsondata = json.loads(driver.find_element(By.XPATH, "/html/body").text)

        except Exception as e:
            logging.error("An error occurred while fetching the token, details: " + str(e))
            raise Exception("Unable to fetch token due to browser error")

        finally:
            driver.quit()

        token = jsondata["access_token"]

        dotenv.set_key(dotenv_file, "TOKEN", str(token))
        os.environ["TOKEN"] = str(token)
        dotenv.set_key(dotenv_file, "EXPIRATION_TIMESTAMP", str(datetime.datetime.now() + datetime.timedelta(minutes=59)))
        os.environ["EXPIRATION_TIMESTAMP"] = str(datetime.datetime.now() + datetime.timedelta(minutes=59))

        logging.info('OAuth 2.0 token obtained')
        return token

    def token_refresh(self):
        current_timestamp = datetime.datetime.now().replace(microsecond=0)
        expiration_timestamp = datetime.datetime.strptime(os.environ['EXPIRATION_TIMESTAMP'],  '%Y-%m-%d %H:%M:%S.%f')

        difference = current_timestamp - expiration_timestamp
        if difference >= datetime.timedelta(minutes=0):
            return True
        else:
            return False
