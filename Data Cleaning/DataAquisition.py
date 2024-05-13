from logging import raiseExceptions
from re import X
from socket import timeout
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException
from selenium.webdriver.common.action_chains import ActionChains 
import time

driver = webdriver.Chrome()

options = webdriver.ChromeOptions()

options.add_experimental_option('excludeSwitches', ['enable-logging'])

#input_make = "hyundai"      #input(f'Make:{str()}').casefold()
#input_model = "veloster"        #input(f'Model:{str()}').casefold()
input_zip = "33186"      #input(f'Zip:{int(max=5)}')
input_radius = "50"       #input(f'Radius:{str(max=4)}')
input_year = 2000
input_state = "state"


driver.get(f'https://www.autotempest.com/results?localization={input_state}&zip={input_zip}&minyear={input_year}')

continue_buttons_xpath = {
    "autotempest" : "/html/body/div[1]/div[3]/section[1]/section/section[2]/section/button",
    "cars" : "/html/body/div[1]/div[3]/section[1]/section/section[3]/section/button",
    "carvana" : "/html/body/div[1]/div[3]/section[1]/section/section[4]/section/button",
    "ebay" : "/html/body/div[1]/div[3]/section[1]/section/section[5]/section/button",
    "truecar" : "/html/body/div[1]/div[3]/section[1]/section/section[6]/section/button",
    "other" : "/html/body/div[1]/div[3]/section[1]/section/section[7]/section/button"
}
    
def click_button(xpath):
    WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH, xpath)))
    button = driver.find_element(By.XPATH, xpath)
    ActionChains(driver).move_to_element(button).click().perform()
    
def car_df():
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

        mileage = section.find("span", class_="mileage")
        if mileage != None:
            mileage_car = mileage.text
            car_dictionary["mileage"].append(mileage_car)
        else:
            car_dictionary["mileage"].append(f"None")
                        
        name = section.find("span", class_="title-wrap listing-title")
        if name != None:
            name_car = name.text.strip().split(" ")
            car_dictionary["year"].append(name_car[0])
            car_dictionary["make"].append(name_car[1])
            car_dictionary["model"].append(name_car[2])
            car_dictionary["trim"].append(name_car[3:6])
            
        distance = section.find("span", class_="distance")
        if distance != None:
            distance_car = distance.text
            car_dictionary["distance from zip"].append(distance_car)
        else:
            car_dictionary["distance from zip"].append(f"delivers to {input_zip}")
                        
    car_dataframe = pd.DataFrame.from_dict(car_dictionary)
    
    
    
    print(car_dataframe)
    
    return car_dataframe

def car_data():
    while True:
        try:
            for button in continue_buttons_xpath.values():
                click_button(button)
        except (NoSuchElementException, StaleElementReferenceException, TimeoutException):
            break    

if __name__ == "__main__":
    car_data()
    car_df()
#driver.quit()

        
