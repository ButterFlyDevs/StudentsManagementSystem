#!/usr/bin/env python

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

"""
browser = webdriver.Firefox()
browser.get('http://www.ubuntu.com/')
"""
from selenium.webdriver.common.keys import Keys
driver = webdriver.Firefox()

"""
driver.get("http://www.python.org")
assert "Python" in driver.title
elem = driver.find_element_by_name("q")
elem.clear()
elem.send_keys("pycon")
elem.send_keys(Keys.RETURN)
assert "No results found." not in driver.page_source
"""

driver.get("http://localhost:8080/#/grupos/1")
assert "Python" in driver.title
elem = driver.find_element_by_name("q")
elem.clear()
elem.send_keys("pycon")
elem.send_keys(Keys.RETURN)
assert "No results found." not in driver.page_source


driver.close()
#driver.quit()
