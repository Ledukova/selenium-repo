import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture
def driver(request):
    wd = webdriver.Edge()
    request.addfinalizer(wd.quit)
    return wd

def test_example(driver):
    driver.get("http://localhost/litecart/")
    # wait = WebDriverWait(driver, 20) # seconds
    kategoria=driver.find_elements_by_css_selector(".middle>.content .box")
    name_errors=0
    for j in range(0, len(kategoria)):
        kategoria=driver.find_elements_by_css_selector(".middle>.content .box")
        my_list=kategoria[j].find_elements_by_css_selector(".link") # список товара box-most-popular
        print()
        tovar=list()
        while len(my_list)!=len(tovar):
            kategoria=driver.find_elements_by_css_selector(".middle>.content .box")
            my_list=kategoria[j].find_elements_by_css_selector(".link") # обновляем список товара при обновлении страницы
            for i in range(0, len(my_list)):
                kategoria=driver.find_elements_by_css_selector(".middle>.content .box")
                my_list=kategoria[j].find_elements_by_css_selector(".link") # обновляем список товара при обновлении страницы
                name_glogal=my_list[i].find_element_by_css_selector(".name").get_attribute("textContent") # название товара на главной странице
                if name_glogal not in tovar:
                    tovar.append(name_glogal)
                    my_list[i].find_element_by_css_selector(".name").click() # нажать на товар, для перехода на страницу товара
                    name_local=driver.find_element_by_tag_name("h1").get_attribute("textContent") # название товара на странице товара
                    if name_glogal!=name_local:
                        name_errors=name_errors+1
                        print("Ошибка: название товара на главной странице - ", name_glogal, " название товара на странице товара - ", name_local)
                    driver.find_element_by_css_selector(".middle a[href='/litecart/']").click()

    if (name_errors>0):
        raise Exception(name_errors, " несоответствий наименований товара на главной странице и странице товара")









