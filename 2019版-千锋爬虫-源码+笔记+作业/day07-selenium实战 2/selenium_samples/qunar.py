import sys
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pyexcel


driver = webdriver.Chrome()
driver.get('https://flight.qunar.com/')

dest = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//input[@name="toCity"]'))
)
# dest = driver.find_element_by_xpath('//input[@name="toCity"]')
dest.send_keys('成都')
time.sleep(1)
dest.send_keys(Keys.RETURN)
driver.find_element_by_css_selector('button.btn_search').click()

flights = WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located(
        (By.XPATH, '//div[@class="m-airfly-lst"]/div[@class="b-airfly"]'))
)

for f in flights:
    fdata = {}
    airlines = f.find_elements_by_xpath('.//div[@class="d-air"]')
    fdata['airlines'] = [airline.text.replace('\n', '-') for airline in airlines]
    fdata['depart'] = f.find_element_by_xpath('.//div[@class="sep-lf"]').text
    fdata['duration'] = f.find_element_by_xpath('.//div[@class="sep-ct"]').text
    fdata['dest'] = f.find_element_by_xpath('.//div[@class="sep-rt"]').text
    fake_price = list(f.find_element_by_xpath('.//span[@class="prc_wp"]/em/b[1]').text)
    covers = f.find_elements_by_xpath('.//span[@class="prc_wp"]/em/b[position()>1]')
    for c in covers:
        index = int(c.value_of_css_property('left')[:-2]) // c.size['width']
        print(fdata['airlines'], fake_price, index, c.text)
        fake_price[index] = c.text
    fdata['price'] = ''.join(fake_price)
    print(fdata)

# driver.quit()














