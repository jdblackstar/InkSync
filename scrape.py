import datetime
import os
import time

from selenium import webdriver

from app import db
from models import Highlight, ScrapeInfo, Tag


def scrape_kindle_highlights():
    driver = webdriver.Chrome()
    scrape_info = ScrapeInfo.query.order_by(ScrapeInfo.id.desc()).first()
    url = "https://read.amazon.com/notebook"
    driver.get(url)
    if driver.current_url == "https://read.amazon.com/landing":
        login_amazon(driver)
    # TODO: scraping code
    # Find all book elements by their common attribute
    # books seem to always start with 'B0'
    books = driver.find_elements_by_xpath('//div[starts-with(@id, "B0")]')
    for book in books:
        book.click()
        time.sleep(2)
        last_accessed = book.find_element_by_xpath(
            '//*[@id="annotation-scroller"]/div/div[1]/div[2]/span'
        ).get_attribute("innerHTML")
        last_accessed_date = datetime.datetime.strptime(
            last_accessed, "%Y-%m-%d %H:%M:%S"
        )
        if (
            scrape_info
            and scrape_info.last_scraped
            and last_accessed_date < scrape_info.last_scraped
        ):
            print("All highlights are up to date.")
            break
        highlights = book.find_elements_by_class_name("highlight")
        for highlight in highlights:
            book_title = (
                highlight.book_title
            )  # TODO: Replace 'highlight.book_title' with the actual code to get the book title
            author = (
                highlight.author
            )  # TODO: Replace 'highlight.author' with the actual code to get the author
            highlight_text = (
                highlight.text
            )  # TODO: Replace 'highlight.text' with the actual code to get the highlight text
            location = (
                highlight.location
            )  # TODO: Replace 'highlight.location' with the actual code to get the location
            new_highlight = Highlight(
                book_title=book_title,
                author=author,
                highlight_text=highlight_text,
                location=location,
                tags=[],  # TODO: Replace with actual tags
                last_accessed=last_accessed,
            )
        driver.back()
        time.sleep(2)
    if scrape_info:
        scrape_info.last_scraped = datetime.datetime.now()
    else:
        scrape_info = ScrapeInfo(last_scraped=datetime.datetime.now())
        db.session.add(scrape_info)
    db.session.commit()


def login_amazon(driver):
    button = driver.find_element_by_xpath("/html/body/header/div/button[2]")
    button.click()
    email_field = driver.find_element_by_name("email")
    email_field.send_keys(os.getenv("AMAZON_EMAIL"))
    password_field = driver.find_element_by_name("password")
    password_field.send_keys(os.getenv("AMAZON_PASSWORD"))
    password_field.submit()  # This will submit the form
