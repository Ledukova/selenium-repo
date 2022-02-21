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
    driver.get("http://localhost/litecart/admin/?app=countries&doc=countries")
    wait = WebDriverWait(driver, 20) # seconds
    driver.find_element_by_name("username").send_keys("admin")
    driver.find_element_by_name("password").send_keys("123")
    driver.find_element_by_name("login").click()
    stroki=driver.find_elements_by_css_selector("tr.row")
    print()
    zone_errors=0
    strani_errors=0
    strana_st=" "
    for i in range(0, len(stroki)):
        kolonki=stroki[i].find_elements_by_css_selector("td") # колонки в строке таблицы стран
        strana_t=kolonki[4].get_attribute("textContent").lower() # название текущей страны в нижнем регистре
        if strana_st>strana_t:
            strani_errors=strani_errors+1
            print("страна не по алфавиту:", strana_t)
        k=int(kolonki[5].get_attribute("textContent"))
        if k>0:
            kolonki[6].find_element_by_css_selector("a").click()
            zones=driver.find_elements_by_css_selector("table.dataTable tr")
            zone_st=" "
            for j in range (1, len(zones)-1):
                zone_str=zones[j].find_elements_by_css_selector("td") # строка из таблицы zones
                zone_t=zone_str[2].get_attribute("textContent").lower() # название текущей зоны в нижнем регистре
                if zone_st>zone_t:
                    zone_errors=zone_errors+1
                    print(strana_t, ": зона не по алфавиту:", zone_t)
                zone_st=zone_t
            driver.find_element_by_css_selector("li#app- a[href$='countries']").click()
            stroki=driver.find_elements_by_css_selector("tr.row")
        strana_st=strana_t
    if (zone_errors>0) or (strani_errors>0):
        raise Exception(strani_errors, "стран не по алфавиту", zone_errors, "зон не по алфавиту")









