from selenium import webdriver
from lxml import html
import time

def startUp():
    # Using chrome automation requires chromedriver to be installed. http://chromedriver.chromium.org
    path_to_chromedriver = ''
    driver = webdriver.Chrome(path_to_chromedriver)

    return driver 

def enterDestAndScrape(url, driver, dest, checkin, checkout):
    
    driver.get(url)

    # Sample field id's  
    dest_field = 'sample_dest_field'
    checkin_field = 'sample_checkin_field'
    checkout_field = 'sample_checkout_field'
    listings_id = 'sample_listings_id'

    time.sleep(2)

    # Website I was looking at had popups, which affected the script, so trying to close this if it exists.
    try:
        driver.find_element_by_css_selector('.cta.widget-overlay-close').click()
    except:
        print("No overlay to close")
    
    time.sleep(1)
    
    # Enter destination info
    driver.find_element_by_id(dest_field).clear()
    driver.find_element_by_id(dest_field).send_keys(dest)
    
    time.sleep(2)
    
    # Website creates a suggestion box for the entered destination, close this as I already know its fine
    try:
        driver.find_element_by_css_selector('.cta.cta-link').click()
    except:
        print("Couldn't close suggestion box!")
    
    time.sleep(2)
    
    # Enter checkin and checkout dates
    driver.find_element_by_id(checkout_field).clear()
    driver.find_element_by_id(checkout_field).send_keys(checkout)
    driver.find_element_by_id(checkin_field).clear()
    driver.find_element_by_id(checkin_field).send_keys(checkin)
    time.sleep(1)
    # Close checkin checkout suggestion box
    driver.find_element_by_css_selector('.widget-overlay-close').click()

    # Run the search
    try:
        driver.find_element_by_css_selector('.cta.cta-strong').click()
    except:
        print("Couldn't continue to next page!")
 
    time.sleep(3)
    
    # Extract hotel listings
    listings = driver.find_element_by_id(listings_id)
    listings_html = html.fromstring(listings.get_attribute('outerHTML'))
    hotels = listings_html.xpath('//div[@class="hotel-wrap"]')[0]
    prices = hotels.xpath('//div[@class="pricing resp-module"]')
    
    val = []
    cnt = 0
    hotel_name = []
    
    # Handle cases where price is not displayed when hotel is booked out
    for i, price in enumerate(prices):
        if 'Fully booked' in price.text_content():
            val.append('NA')
            cnt += 1
        else:
            val.append(price.xpath('//div[@class="price"]')[i-cnt].text_content().split("£")[-1])
        
        hotel_name.append(hotels.xpath('//h3')[i].text_content())
    
    # Optionally close the driver
    # driver.close()
    
    # Pass back data as a list
    return [hotel_name,val]
