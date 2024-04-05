# This is a pratice project of BeautifulSoup & Selenium Webdriver
# The target website is cloned from Zillow.com, ensuring a static & non-changing web structrue
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
import requests

# ****************** Scrape Data ************************
housing_web = requests.get("https://appbrewery.github.io/Zillow-Clone/").text
housing_soup = BeautifulSoup(housing_web, "html.parser")

#find addresses
addresses = housing_soup.select(selector="#grid-search-results ul li .StyledPropertyCardDataWrapper address")
addresses = [address.text.strip() for address in addresses]

#find pricings
pricings = housing_soup.select(selector="#grid-search-results ul li .PropertyCardWrapper__StyledPriceLine")
pricings = [pricing.text.split("+")[0] for pricing in pricings]
for i in range(len(pricings)):
    if not "/mo" in pricings[i]:
        pricings[i] += "/mo"

#find links
links = housing_soup.select(selector="#grid-search-results ul li .StyledPropertyCardDataWrapper a")
links = [link.get("href") for link in links]

# ****************** Fill & Submit Data ************************
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver_form = webdriver.Chrome(options=chrome_options)
driver_form.get("https://forms.gle/mawmcyVBWcT7sTun7")
time.sleep(2)

for i in range(len(addresses)):
    try:
        input_address = driver_form.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
        input_price = driver_form.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
        input_link = driver_form.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
        btn_submit = driver_form.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span')

        input_address.send_keys(addresses[i])
        input_price.send_keys(pricings[i])
        input_link.send_keys(links[i])
        btn_submit.click()
        time.sleep(1)

    except NoSuchElementException: #form submitted, start a new form
        a_new_response = driver_form.find_element(By.XPATH, value='/html/body/div[1]/div[2]/div[1]/div/div[4]/a')
        a_new_response.click()
        time.sleep(1)

driver_form.quit()