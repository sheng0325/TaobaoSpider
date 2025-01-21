from selenium import webdriver

driver = webdriver.Chrome()
url = 'https://www.csdn.net/'
driver.get(url)
driver.maximize_window()
