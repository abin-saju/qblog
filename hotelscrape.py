from selenium import webdriver
from lxml import html
import time

def startUp():
# Using chrome automation requires chromedriver to be installed. http://chromedriver.chromium.org
    driver = webdriver.Chrome('/Users/abinsaju/chromedriver')

    return driver 

def enterDestAndScrape(url, driver, dest, checkin, checkout):
    
    driver.get(url)
    
    dest_field = 'sample_dest_field'
    checkin_field = 'sample_checkin_field'
    checkout_field = 'sample_checkout_field'
    listings_id = 'sample_listings_id'

    time.sleep(2)

    try:
        driver.find_element_by_css_selector('.cta.widget-overlay-close').click()
    except:
        print("No overlay to close")
    
    time.sleep(1)
    driver.find_element_by_id(dest_field).clear()
    driver.find_element_by_id(dest_field).send_keys(dest)
    
    time.sleep(2)
    
    try:
        driver.find_element_by_css_selector('.cta.cta-link').click()
    except:
        print("Couldn't close suggestion box!")
    
    time.sleep(2)
    
    driver.find_element_by_id(checkout_field).clear()
    driver.find_element_by_id(checkout_field).send_keys(checkout)
    driver.find_element_by_id(checkin_field).clear()
    driver.find_element_by_id(checkin_field).send_keys(checkin)
    time.sleep(1)
    driver.find_element_by_css_selector('.widget-overlay-close').click()

    try:
        driver.find_element_by_css_selector('.cta.cta-strong').click()
    except:
        print("Couldn't continue to next page!")
 
    time.sleep(3)
    
    listings = driver.find_element_by_id(listings_id)
    listings_html = html.fromstring(listings.get_attribute('outerHTML'))
    hotels = listings_html.xpath('//div[@class="hotel-wrap"]')[0]
    prices = hotels.xpath('//div[@class="pricing resp-module"]')
    
    val = []
    cnt = 0
    hotel_name = []
    
    for i, price in enumerate(prices):
        if 'Fully booked' in price.text_content():
            val.append('NA')
            cnt += 1
        else:
            val.append(price.xpath('//div[@class="price"]')[i-cnt].text_content().split("£")[-1])
        
        hotel_name.append(hotels.xpath('//h3')[i].text_content())
    
    #driver.close()
    
    return [hotel_name,val]