import pytest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import string

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
    driver.get("http://localhost/litecart/admin/?app=settings&doc=security&setting_group_key=store_info&page=1&key=captcha_enabled&action=edit")
    # wait = WebDriverWait(driver, 20) # seconds
    driver.find_element_by_name("username").send_keys("admin")
    driver.find_element_by_name("password").send_keys("123")
    driver.find_element_by_name("login").click()
    captcha_false=driver.find_element_by_css_selector("input[value='0']")
    if captcha_false.get_attribute("checked")!="checked": # проверка captcha false
        captcha_false.click()
        driver.find_element_by_css_selector("button[name='save']").click()
    driver.get("http://localhost/litecart/admin/?app=customers&doc=customers")
    list_email=list()
    my_list=driver.find_elements_by_css_selector("tr.row")
    for i in range(0, len(my_list)):
        my_list[i].find_element_by_css_selector(".fa-pencil").click()
        email_customers=driver.find_element_by_css_selector("[type='email']").get_attribute("textContent")
        list_email.append(email_customers)
        driver.find_element_by_name('cancel').click()
        my_list=driver.find_elements_by_css_selector("tr.row")
    email=(generate_random_string(8) + "@mail.ru")
    while email in list_email:
        email=(generate_random_string(8) + "@mail.ru")
    driver.get("http://localhost/litecart/")
    driver.find_element_by_css_selector("aside table a").click() # нажатие на регистрацию
    country=driver.find_element_by_css_selector(".select2-selection__arrow") # поле выбора страны
    country.click() # нажать на выбор страны
    driver.find_element_by_css_selector("li[id$='US']").click()
    required_pola=driver.find_elements_by_css_selector(".required ~ input") # обязательные поля
    for i in range(0, 5):
        if i != 3:
            required_pola[i].send_keys('тест')
    parol="12345"
    for j in range(7, 10):
        required_pola[j].send_keys(parol)
    login=email
    print('логин: ',login, 'пароль: ', parol)
    nomer=random.randint(10000, 99999)
    required_pola[3].send_keys(nomer)
    print(nomer)
    required_pola[6].send_keys(email)
    driver.find_element_by_name('create_account').click()
    driver.find_element_by_css_selector(".content [href$='logout']").click()
    driver.find_element_by_name("email").clear()
    driver.find_element_by_name("email").send_keys(login)
    driver.find_element_by_name("password").clear()
    driver.find_element_by_name("password").send_keys(parol)
    driver.find_element_by_name("login").click()
    driver.find_element_by_css_selector(".content [href$='logout']").click()











