from selenium import webdriver
from selenium.webdriver.common.by import By
import constants as const
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from selenium.common.exceptions import NoSuchElementException

class Dictionary(webdriver.Chrome):
    def __init__(self, driver_path=r"chromedriver.exe", teardown=True):
        self.driver_path = driver_path
        self.teardown = teardown
        os.environ['PATH'] += os.pathsep + self.driver_path
        super(Dictionary, self).__init__()
        self.implicitly_wait(5)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    def land_first_page(self):
        self.get(const.BASE_URL)

    def is_amharic(self, word):
        return any('\u1200' <= char <= '\u137F' for char in word)

    def set_the_word(self, word):
        search_box = self.find_element(By.ID, 'txtWordAmharic' if self.is_amharic(word) else 'txtWordEnglish')
        search_box.send_keys(word)

    def press_search(self, word):
        if self.is_amharic(word):
            self.find_element(By.ID, 'btnAmharicSearch').click()
        else:
            self.find_element(By.ID, 'btnEnglishSearch').click()

    def get_meaning(self , word):
        try:
            meanings_box = WebDriverWait(self, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.definitionContainerColumn"))
            )
            meanings = meanings_box.find_elements(By.CLASS_NAME, "definitionSection")
            for meaning in meanings:
                lang = meaning.find_element(By.CLASS_NAME, 'languageHeader').text
                if not self.is_amharic(word):
                    if lang == 'AMHARIC DICTIONARY':
                        m = meaning.find_element(By.CLASS_NAME , 'definitionContent')
                        return m.text
                else:
                    if lang == 'ENGLISH DICTIONARY':
                        m = meaning.find_element(By.CLASS_NAME , 'definitionContent')
                        return m.text

        except NoSuchElementException:
            return None 

    def find_word_meaning(self, word):
        self.land_first_page()
        self.set_the_word(word)
        self.press_search(word)
        return self.get_meaning(word)
