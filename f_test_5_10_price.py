import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture
def driver(request):
    wd = webdriver.Firefox()
    request.addfinalizer(wd.quit)
    return wd

def test_example(driver):
    driver.get("http://localhost/litecart/")
    # wait = WebDriverWait(driver, 20) # seconds
    kategoria=driver.find_elements_by_css_selector(".middle>.content .box")
    price_errors=0
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
                price_list=my_list[i].find_elements_by_css_selector(".price")
                if len(price_list)==0:
                    name_glogal=my_list[i].find_element_by_css_selector(".name").get_attribute("textContent")
                    prise1_glogal=my_list[i].find_element_by_tag_name("s").get_attribute("textContent") # цена начальная на главной странице
                    prise2_glogal=my_list[i].find_element_by_tag_name("strong").get_attribute("textContent") # цена со скидкой на главной странице
                    if name_glogal not in tovar:
                        tovar.append(name_glogal)
                        my_list[i].find_element_by_css_selector(".name").click() # нажать на товар, для перехода на страницу товара
                        prise1_local=driver.find_element_by_css_selector(".box .regular-price").get_attribute("textContent") # цена начальная на странице товара
                        if prise1_glogal!=prise1_local:
                            price_errors=price_errors+1
                            print("Ошибка: начальная цена товара ", name_glogal, " на главной странице - ", prise1_glogal, " не совпадает с ценой на странице товара - ", prise1_local)
                        prise2_local=driver.find_element_by_css_selector(".box .campaign-price").get_attribute("textContent") # цена начальная на странице товара
                        if prise2_glogal!=prise2_local:
                            price_errors=price_errors+1
                            print("Ошибка: акционная цена товара ", name_glogal, " на главной странице - ", prise2_glogal, " не совпадает с ценой на странице товара - ", prise2_local)
                        driver.find_element_by_css_selector(".middle a[href='/litecart/']").click()
                else:
                    name_glogal=my_list[i].find_element_by_css_selector(".name").get_attribute("textContent")
                    price_global=my_list[i].find_element_by_css_selector(".price").get_attribute("textContent") # цена на главной странице
                    if name_glogal not in tovar:
                        tovar.append(name_glogal)
                        my_list[i].find_element_by_css_selector(".name").click() # нажать на товар, для перехода на страницу товара
                        price_local=driver.find_element_by_css_selector(".information .price").get_attribute("textContent") # цена на странице товара
                        if price_global!=price_local:
                            price_errors=price_errors+1
                            print("Ошибка: цена товара ", name_glogal," на главной странице ", price_global, " не совпадает с ценой на странице товара - ", price_local)
                        driver.find_element_by_css_selector(".middle a[href='/litecart/']").click()
    if (price_errors>0):
        raise Exception(price_errors, " несоответствий цены товара на главной странице и странице товара")









