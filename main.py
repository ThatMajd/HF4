from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd

link = "https://www.airbnb.com/s/Los-Angeles--CA--United-States/homes?" \
       "tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week" \
       "&price_filter_input_type=0&price_filter_num_nights=5&query=Los%20Angeles%2C%20CA&" \
       "place_id=ChIJE9on3F3HwoAR9AhGJW_fL-I&date_picker_type=flexible_dates" \
       "&source=structured_search_input_header&search_type=autocomplete_click"

LISTINGS_CSS_SELECTOR = "#site-content > div.f1ict9kd.dir.dir-ltr > div.l1adzyzg.dir.dir-ltr" \
                        " > div > div > div > div > div > div"
NEXT_BUTTON_CSS = '[aria-label="Next"]'
NAVIGATION_CSS = '[aria-label="Search results pagination"]'
PRICES_CSS = "[data-section-id=BOOK_IT_SIDEBAR]"
REVIEWS_CSS = "[data-section-id=REVIEWS_DEFAULT]"


class Scraper:
    def __init__(self, link):
        options = webdriver.ChromeOptions()
        options.add_argument("--lang=en")

        self.driver = webdriver.Chrome(executable_path="/Users/majdbishara/PycharmProjects/HF_task4/chromedriver", options=options)
        self.link = link
        self.driver.get(self.link)

        self.page_num = 1

        self.df = None

        time.sleep(10)

    def kill(self):
        self.driver.quit()

    def get_data(self, listing):
        data = {}

        self.driver.get(listing)
        time.sleep(8)

        children = self.driver.find_element(By.CSS_SELECTOR, "[data-section-id=TITLE_DEFAULT]")\
            .find_element(By.XPATH,"./*").find_elements(By.XPATH, "./*")
        title = children[0].text
        info = children[1].find_element(By.XPATH, "./*").find_elements(By.XPATH, "./*")

        has_reviews = True

        if len(info) == 3:
            ratings = info[0]
            if ratings.text != "New":
                ratings = ratings.find_elements(By.XPATH, "./*")
                rating = ratings[1].text.replace(" ·", "")
                reviews = ratings[2].text.replace(" reviews", "")
            else:
                has_reviews = False
                rating = "None"
                reviews = "None"
            location = info[2].text

        _meta = {"Title": title, "Location": location, "Rating": rating, "Number of Reviews": reviews}

        prices = \
            self.driver.find_element(By.CSS_SELECTOR, PRICES_CSS).find_element(By.XPATH, "./*").find_element(By.XPATH, "./*") \
                .find_elements(By.XPATH, "./*")[-1].find_element(By.XPATH, "./*").find_element(By.XPATH,
                                                                                               "./*").find_elements(
                By.XPATH, "./*")
        breakdown = prices[0].find_elements(By.XPATH, "./*")

        total = prices[1].text.replace("Total\n", "")

        breakdown = [a.text.replace("\nShow price breakdown", "") for a in breakdown]
        price_per_night, nights = breakdown[0].split("\n")[0].split(" x ")
        nights = nights.replace(" nights", "")
        breakdown.pop(0)
        cleaning_fee, service_fee, tax = 0, 0, 0
        for p in breakdown:
            serv, price = p.split("\n")
            price = int(price.replace("₪", ""))
            if serv == "Cleaning fee":
                cleaning_fee = price
            elif serv == "Service fee":
                service_fee = price
            elif serv == "Taxes":
                tax = price
        _prices = {"Total Price": total, "Price Per Night": price_per_night, "Nights": nights,
                   "Cleaning fee": cleaning_fee, "Service fee": service_fee, "Taxes": tax}

        if has_reviews:
            time.sleep(2)
            measures = \
            self.driver.find_element(By.CSS_SELECTOR, REVIEWS_CSS).find_element(By.XPATH, "./*").find_elements(By.XPATH,
                                                                                                          "./*")[1] \
                .find_element(By.XPATH, "./*").find_element(By.XPATH, "./*").find_elements(By.XPATH, "./*")

            _msrs = {}
            for m in measures:
                k, v = m.text.split("\n")
                _msrs[k + "_measure"] = float(v)
        else:
            _msrs = {'Cleanliness_measure': 0, 'Accuracy_measure': 0, 'Communication_measure': 0, 'Location_measure': 0,
                     'Check-in_measure': 0, 'Value_measure': 0}

        data.update(_meta)
        data.update(_prices)
        data.update(_msrs)

        if self.df is None:
            pd.DataFrame(data)
        else:
            self.df.append(data)

    def get_listings(self):
        time.sleep(6)
        listings = self.driver.find_elements(By.CSS_SELECTOR, LISTINGS_CSS_SELECTOR)
        return ["https://" + listing.find_element(By.CSS_SELECTOR, "[itemprop='url']").get_attribute("content") for listing in listings]

    def go_to_next_page(self):
        time.sleep(6)
        button = self.driver.find_element(By.CSS_SELECTOR, NAVIGATION_CSS).find_element(By.CSS_SELECTOR, NEXT_BUTTON_CSS)
        button.click()


