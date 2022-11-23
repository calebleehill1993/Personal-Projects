# Southwest could detect that I was using Selenium so I had to get around that by changing the $cdc_ variable in the
# chromedriver to $dog_ using vim.
# vim /path/to/chromedriver
# Replace all instances of cdc_ with dog_ by typing :%s/cdc_/dog_/g
# :wq!    this saves the file
# https://technoteshelp.com/javascript-can-a-website-detect-when-you-are-using-selenium-with-chromedriver/

import gspread
from oauth2client.service_account import ServiceAccountCredentials

# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
import geckodriver_autoinstaller
# Used for scrapping websites from HTML
from bs4 import BeautifulSoup
import os
import time
from datetime import date, datetime
import re
import sys
import time

start = time.time()

geckodriver_autoinstaller.install()

options = webdriver.FirefoxOptions()
options.add_argument('--headless')
options.add_argument("start-maximized")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument('--no-sandbox')
options.add_argument('--disable-application-cache')
options.add_argument('--disable-gpu')
options.add_argument("--disable-dev-shm-usage")


# options = Options()
# options.add_argument("--window-size=1920,1080")
# options.add_argument("--headless")
# options.add_argument("--disable-gpu")
# options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
#
# browser = webdriver.Chrome(options=options)


scope = ["https://spreadsheets.google.com/feeds",
         'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file",
         "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name(os.path.join(sys.path[0], "creds.json"),scope)
client = gspread.authorize(creds)

sheet = client.open("Costs of Wood Tracker").get_worksheet(1)
log = client.open("Costs of Wood Tracker").get_worksheet(4)

def convert_price(string_price):
    if '$' in string_price:
        if '.' in string_price:
            # Gets rid of the dollar sign
            return float(string_price[1:])
        else:
            # Gets rid of the dollar sign and adds the decimal
            return float(string_price[1:-2] + '.' + string_price[-2:])
    if '¢' in string_price:
        return float('.' + string_price[:-1])

def to_log(message):
    log.insert_row([str(datetime.now()), message], index=2)

to_log('Beginning to Scrape Home Depot')

count = 0

links = ['https://www.homedepot.com/p/OSB-7-16-in-Sheathing-Panel-Application-as-4-ft-x-8-ft-386081/202106230',
         'https://www.homedepot.com/p/Oriented-Strand-Board-Common-19-32-in-x-4-ft-x-8-ft-Actual-0-578-in-x-47-75-in-x-95-75-in-691459/205821485',
         'https://www.homedepot.com/p/23-32-in-x-4-ft-x-8-ft-Southern-Pine-Tongue-and-Groove-Oriented-Strand-Board-1365931/206441714',
         'https://www.homedepot.com/p/2-in-x-4-in-x-104-5-8-in-Prime-Kiln-Dried-Whitewood-Stud-832150/202053616',
         'https://www.homedepot.com/p/2-in-x-4-in-x-16-ft-Prime-Standard-and-Better-Douglas-Fir-Lumber-2167-16/206019456',
         'https://www.homedepot.com/p/2-in-x-6-in-x-104-5-8-in-Prime-Kiln-Dried-Whitewood-Stud-0207789/303338277',
         'https://www.homedepot.com/p/2-in-x-6-in-x-16-ft-2-and-Better-Prime-Doug-Fir-Lumber-2x6-16-2-btr-prime-doug-fir/300177736',
         'https://www.homedepot.com/p/2-in-x-4-in-x-8-ft-Prime-Whitewood-Stud-058449/312528776',
         'https://www.homedepot.com/p/2-in-x-6-in-x-8-ft-2-and-Better-Prime-Douglas-Fir-Lumber-2023-8/206019463',
         'https://www.homedepot.com/p/2-in-x-4-in-x-16-ft-2-Ground-Contact-Hem-Fir-Pressure-Treated-Lumber-549000102041600/206931756',
         'https://www.homedepot.com/p/2-in-x-6-in-x-16-ft-2-Ground-Contact-Hem-Fir-Pressure-Treated-Lumber-549000102061600/206931770',
         'https://www.homedepot.com/p/2-in-x-4-in-x-92-5-8-in-Prime-Whitewood-Stud-569062/202091224',
         'https://www.homedepot.com/p/2-in-x-6-in-x-92-5-8-in-Prime-Kiln-Dried-Whitewood-Stud-845728/202091228']

# Home Depot
for link in links:
    tries = 1

    while tries < 4:
        if tries > 1:
            print('Failed. Starting try ' + str(tries))
            to_log('Failed. Starting try ' + str(tries))
        try:
            count += 1
            to_log('Starting Firefox Web Driver ' + str(count) + '/' + str(len(links)))
            browser = webdriver.Firefox(options=options)

            to_log('Getting starter page')
            browser.get(
                'https://www.homedepot.com/p/OSB-7-16-in-Sheathing-Panel-Application-as-4-ft-x-8-ft-386081/202106230')
            time.sleep(5)
            assert 'Home Depot' in browser.title

            to_log('Selecting Store')

            browser.find_element(By.XPATH, '//div[@class="MyStoreWrapper"]').click()

            time.sleep(2)
            browser.find_element(By.XPATH, "//span[text()='Find Other Stores']").click()
            time.sleep(2)
            elem = browser.find_element(By.ID, "myStore-formInput")
            elem.send_keys('83815')
            elem.send_keys(Keys.RETURN)
            time.sleep(2)
            try:
                browser.find_element(By.XPATH, '//button[@data-storezip="83815"]').click()
                time.sleep(5)
            except:
                print("That's the already selected store.")
                to_log("That's the already selected store.")

            browser.get(link)
            time.sleep(5 * tries)

            print(browser.title)

            html_path = os.path.join(os.path.dirname(__file__), 'home_depot.html')

            with open(html_path, "w") as f:
                f.write(browser.page_source)

            with open(html_path, "r") as f:
                soup = BeautifulSoup(f, 'html.parser')
                try:
                    price_section = soup.find("div", {"id": "unit-price"})
                    print(price_section.text)
                    to_log(price_section.text)
                except:
                    try:
                        price_section = soup.find("div", {"id": "standard-price"})
                        print(price_section.text)
                        to_log(price_section.text)
                    except:
                        print("Couldn't find price.")
                        to_log("Couldn't find price.")
                        tries += 1
                        continue

                prices_re = re.findall('(\$[0-9.¢]+|[0-9.¢]+¢)', price_section.text)
                bulk_re = re.findall('Buy (\d+) or more ([$\d.¢]+)', price_section.text)
                limit_re = re.findall('Limit (\d+) per order', price_section.text)

                price = 0.0
                has_bulk_price = False
                bulk_count = 0
                bulk_price = 0.0
                has_limit = False
                limit = 0

                if len(prices_re) > 0:
                    price = convert_price(prices_re[0])
                if len(bulk_re) > 0:
                    has_bulk_price = True
                    bulk_count = int(bulk_re[0][0])
                    bulk_price = convert_price(bulk_re[0][1])
                if len(limit_re) > 0:
                    has_limit = True
                    limit = int(limit_re[0])

                if price > 0:
                    # Add row to the Google Sheet Database
                    to_log('Inserting - ' + browser.title)
                    sheet.insert_row([browser.title, str(date.today()), price, has_bulk_price, bulk_count, bulk_price,
                                      has_limit, limit], index=2)
                    tries = 4
                else:
                    tries += 1

        except Exception as e:
            to_log(str(e))

        finally:
            to_log('Quiting Browser')
            browser.quit()

to_log('Finished Process - ' + str((time.time() - start) / 60.0) + ' minutes')
