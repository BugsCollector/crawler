import sys
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pyexcel

if __name__ == '__main__':
    keyword = 'iphone'
    if len(sys.argv) > 1:
        keyword = sys.argv[1]

    option = Options()
    # option.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options=option)
    driver.get('https://www.jd.com/')
    driver.save_screenshot('1.png')
    kw = driver.find_element_by_id('key')
    kw.send_keys(keyword)
    kw.send_keys(Keys.RETURN)

    # 1. 隐式等待，如果没有立即查找到相应的元素，则最长等待10秒钟
    # driver.implicitly_wait(10)
    # 点击按销量排序
    # sort_btn = driver.find_element_by_xpath('.//div[@class="f-sort"]/a[2]')

    # 2. 傻瓜式等待，不管能否找到元素，都等待10秒
    # time.sleep(10)
    # sort_btn = driver.find_element_by_xpath('.//div[@class="f-sort"]/a[2]')

    # 3. 显式等待
    # 当查找到我们需要定位的元素时，则立即返回，否则最长等待10秒钟
    # 默认每隔500毫秒查找一次，直到找到了相应的元素或者timeout
    sort_btn = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, './/div[@class="f-sort"]/a[2]'))
    )
    sort_btn.click()
    driver.save_screenshot('2.png')
    has_next = True
    rows = []
    page_count = 0
    while has_next:
        page_count += 1
        if page_count > 3:
            break
        # driver.save_screenshot('3.png')
        # cur_page = driver.find_element_by_xpath(
        #     '//div[@id="J_bottomPage"]//a[@class="curr"]').text
        # print('---------current page is %s --------' % cur_page)
        # 先获取整个商品区域的尺寸坐标
        goods_list = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((
                By.ID, 'J_goodsList'
            ))
        )
        # goods_list = driver.find_element_by_id('J_goodsList')
        # 根据区域的大小决定往下滑动多少
        y = goods_list.rect['y'] + goods_list.rect['height'] - 500
        for i in range(0, y + (y // 20), y // 20):
            driver.execute_script('window.scrollTo(0, %s)' % i)
            time.sleep(0.5)

        # 先获取所有的商品节点
        # products = driver.find_elements_by_class_name('gl-item')
        WebDriverWait(driver, 10).until(
            EC.invisibility_of_element_located((
                By.ID, 'J_scroll_loading'
            ))
        )
        products = driver.find_elements_by_class_name('gl-item')
        for p in products:
            row = {}
            try:
                sku = p.get_attribute('data-sku')
                row['price'] = p.find_element_by_css_selector('strong.J_%s' % sku).text
                row['name'] = p.find_element_by_css_selector('div.p-name>a>em').text
                row['comments'] = p.find_element_by_id('J_comment_%s' % sku).text
                row['shop'] = p.find_element_by_css_selector('div.p-shop>span>a').text
            except Exception:
                print('ignore 1 row...')
                # sys.exit(1)
                continue
            print(row)
            rows.append(row)
        try:
            next_page = driver.find_element_by_css_selector('a.pn-next')
            if 'disabled' in next_page.get_attribute('class'):
                has_next = False
            else:
                next_page.click()
        except:
            has_next = False

    pyexcel.save_as(records=rows, dest_file_name='%s.xls' % keyword)
    # driver.quit()