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
    kategoria=driver.find_elements_by_css_selector(".middle>.content .box")
    color_errors=0
    for j in range(0, len(kategoria)):
        my_list=kategoria[j].find_elements_by_css_selector(".link") # список товара box-most-popular
        print()
        tovar=list()
        while len(my_list)!=len(tovar):
            for i in range(0, len(my_list)):
                price_list=my_list[i].find_elements_by_css_selector(".price")
                if len(price_list)==0:
                    name_global=my_list[i].find_element_by_css_selector(".name").get_attribute("textContent")
                    prise_obichnay_glogal=my_list[i].find_element_by_tag_name("s").value_of_css_property("font-size") # размер цены начальной на главной странице
                    prise_akzionay_glogal=my_list[i].find_element_by_tag_name("strong").value_of_css_property("font-size") # размер цены акционной на главной странице
                    #print("размер цены обычной на гл.странице", prise_obichnay_glogal)
                    #print("размер цены акционной на гл.странице", prise_akzionay_glogal)
                    if prise_akzionay_glogal <= prise_obichnay_glogal:
                        color_errors=color_errors+1
                        print("Ошибка: размер обычной цены товара ", name_global, " на главной странице меньше или равнен размеру цены акционной")
                    if name_global not in tovar:
                        tovar.append(name_global)
                        my_list[i].find_element_by_css_selector(".name").click() # нажать на товар, для перехода на страницу товара
                        prise_obichnay_local=driver.find_element_by_css_selector(".box .regular-price").value_of_css_property("font-size") # размер цены начальная на странице товара
                        prise_akzionay_local=driver.find_element_by_css_selector(".box .campaign-price").value_of_css_property("font-size") # размен цены акционной  на странице товара
                        #print("размер цены обычной на странице товара", prise_obichnay_local)
                        #print("размер цены акционной на гл.странице товара", prise_akzionay_local)
                        if prise_akzionay_local <= prise_obichnay_local:
                            color_errors=color_errors+1
                            print("Ошибка: размер обычной цены товара ", name_global, " на странице товара меньше или равнен размеру цены акционной")
                        driver.find_element_by_css_selector(".middle a[href='/litecart/']").click()
                        kategoria=driver.find_elements_by_css_selector(".middle>.content .box")
                        my_list=kategoria[j].find_elements_by_css_selector(".link") # обновляем список товара при обновлении страницы
                else:
                    name_glogal=my_list[i].find_element_by_css_selector(".name").get_attribute("textContent")
                    if name_glogal not in tovar:
                        tovar.append(name_glogal)
    if (color_errors>0):
        raise Exception(color_errors, " ошибок размера цены товара")









