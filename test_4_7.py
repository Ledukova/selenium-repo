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
    driver.get("http://localhost/litecart/")
    wait = WebDriverWait(driver, 20) # seconds
    my_list=driver.find_elements_by_css_selector("[class^='product']")
    hi=0 # кол-во без стикера
    hj=0 # кол-во более одного стикера
    for i in range(0, len(my_list)):
        sticker_list=my_list[i].find_elements_by_css_selector("[class^='sticker']")
        if len(sticker_list)==0:
            print('Продукт ', i, ' без стикер')
            hi=hi+1
        if len(sticker_list)>1:
            print('У продукта ', i, ' более одного стикера')
            hj=hj+1
    if (hi>0) or (hj>0):
        raise Exception(hi, ' продуктов без стикеров. У ', hj, ' продуктов более одного стикера')










