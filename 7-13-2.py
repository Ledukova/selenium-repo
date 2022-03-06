import time

import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    request.addfinalizer(wd.quit)
    return wd

def price_v_float(price):
    price = price[1:]
    #print("цена", price)
    return float(price)

def test_example(driver):
    driver.get("http://localhost/litecart/")
    wait = WebDriverWait(driver, 20)
    print()
    i=1
    while i < 4:
        tovar = driver.find_elements_by_css_selector("ul .link")
        tovar[0].click()
        element = driver.find_element_by_css_selector("span.quantity")
        # (".formatted_value")
        v_korzine_do = element.get_attribute("textContent")
        # print("до обновления", v_korzine_do)
        tovar_sale = driver.find_elements_by_name("options[Size]")
        if len(tovar_sale) > 0:
            driver.find_element_by_name("options[Size]").send_keys("S")
        driver.find_element_by_name('add_cart_product').click()  # добавляет товар в корзину
        v_korzine_now = element.get_attribute("textContent")
        while v_korzine_do == v_korzine_now:
            element = wait.until(lambda d: d.find_element_by_css_selector("span.quantity"))
            v_korzine_now = element.get_attribute("textContent")
        # print ("после обновления", v_korzine_now)
        driver.find_element_by_css_selector("[href='/litecart/']").click()  # переход на главную страницу
        i = i+1  # кол-во циклов помещения товара в корзину
    driver.find_element_by_css_selector("div#cart .link").click()  # переход в корзину
    tovarov_v_korzine = driver.find_elements_by_name('remove_cart_item')
    #print("товаров в корзине", len(tovarov_v_korzine))
    while (len(tovarov_v_korzine) > 0):
        #print("l на входе", l)
        t = driver.find_elements_by_css_selector(".footer strong")[1]
        tovarov_v_korzine[0].click()  # удаляем из корзины товар начиная с последнего
        print("t ", t.get_attribute("textContent"))
        wait.until(EC.staleness_of(t))  # ждем исчезновение элемента в таблице
        tovarov_v_korzine = driver.find_elements_by_name('remove_cart_item')
        print(len(tovarov_v_korzine), "товаров в корзине")
        if len(tovarov_v_korzine) > 0:
            wait.until(lambda d: d.find_elements_by_css_selector(".footer strong")[1])  # ждем появления элемента в таблице
    if len(tovarov_v_korzine) == 0:
        print("Товара в корзине нет")
    else:
        print(len(tovarov_v_korzine), "товаров в корзине")