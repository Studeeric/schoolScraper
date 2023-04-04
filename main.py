from csv import writer

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

url = "https://www.bever.nl/c/heren/jassen/zomerjassen.html"
page = requests.get(url)

driver = webdriver.Firefox()
driver.get(url)

driver.find_element(By.ID, 'accept-all-cookies').click()

element = driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div[2]/div/div/div/div[9]/div/div/a[3]")
totalPages = element.text

soup = BeautifulSoup(page.content, 'html.parser')
lists = [item for item in soup.find_all('div', class_="as-m-product-tile")
         if not item.find('div', class_="as-m-rating--read-only-and-empty")]

with open('heren-zomerjassen.csv', 'w', encoding="utf8", newline="") as f:
    theWriter = writer(f)
    header = ['Brand', 'Title', 'Price', 'Reviews']
    theWriter.writerow(header)

    for item in lists:
        brand = item.find('span', class_="as-m-product-tile__brand").text
        title = item.find('span', class_="as-m-product-tile__name").text
        price = item.find('div', class_="as-a-price__value--sell").text.replace('€', '')
        price.replace(',', '.')

        product_link = item.find('a', class_="as-m-product-tile__link")['href']
        driver.get('https://www.bever.nl' + product_link)
        page = requests.get(driver.current_url)
        soup = BeautifulSoup(page.content, 'html.parser')
        details = soup.find('div', class_='as-t-pdp-layout__item--header')
        reviews = details.find('div', class_='as-m-reevoo__rating').text.replace(' review', '').replace('s', '')

        driver.back()

        info = [brand, title, price, reviews]

        theWriter.writerow(info)

driver.close()