# s = Scraper(link)
# s.go_to_next_page()
# time.sleep(3)
# s.kill()

data = {}

driver = webdriver.Chrome(executable_path="/Users/majdbishara/PycharmProjects/HF_task4/chromedriver")
driver.get("https://www.airbnb.com/rooms/681872826326991191?adults=1&children=0&infants=0&pets=0&check_in=2023-01-02&check_out=2023-01-08&source_impression_id=p3_1671393216_5cQXH3ZUHrGyT7JQ")
time.sleep(8)

children = driver.find_element(By.CSS_SELECTOR, "[data-section-id=TITLE_DEFAULT]").find_element(By.XPATH, "./*").find_elements(By.XPATH, "./*")
title = children[0].text
info = children[1].find_element(By.XPATH, "./*").find_elements(By.XPATH, "./*")

has_reviews = True

if len(info) == 3:
    ratings = info[0]
    if ratings.text != "New":
        ratings = ratings.find_elements(By.XPATH, "./*")
        rating = ratings[1].text.replace(" ·", "")
        reviews = ratings[2].text.replace(" reviews", "")
    else:
        has_reviews = False
        rating = "None"
        reviews = "None"
    location = info[2].text

_meta = {"Title": title, "Location": location, "Rating": rating, "Number of Reviews": reviews}


prices = \
    driver.find_element(By.CSS_SELECTOR, PRICES_CSS).find_element(By.XPATH, "./*").find_element(By.XPATH, "./*")\
    .find_elements(By.XPATH, "./*")[-1].find_element(By.XPATH, "./*").find_element(By.XPATH, "./*").find_elements(By.XPATH, "./*")
breakdown = prices[0].find_elements(By.XPATH, "./*")

total = prices[1].text.replace("Total\n", "")

breakdown = [a.text.replace("\nShow price breakdown", "") for a in breakdown]
price_per_night, nights = breakdown[0].split("\n")[0].split(" x ")
nights = nights.replace(" nights", "")
breakdown.pop(0)
cleaning_fee, service_fee, tax = 0, 0, 0
for p in breakdown:
    serv, price = p.split("\n")
    price = int(price.replace("₪", ""))
    if serv == "Cleaning fee":
        cleaning_fee = price
    elif serv == "Service fee":
        service_fee = price
    elif serv == "Taxes":
        tax = price
_prices = {"Total Price": total, "Price Per Night": price_per_night, "Nights": nights, "Cleaning fee": cleaning_fee, "Service fee": service_fee, "Taxes": tax}

if has_reviews:
    time.sleep(2)
    measures = driver.find_element(By.CSS_SELECTOR, REVIEWS_CSS).find_element(By.XPATH, "./*").find_elements(By.XPATH, "./*")[1]\
        .find_element(By.XPATH, "./*").find_element(By.XPATH, "./*").find_elements(By.XPATH, "./*")

    _msrs = {}
    for m in measures:
        k, v = m.text.split("\n")
        _msrs[k + "_measure"] = float(v)
else:
    _msrs = {'Cleanliness_measure': 0, 'Accuracy_measure': 0, 'Communication_measure': 0, 'Location_measure': 0, 'Check-in_measure': 0, 'Value_measure': 0}
driver.quit()

data.update(_meta)
data.update(_prices)
data.update(_msrs)
print(data)
