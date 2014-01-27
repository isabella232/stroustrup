import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import *
import selenium.webdriver.support.ui as ui
import time



class Books_test(unittest.TestCase):

    def setUp(self):
        print('FIREFOX')
        self.driver = webdriver.Firefox()
        print('CHROME')
        #self.chrome_search()
        print('REMOTE')
        #self.driver = webdriver.Remote(command_executor='http://127.0.0.1:4444/wd/hub', desired_capabilities=webdriver.DesiredCapabilities.HTMLUNIT)



    def test_search_auth(self):
        driver = self.driver
        driver.get("http://127.0.0.1:8000/") #i suppose it's gonna be changed
        print('passed1')
        try:
            elem = driver.find_element_by_partial_link_text('Log out')
        except NoSuchElementException:
            print('already log outed')
            elem = driver.find_element_by_partial_link_text('Sign in')
            elem.send_keys(Keys.RETURN)

            print('passed2')
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
            print('passed3')
            time.sleep(2)
            self.assertIn('All books.', driver.title)

            print('passed4')
            elem = driver.find_element_by_partial_link_text('Users')
            elem.send_keys(Keys.RETURN)

            print('passed5')

            elements = driver.find_elements_by_partial_link_text('Backpack')
            for elem in elements:
                elem.click()
                time.sleep(1)
                elem.click()
                print('minus 1')
            print('passed6')

            elem = driver.find_element_by_partial_link_text('Request')
            elem.send_keys(Keys.RETURN)


            print('passed7')

            time.sleep(1)
            title = driver.find_element_by_id('id_title')
            url = driver.find_element_by_id('id_url')
            title.send_keys('TEST')
            url.send_keys('www.ozon.com')
            send = driver.find_element_by_class_name('request_button')
            send.click()

            print('passed8')
            elems = driver.find_elements_by_class_name('request_vote_button')
            for elem in elems:
                    print('heart')
                    elem.send_keys(Keys.RETURN)
            print('passed9')




        print('success!')

    def chrome_search(self):
        self.driver = webdriver.Chrome(executable_path='/Documents/custom_django_templates/chromedriver')
        self.test_search_auth()

    def fox_search(self):
        self.driver = webdriver.Firefox()
        self.test_search_auth()


    def tearDown(self):
        try:
            self.driver.close()
        except Exception as e:
            print('Closed')
if __name__ == "__main__":
    unittest.main()
