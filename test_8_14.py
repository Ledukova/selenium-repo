import pytest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    request.addfinalizer(wd.quit)
    return wd

def test_example(driver):
    driver.get("http://localhost/litecart/admin/?app=countries&doc=countries")
    driver.find_element_by_name("username").send_keys("admin")
    driver.find_element_by_name("password").send_keys("123")
    driver.find_element_by_name("login").click()
    wait = WebDriverWait(driver, 30)
    driver.find_element_by_css_selector(".button").click()
    links = driver.find_elements_by_css_selector(".fa-external-link")  # все ссылки на  Add New Country
    # print()
    window_home = driver.current_window_handle  # идентификатор страницы Add New Country
    window = driver.window_handles  # исходный массив окон из одного окна страницы Add New Country
    # print(window_home)
    for i in range(0, len(links)):
        links[i].click()  # открытие i-ой ссылки
        windows = driver.window_handles  # находим идентификаторы всех открытыех окон
        #print("открытые окна", windows)
        if len(window) == len(windows):  # ждем открытия окна
            wait.until(lambda d: len(window) < len(driver.window_handles))
            windows = driver.window_handles
        for i in range(0, len(windows)):  # определить какое окно открылось
            if window_home != windows[i]:
                new_window = windows[i]
                #print(new_window)
        driver.switch_to.window(new_window)  # переходим в новое окно
        driver.close() #закрываем новое окно
        driver.switch_to.window(window_home)  # переходим в окно со страницей Add New Country
        links = driver.find_elements_by_css_selector(".fa-external-link")  # обновляем список ссылок
    driver.quit()

