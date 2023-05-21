import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

#======================= Парсинг сайта https://elis.ru =======================

URL_TEMPLATE = "https://elis.ru"
r = requests.get(URL_TEMPLATE)

#=================== Открываем браузер по указанному адресу ==================

options = webdriver.ChromeOptions()
options.add_argument("--disable-infobars")
options.add_argument("start-maximized")
options.add_argument("--disable-extensions")

driver = webdriver.Chrome(options=options)
driver.maximize_window()
driver.get(URL_TEMPLATE + '/catalog/zhenschiny/new/')

#======================= Авторизация =======================
# Нажимаем на значок авторизации, вводим номер телефона и закрываем окно

user = driver.find_element(By.XPATH, "//a[@class='nav-ul__link ds-popup-auth-open']")
driver.execute_script("arguments[0].click();", user)
driver.find_element(By.XPATH, "//input[@name='PHONE_NUMBER']").send_keys('9999999999')
close = driver.find_element(By.XPATH, "//button[@class='popup__close ds-popup-auth-close']")
driver.execute_script("arguments[0].click();", close)
time.sleep(3)

#======================= Пагинация =======================
# Нажимаем на кнопку, пока есть возможность, с задержкой для загрузки страницы
show_more = driver.find_element(By.XPATH, "//div[@data-use='show-more-1']")
for _ in range(10):
    try:
        driver.execute_script("arguments[0].click();", show_more)
    except Exception:
        print('Пытались тыкнуть, но не до тыка')
        break
    time.sleep(3)

#======================= Парсер =======================
#Данный парсер собирает данные с названиями товаров, их ценами и характеристиками
soup = BeautifulSoup(driver.page_source, 'html.parser')
df = pd.DataFrame()

#Считываем названия всех товаров, предоставленных на странице
names = soup.find_all('a', class_='card__title')
names = [name.span.text for name in names]
df['Name'] = names

#Считываем стоимость каждого товара на странице
prices = soup.find_all('span', class_='price card__price')
prices = [price.text for price in prices]
df['Price'] = prices

#Считываем ссылки для каждого товара, чтобы перейти по ним для считывания их характеристик
pages = soup.find_all('div', class_='card col-6 col-md-4 col-xl-3')
pages = [requests.get(URL_TEMPLATE + page.a['href']) for page in pages]
descriptions = []
for page in pages:
    soup = BeautifulSoup(page.text, 'html.parser')
    description = soup.find('div', class_='item-detail__detail')
    description = description.p.text
    descriptions.append(description)
df['Descriptions'] = descriptions
df.to_csv('elis.csv', index=False)

