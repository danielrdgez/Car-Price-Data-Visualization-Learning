import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver

path = "C:\Program Files (x86)\chromedriver.exe"

driver = webdriver.Chrome(path)

input_make = "hyundai"      #input(f'Make:{str()}').casefold()
input_model = "veloster"        #input(f'Model:{str()}').casefold()
input_zip = "33186"      #input(f'Zip:{int(max=5)}')
input_radius = "100"       #input(f'Radius:{str(max=4)}')


driver.get(f'https://www.autotempest.com/results?make={input_make}&model={input_model}&radius={input_radius}&zip={input_zip}')

html = driver.page_source

soup = BeautifulSoup(html, "html.parser")

section_card = soup.find_all("div", class_="description-wrap", limit=10)

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
    price_car = price.text
    car_dictionary["price"].append(price_car)

    mileage = section.find("span", class_="info mileage")
    if len(mileage) > 0:
        mileage_car = mileage.text
        car_dictionary["mileage"].append(mileage_car)
                
    name = section.find("a", class_="listing-link source-link")
    name_car = name.text.strip().split(" ")
    car_dictionary["year"].append(name_car[0])
    car_dictionary["make"].append(name_car[1])
    car_dictionary["model"].append(name_car[2])
    car_dictionary["trim"].append(name_car[3:])
    
    distance = section.find("span", class_="distance")
    distance_car = distance.text
    car_dictionary["distance from zip"].append(distance_car)
                
car_dataframe = pd.DataFrame.from_dict(car_dictionary)
print(car_dataframe)

        
