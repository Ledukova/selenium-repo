import pytest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
import random
import string
import os.path

@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    request.addfinalizer(wd.quit)
    return wd

def generate_random_string(length):
    letters = string.ascii_lowercase
    rand_string = ''.join(random.choice(letters) for i in range(length))
    return rand_string

def test_example(driver):
    driver.get("http://localhost/litecart/admin/?app=catalog&doc=catalog")
    driver.find_element_by_name("username").send_keys("admin")
    driver.find_element_by_name("password").send_keys("123")
    driver.find_element_by_name("login").click()
    print()
    catalog_name = list()
    rows = driver.find_elements_by_css_selector("tr.row")  # формирование списка товара в корневом уровне
    #print("строки товаров", rows)
    if len(rows) > 0:  # формирование списка товаров
        for i in range(1, len(rows)):
            #print(i, "строка товаров", rows[i])
            if len(rows[i].find_elements_by_css_selector(".fa-folder")) == 0:  # это - товар
                elements = rows[i].find_elements_by_css_selector("td")
                name = elements[2].find_element_by_css_selector("a").get_attribute("textContent")
                #print("товар", name)
                catalog_name.append(name)
    #print("каталог товаров:", catalog_name)
    driver.find_element_by_css_selector("[href$='edit_product']").click()
    WebDriverWait(driver, 20)  # seconds
    status = driver.find_elements_by_css_selector("[type='radio']")
    status[0].click()
    text_name = generate_random_string(6)
    while text_name in catalog_name:
        text_name = generate_random_string(6)
    driver.find_element_by_name("name[en]").send_keys(text_name)
    nomer = random.randint(10000, 99999)
    driver.find_element_by_name('code').send_keys(nomer)
    # товар будет создан в корневом каталоге
    driver.find_element_by_css_selector("[value='1-3']").click()
    driver.find_element_by_name('sold_out_status_id').send_keys("sold out")
    path = os.path.abspath("img_tovar.jpg")
    driver.find_element_by_css_selector("[type='file']").send_keys(path)
    driver.find_element_by_css_selector("[name$='_from']").send_keys(Keys.HOME + "01012022")
    driver.find_element_by_css_selector("[name$='_to']").send_keys(Keys.HOME + "01012023")
    driver.find_element_by_css_selector("[href='#tab-information']").click()
    driver.find_element_by_name('manufacturer_id').send_keys("AСМЕ Corp.")
    information = driver.find_element_by_id('tab-information')
    text = information.find_elements_by_css_selector("[type='text']")
    for i in range(0, len(text)):
        text[i].send_keys('test')
    information.find_element_by_css_selector("[dir='ltr']").send_keys('test test test')
    driver.find_element_by_css_selector("[href='#tab-prices']").click()
    driver.find_element_by_name("purchase_price").send_keys(Keys.HOME + "150")
    driver.find_element_by_css_selector("[name$='_code']").click()
    driver.find_element_by_css_selector("[value='USD']").click()
    driver.find_element_by_name("prices[USD]").send_keys("10")
    driver.find_element_by_name("prices[EUR]").send_keys("10")
    driver.find_element_by_name("save").click()
    catalog_name = list()
    rows = driver.find_elements_by_css_selector("tr.row")  # формирование списка товара в корневом уровне
    if len(rows) > 0:  # формирование списка товаров
        for i in range(1, len(rows)):
            #print(i, "строка товаров", rows[i])
            if len(rows[i].find_elements_by_css_selector(".fa-folder")) == 0:  # это - товар
                elements = rows[i].find_elements_by_css_selector("td")
                name = elements[2].find_element_by_css_selector("a").get_attribute("textContent")
                #print("товар", name)
                catalog_name.append(name)
    # print("каталог товаров:", catalog_name)
    if text_name in catalog_name:
        print("Товар", text_name, "создан")
    else:
        raise Exception("Товар не создан")
