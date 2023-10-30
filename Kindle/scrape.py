import datetime
import os
import time

from selenium import webdriver

from .models import Highlight, ScrapeInfo, Tag


def scrape_kindle_highlights():
    # Create a new Selenium browser instance
    driver = webdriver.Chrome()
    # Retrieve the last_scraped value
    scrape_info = ScrapeInfo.objects.first()
    if scrape_info:
        last_scraped = scrape_info.last_scraped
    else:
        last_scraped = None

    # URL of the page you want to scrape
    url = "https://read.amazon.com/notebook"

    # Navigate to the URL
    driver.get(url)

    # Check if we were redirected to the login page
    if driver.current_url == "https://read.amazon.com/landing":
        login_amazon(driver)

    # # click on the Notes & Highlights section
    # highlights_page = driver.find_elements_by_xpath('//*[@id="notes_button"]')
    # highlights_page.click()

    # TODO: scraping code
    # Find all book elements by their common attribute
    # books seem to always start with 'B0'
    books = driver.find_elements_by_xpath('//div[starts-with(@id, "B0")]')

    # Loop over the books
    for book in books:
        # Click on the book
        book.click()

        # Wait for the page to load
        time.sleep(2)  # Adjust this delay as needed

        # if the Last Accessed date is earlier than the last time the script run, return because every book after this is earlier in time
        last_accessed = book.find_element_by_xpath(
            '//*[@id="annotation-scroller"]/div/div[1]/div[2]/span'
        ).get_attribute("innerHTML")
        last_accessed_date = datetime.strptime(last_accessed, "%Y-%m-%d %H:%M:%S")
        if last_accessed_date < last_scraped:
            print("All highlights are up to date.")
            break

        # Now you can scrape the highlights for this book
        highlights = book.find_elements_by_class_name(
            "highlight"
        )  # Replace 'highlight' with the actual class name

        # Loop over the highlights
        for highlight in highlights:
            # Extract the highlight data
            book_title = (
                highlight.book_title
            )  # Replace 'highlight.book_title' with the actual code to get the book title
            author = (
                highlight.author
            )  # Replace 'highlight.author' with the actual code to get the author
            highlight_text = (
                highlight.text
            )  # Replace 'highlight.text' with the actual code to get the highlight text
            location = (
                highlight.location
            )  # Replace 'highlight.location' with the actual code to get the location

            # Check if a highlight with the same book_title, author, highlight_text, and location already exists
            if not Highlight.objects.filter(
                book_title=book_title,
                author=author,
                highlight_text=highlight_text,
                location=location,
            ).exists():
                # If not, create a new Highlight instance
                Highlight.objects.create(
                    book_title=book_title,
                    author=author,
                    highlight_text=highlight_text,
                    location=location,
                    last_accessed=last_accessed,
                )

        # Go back to the book list
        driver.back()

        # Wait for the page to load
        time.sleep(2)  # Adjust this delay as needed

    if scrape_info:
        scrape_info.last_scraped = datetime.now()
        scrape_info.save()
    else:
        ScrapeInfo.objects.create(last_scraped=datetime.now())


def login_amazon(driver):
    # Find the button and click it
    button = driver.find_element_by_xpath("/html/body/header/div/button[2]")
    button.click()

    # Find the email/phone number field and enter your email
    email_field = driver.find_element_by_name("email")
    email_field.send_keys(os.getenv("AMAZON_EMAIL"))

    # Find the password field, enter your password, and submit the form
    password_field = driver.find_element_by_name("password")
    password_field.send_keys(os.getenv("AMAZON_PASSWORD"))
    password_field.submit()  # This will submit the form
