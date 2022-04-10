from socket import timeout
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException 
from selenium.common.exceptions import TimeoutException
import time

path = "C:\Program Files (x86)\chromedriver.exe"

driver = webdriver.Chrome(path)

input_make = "toyota"      #input(f'Make:{str()}').casefold()
input_model = "corolla"        #input(f'Model:{str()}').casefold()
input_zip = "33186"      #input(f'Zip:{int(max=5)}')
input_radius = "100"       #input(f'Radius:{str(max=4)}')


driver.get(f'https://www.autotempest.com/results?radius={input_radius}zip={input_zip}')
    
try:
    driver.set_page_load_timeout(5)   
    element = WebDriverWait(driver,10).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[3]/section[1]/section/section[8]/section/button"))
        )
    time.sleep(5)
    driver.find_element_by_xpath("/html/body/div[1]/div[3]/section[1]/section/section[8]/section/button").click()
except TimeoutException:
    pass

html = driver.page_source

soup = BeautifulSoup(html, "html.parser")

section_card = soup.find_all("div", class_="description-wrap")

car_dictionary = {
    "price" : [],
    "mileage" : [],
    "year" : [],
    "make" : [],
    "model" : [],
    "trim" : [],
    "distance from zip" : []
    }

for section in section_card:
    price = section.find("div", class_= "badge__label label--price")
    if price != None:
        price_car = price.text
        car_dictionary["price"].append(price_car)
    else:
        car_dictionary["price"].append("Inquire")

    mileage = section.find("span", class_="info mileage")
    if mileage != None:
        mileage_car = mileage.text
        car_dictionary["mileage"].append(mileage_car)
    else:
        car_dictionary["mileage"].append(f"None")
                    
    name = section.find("a", class_="listing-link source-link")
    if name != None:
        name_car = name.text.strip().split(" ")
        car_dictionary["year"].append(name_car[0])
        car_dictionary["make"].append(name_car[1])
        car_dictionary["model"].append(name_car[2])
        car_dictionary["trim"].append(name_car[3:])
        
    distance = section.find("span", class_="distance")
    if distance != None:
        distance_car = distance.text
        car_dictionary["distance from zip"].append(distance_car)
    else:
        car_dictionary["distance from zip"].append(f"delivers to {input_zip}")
                    
car_dataframe = pd.DataFrame.from_dict(car_dictionary)
print(car_dataframe)

        
