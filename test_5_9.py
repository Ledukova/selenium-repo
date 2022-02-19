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
    driver.get("http://localhost/litecart/admin/?app=geo_zones&doc=geo_zones")
    wait = WebDriverWait(driver, 20) # seconds
    driver.find_element_by_name("username").send_keys("admin")
    driver.find_element_by_name("password").send_keys("123")
    driver.find_element_by_name("login").click()
    stroki=driver.find_elements_by_css_selector("tr.row")
    print()
    zone_errors=0
    for i in range(0, len(stroki)):
        stroki=driver.find_elements_by_css_selector("tr.row")
        stroki[i].find_element_by_css_selector("a[title='Edit']").click() # нажимать кнопку редактировать
        zones=driver.find_elements_by_css_selector("table.dataTable tr")
        zone_st=" "
        for j in range (1, len(zones)-1):
            zone_str=zones[j].find_elements_by_css_selector("td") # строка из таблицы zones
            zone_t=zone_str[2].find_element_by_css_selector("option[selected='selected']").get_attribute("textContent").lower() # название текущей зоны в нижнем регистре
            strana_t=zone_str[1].find_element_by_css_selector("option[selected='selected']").get_attribute("textContent").lower()
            if zone_st>zone_t:
                zone_errors=zone_errors+1
                print(strana_t, ": зона не по алфавиту:", zone_t)
            zone_st=zone_t
        driver.find_element_by_css_selector("li#app- a[href$='geo_zones']").click()
    if (zone_errors>0):
        raise Exception(zone_errors, "зон не по алфавиту")









