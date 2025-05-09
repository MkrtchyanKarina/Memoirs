import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


class MySeleniumTests(StaticLiveServerTestCase):
    def setUp(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        self.browser = webdriver.Chrome(options=options)


    def test1_register(self):

        self.browser.get(self.live_server_url + '/users/register/')

        WebDriverWait(self.browser, 20).until(EC.element_to_be_clickable((By.TAG_NAME, "form"))).click()

        form = self.browser.find_element(By.TAG_NAME, "form")

        username = form.find_element(By.ID, 'id_username')
        username.send_keys('TestUser')

        email = form.find_element(By.ID, 'id_email')
        email.send_keys('TestUser1234@mail.ru')

        password1 = form.find_element(By.ID, 'id_password1')
        password1.send_keys('password1234PASSWORD')

        password2 = form.find_element(By.ID, 'id_password2')
        password2.send_keys('password1234PASSWORD')

        submit_button = form.find_element(By.TAG_NAME, "button")
        submit_button.click()


        # self.browser.get(self.live_server_url + '/users/login/')

        WebDriverWait(self.browser, 20).until(EC.element_to_be_clickable((By.TAG_NAME, "form"))).click()

        form = self.browser.find_element(By.TAG_NAME, "form")

        username = form.find_element(By.ID, 'id_username')
        username.send_keys('TestUser')

        password = form.find_element(By.ID, 'id_password')
        password.send_keys('password1234PASSWORD')

        submit_button = form.find_element(By.TAG_NAME, "button")
        submit_button.click()







        # self.browser.get(self.live_server_url + '/users/login/')
        #
        # WebDriverWait(self.browser, 20).until(EC.element_to_be_clickable((By.TAG_NAME, "form"))).click()
        #
        # form = self.browser.find_element(By.TAG_NAME, "form")
        #
        # username = form.find_element(By.ID, 'id_username')
        # username.send_keys('TestUser1234@mail.ru')
        #
        # password = form.find_element(By.ID, 'id_password')
        # password.send_keys('password1234PASSWORD')
        #
        # submit_button = form.find_element(By.TAG_NAME, "button")
        # submit_button.click()


    def tearDown(self):
        # self.browser.delete_all_cookies()
        # self.browser.execute_script("window.localStorage.clear();")
        # self.browser.execute_script("window.sessionStorage.clear();")
        self.browser.quit()

