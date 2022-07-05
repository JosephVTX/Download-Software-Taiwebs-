import time
import unittest

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from functions import validate_url
from functions import validate_url_taiwebs
from functions import wait_download_file


class BotDownload(unittest.TestCase):

    def setUp(self):

        self.path_download = "E:\\Documentos\\PycharmProjects\\softwareDownload\\Download\\"
        chrome_prefs = {'profile.default_content_setting_values': {'cookies': 2, 'images': 2,
                                                                   "download.default_directory": self.path_download,
                                                                   'plugins': 2, 'popups': 2, 'geolocation': 2,
                                                                   'notifications': 2, 'auto_select_certificate': 2,
                                                                   'fullscreen': 2,
                                                                   'mouselock': 2, 'mixed_script': 2, 'media_stream': 2,
                                                                   'media_stream_mic': 2, 'media_stream_camera': 2,
                                                                   'protocol_handlers': 2,
                                                                   'ppapi_broker': 2, 'automatic_downloads': 2,
                                                                   'midi_sysex': 2,
                                                                   'push_messaging': 2, 'ssl_cert_decisions': 2,
                                                                   'metro_switch_to_desktop': 2,
                                                                   'protected_media_identifier': 2, 'app_banner': 2,
                                                                   'site_engagement': 2,
                                                                   'durable_storage': 2}}
        options = Options()
        options.add_extension("Extension/uBlock.crx")  # Extension para bloquear anuncios.
        options.add_argument("--start-maximized")  # Maximiza el  navegador
        options.add_experimental_option("prefs", chrome_prefs)
        options.add_argument('--remote-debugging-port=9222')
        self.driver = webdriver.Chrome(options=options, service=ChromeService(ChromeDriverManager().install()))
        self.driver.minimize_window()
        params = {'behavior': 'allow', 'downloadPath': self.path_download}
        self.driver.execute_cdp_cmd('Page.setDownloadBehavior', params)

    def test_download(self):

        while True:

            url = input("Ingresa la URL del Software: ")
            if validate_url(url) and validate_url_taiwebs(url):
                break
            print("UPS! Al parecer es una URL invalida.")

        driver = self.driver
        wait = WebDriverWait(driver, 20)
        driver.get(url)

        title_software = wait.until(ec.visibility_of_element_located((By.XPATH, "//h1[@class='text-big']"))).text
        btn_download = wait.until(ec.visibility_of_element_located((By.XPATH, "//*[self::a[@class='box-down-bottom'] "
                                                                              "or self::button[@class='btn-block "
                                                                              "block_download']]")))
        btn_download.click()

        if len(driver.window_handles) == 2:
            driver.switch_to.window(driver.window_handles[1])

        all_btn_download = wait.until(ec.presence_of_all_elements_located((By.XPATH, "//div[contains(@id,'download')]"
                                                                                     "//ul/a")))
        for btn_download_2 in all_btn_download:

            if btn_download_2.is_displayed():
                btn_download_2.click()
                break

        print(f"DESCARGANDO {title_software}")
        wait_download_file(self.path_download)
        print("DESCARGA COMPLETADA!")

    def tearDown(self):
        time.sleep(2)
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
