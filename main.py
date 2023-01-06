import requests
import lxml
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0",
    "Accept-Language": "en-US,en;q=0.5",
}

url_endpoint = "https://www.zillow.com/laredo-tx/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3A%22Laredo%2C%20TX%22%2C%22mapBounds%22%3A%7B%22west%22%3A-99.63274545116087%2C%22east%22%3A-99.26882333202025%2C%22south%22%3A27.44888267647564%2C%22north%22%3A27.610240653633014%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A52893%2C%22regionType%22%3A6%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A%7B%22min%22%3A200000%2C%22max%22%3A872627%7D%2C%22mp%22%3A%7B%22min%22%3A988%2C%22max%22%3A3000%7D%2C%22beds%22%3A%7B%22min%22%3A3%7D%2C%22sort%22%3A%7B%22value%22%3A%22globalrelevanceex%22%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A11%7D"

spreadsheet_url = "https://docs.google.com/forms/d/e/1FAIpQLSfk6LQ5C76BHskKeMUorMW5Xl6HuKl19C5R4U6ujrhb2VXrDg/viewform?usp=sf_link"

response = requests.get(url=url_endpoint, headers=headers)
web_page = response.text

soup = BeautifulSoup(web_page, "html.parser")
# ListItem-c11n-8-81-1__sc-10e22w8-0 srp__hpnp3q-0 enEXBq with_constellation
listings = soup.find_all("li", "ListItem-c11n-8-81-1__sc-10e22w8-0")
# li[1]/article/div/div[2]/div[2]/a/div/img
addresses = []
prices = []
links = []
for listing in listings:
    try:
        img = listing.find("img")
        link = listing.find("a")
        span = listing.find("span")
        addresses.append(img['alt'])
        links.append(link['href'])
        prices.append(span.string)
    except:
        pass


chrome_driver_path = "C:\Development\chromedriver.exe"

driver = webdriver.Chrome(executable_path=chrome_driver_path)

driver.get(spreadsheet_url)



for j in range(0, 9):
    time.sleep(5)
    try:
        submit_another_link = driver.find_element(By.CSS_SELECTOR, ".c2gzEf > a:nth-child(1)")
        submit_another_link.click()
    except:
        pass
    inputs = driver.find_elements(By.CLASS_NAME, "whsOnd")
    for i in range(0, 3):
        if i == 0:
            inputs[i].send_keys(addresses[j])
        elif i == 1:
            inputs[i].send_keys(prices[j])
        else:
            inputs[i].send_keys(links[j])
        time.sleep(2)
    submit_button = driver.find_element(By.CSS_SELECTOR, ".Y5sE8d > span:nth-child(3)")
    submit_button.click()


