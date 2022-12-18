from selenium import webdriver
from selenium.webdriver.common.by import By
import time

link = "https://www.airbnb.com/s/Los-Angeles--CA--United-States/homes?" \
       "tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week" \
       "&price_filter_input_type=0&price_filter_num_nights=5&query=Los%20Angeles%2C%20CA&" \
       "place_id=ChIJE9on3F3HwoAR9AhGJW_fL-I&date_picker_type=flexible_dates" \
       "&source=structured_search_input_header&search_type=autocomplete_click"

LISTINGS_CSS_SELECTOR = "#site-content > div.f1ict9kd.dir.dir-ltr > div.l1adzyzg.dir.dir-ltr" \
                        " > div > div > div > div > div > div"
NEXT_BUTTON_CSS = '[aria-label="Next"]'
NAVIGATION_CSS = '[aria-label="Search results pagination"]'


class Scraper:
    def __init__(self, link):
        options = webdriver.ChromeOptions()
        options.add_argument("--lang=en")

        self.driver = webdriver.Chrome(executable_path="/Users/majdbishara/PycharmProjects/HF_task4/chromedriver", options=options)
        self.link = link
        self.driver.get(self.link)

        self.page_num = 1
        time.sleep(10)

    def kill(self):
        self.driver.quit()

    def get_listings(self):
        time.sleep(6)
        return self.driver.find_elements(By.CSS_SELECTOR, LISTINGS_CSS_SELECTOR)

    def go_to_next_page(self):
        time.sleep(6)
        button = self.driver.find_element(By.CSS_SELECTOR, NAVIGATION_CSS).find_element(By.CSS_SELECTOR, NEXT_BUTTON_CSS)
        button.click()


s = Scraper(link)

for elem in s.get_listings():
    print(elem.text)
    print("--------")
    print()
    print("--------")
    break

s.go_to_next_page()

for elem in s.get_listings():
    print(elem.text)
    print("--------")
    print()
    print("--------")
    break

s.go_to_next_page()
time.sleep(4)

s.kill()


