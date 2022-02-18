import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    request.addfinalizer(wd.quit)
    return wd

def test_example(driver):
    driver.get("http://localhost/litecart/admin/")
    wait = WebDriverWait(driver, 20) # seconds
    driver.find_element_by_name("username").send_keys("admin")
    driver.find_element_by_name("password").send_keys("123")
    driver.find_element_by_name("login").click()
    wait.until(EC.title_is("My Store"))
    hi=0
    my_list=driver.find_elements_by_css_selector("#app-")
    for i in range(0, len(my_list)):
        my_list=driver.find_elements_by_css_selector("#app-")
        my_list[i].click()
        h=driver.find_elements_by_css_selector("h1")
        if len(h)==0:
            print('Заголовок не найден: № пункта главного меню=', i)
            hi=hi+1
        small_list=driver.find_elements_by_css_selector("#app- li a")
        l=len(small_list)
        if l>0:
            for j in range(0, l):
                small_list=driver.find_elements_by_css_selector("#app- li a")
                small_list[j].click()
                h=driver.find_elements_by_css_selector("h1")
                if len(h)==0:
                    print('Заголовок не найден: № пункта главного меню=', i, ' № подпункта=', j)
                    hi=hi+1
    if hi>0:
        raise Exception('Не найдено заголовков на ', hi, ' страницах')










