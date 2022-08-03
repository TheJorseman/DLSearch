from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
# Waiters
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# Others
from os import path
import platform

class FirefoxDriver(object):
    def __init__(self, web_driver_path="DLSEARCH/tools/webdriver", sleep_time_s=0.7):
        super(FirefoxDriver,self).__init__()
        self.web_driver_path = web_driver_path
        self.sleep_time_s = sleep_time_s
        self.set_driver()
        
    def set_driver(self):
        #webdriver_filename=""
        if platform.system() == "Windows":
            firefox_webdriver_filename="geckodriver.exe"
        elif platform.system() == "Linux":
            firefox_webdriver_filename="geckodriver"
        #firefox_webdriver_path = path.join("scrapping","tools","webdriver",firefox_webdriver_filename)
        firefox_webdriver_path=path.join(self.web_driver_path,firefox_webdriver_filename)
        self.driver = webdriver.Firefox(executable_path=firefox_webdriver_path)
        self.driver.implicitly_wait(self.sleep_time_s)
    
    def sleep_time(self):
        sleep(self.sleep_time_s)

    def open_url(self, url, sleep_time_s=0.7):
        self.driver.get(url)
        sleep(sleep_time_s)

    def set_credentials(self, username, password):
        self.set_username(username)
        self.set_password(password)
        self.sleep_time()

    def set_username(self, username):
        element_username = self.search_input_username()
        element_username.send_keys(username)

    def set_password(self, password):
        element_pass = self.search_input_password()
        element_pass.send_keys(password)
        element_pass.submit()

    def search_input_password(self):
        key = "password"
        element = self.search_by_id(key)
        if not element:
            element = self.search_by_name(key)
        if not element:
            raise Warning("Input Not Found")
        return element

    def search_input_username(self):
        key = "username"
        element = self.search_by_id(key)
        if not element:
            element = self.search_by_name(key)
        if not element:
            raise Warning("Input Not Found")
        return element

    def search_by_class(self, _class):
        try:
            inputElement = self.driver.find_element_by_class_name(_class)
        except:
            inputElement = False
        return inputElement

    def search_by_id(self, _id):
        try:
            inputElement = self.driver.find_elements_by_id(_id)
        except:
            inputElement = False
        return inputElement

    def search_by_name(self, name):
        try:
            inputElement = self.driver.find_element_by_name(name)
        except:
            inputElement = False
        return inputElement


    def close(self):
        self.driver.close()