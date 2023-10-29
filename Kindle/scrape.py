import os
from selenium import webdriver
from .models import Highlight, Tag

def scrape_kindle_highlights():
    # Create a new Selenium browser instance
    driver = webdriver.Chrome()

    # URL of the page you want to scrape
    url = 'https://read.amazon.com/'

    # Navigate to the URL
    driver.get(url)

    # Check if we were redirected to the login page
    if driver.current_url == 'https://read.amazon.com/landing':
        login_amazon(driver)

    # TODO: scraping code

def login_amazon(driver):
    # Find the button and click it
    button = driver.find_element_by_xpath('/html/body/header/div/button[2]')
    button.click()

    # Find the email/phone number field and enter your email
    email_field = driver.find_element_by_name('email')
    email_field.send_keys(os.getenv('AMAZON_EMAIL'))

    # Find the password field, enter your password, and submit the form
    password_field = driver.find_element_by_name('password')
    password_field.send_keys(os.getenv('AMAZON_PASSWORD'))
    password_field.submit()  # This will submit the form