from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import csv 

search_query = input("What are you looking for on Lazada?\n").replace(" ", "+")
pages_length = int(input("Up to how many pages do you want to scour?\n"))

URL_PREFIX = "https://www.lazada.com.ph/catalog/?q="
URL_SUFFIX = "&_keyori=ss&from=input&spm=a2o4l.home.search.go.239e7e66ukVGRE"
URL = f"{URL_PREFIX}{search_query}{URL_SUFFIX}"

chromeDriverService=Service("/usr/local/bin/chromedriver")
driver = webdriver.Chrome(service=chromeDriverService)
driver.get(URL)


headers = ['description', 'price']
data = []

number = 0

for i in range(pages_length): 
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#root")))
    soup = BeautifulSoup(driver.page_source, "html.parser")

    for item in soup.find_all("div", class_="buTCk"):
        product = {}

        item_description = item.find(title=True, age=True).text
        product['description'] = item_description
    
        item_price = item.find('span', class_='ooOxS').text
        product['price'] =  item_price

        data.append(product)

    number = number + 1
    if number == pages_length:
        continue

    driver.find_element(By.CSS_SELECTOR, ".ant-pagination-next").click()
    
    next_items_loading_buffer = 5
    time.sleep(next_items_loading_buffer)

with open("data.csv", "w") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames = headers) 
    writer.writeheader() 
    writer.writerows(data) 

driver.close()
driver.quit() 
print("Done! Please check for data.csv in your directory!")