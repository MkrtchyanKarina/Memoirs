from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import tempfile
import os


class MySeleniumTests(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Создаем уникальную временную папку для данных Chrome
        cls.chrome_user_dir = tempfile.mkdtemp()

        options = webdriver.ChromeOptions()
        options.add_argument(f"--user-data-dir={cls.chrome_user_dir}")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        # Для CI добавляем headless-режим
        if os.getenv('CI') == 'true':
            options.add_argument("--headless=new")

        cls.browser = webdriver.Chrome(options=options)

    def test_register_and_auth(self):
        try:
            self._test_registration()
            self._test_authorization()
        except Exception as e:
            self.browser.save_screenshot('test_failed.png')
            raise

    def _test_registration(self):
        self.browser.get(self.live_server_url + '/users/register/')

        form = WebDriverWait(self.browser, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "form"))
        )

        form.find_element(By.ID, 'id_username').send_keys('TestUser')
        form.find_element(By.ID, 'id_email').send_keys('TestUser1234@mail.ru')
        form.find_element(By.ID, 'id_password1').send_keys('password1234PASSWORD')
        form.find_element(By.ID, 'id_password2').send_keys('password1234PASSWORD')
        form.find_element(By.TAG_NAME, "button").click()

    def _test_authorization(self):
        WebDriverWait(self.browser, 20).until(
            EC.url_contains('/users/login/')
        )

        form = WebDriverWait(self.browser, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "form"))
        )

        form.find_element(By.ID, 'id_username').send_keys('TestUser')
        form.find_element(By.ID, 'id_password').send_keys('password1234PASSWORD')
        form.find_element(By.TAG_NAME, "button").click()

        # Проверка успешной авторизации
        WebDriverWait(self.browser, 20).until(
            EC.title_is("Главная страница")
        )

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        # Удаляем временную папку
        try:
            import shutil
            shutil.rmtree(cls.chrome_user_dir, ignore_errors=True)
        except Exception as e:
            print(f"Error removing Chrome user directory: {e}")
        super().tearDownClass()