import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import *
import selenium.webdriver.support.ui as ui
import time

class Authentefication(unittest.TestCase):

    def setUp(self):
        #self.driver = webdriver.Remote(command_executor='http://127.0.0.1:4444/wd/hub', desired_capabilities=webdriver.DesiredCapabilities.HTMLUNIT)
        self.driver = webdriver.Firefox()

    def test_search_in_python_org(self):
        driver = self.driver
        driver.get("http://127.0.0.1:8000/") #i suppose it's gonna be changed
        #self.assertIn("All books.", driver.title)
        wait = ui.WebDriverWait(driver,100)
        print('passed1')
        try:
            elem = driver.find_element_by_partial_link_text('Log out')
            elem.send_keys(Keys.RETURN)
            elem = driver.find_element_by_partial_link_text('Main page')
            elem.send_keys(Keys.RETURN)
        except NoSuchElementException:
            print('already log outed')
        print('passed2')
        elem = driver.find_element_by_partial_link_text('Sign in')
        elem.send_keys(Keys.RETURN)
        print('passed3')

        time.sleep(1)
        try:
            elems = driver.find_elements_by_class_name("button")
            print('found')
            for elem in elems:
                elem.send_keys(Keys.ENTER)
        except NoSuchElementException or StaleElementReferenceException as ex:
            print(ex)
            driver.back()


        print('passed4')
        time.sleep(1)


        elem = driver.find_element_by_id('id_username')
        print('found')
        elem.send_keys('')
        elem.send_keys(Keys.RETURN)

        print('should be error')
        #wait.until(True, '')
        try:
            errorbox = driver.find_elements_by_tag_name('li')
        except NoSuchElementException as ex:
            print(ex)

        print('passed5')

        elem = driver.find_element_by_partial_link_text('Fall')
        elem.send_keys(Keys.RETURN)

        print('passed6')
        time.sleep(1)
        elem = driver.find_element_by_partial_link_text('Sign in')
        elem.send_keys(Keys.RETURN)

        print('passed7')
        time.sleep(1)
        login = driver.find_element_by_id('id_username')
        password = driver.find_element_by_id('id_password')
        login.send_keys('admin')
        password.send_keys('incorrect')
        time.sleep(1)
        elems = driver.find_elements_by_tag_name('button')
        print(elems)
        if elems:
            elems[0].send_keys(Keys.RETURN)

        print('found')


        print('passed8')
        time.sleep(2)

        self.assertIn('All books.', driver.title)

        print('success!')




    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()