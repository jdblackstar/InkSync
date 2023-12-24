from datetime import datetime


class Tag:
    def __init__(self, color):
        self.color = color


class Highlight:
    def __init__(
        self, book_title, author, highlight_text, location, tags, last_accessed
    ):
        self.book_title = book_title
        self.author = author
        self.highlight_text = highlight_text
        self.location = location
        self.tags = tags
        self.last_accessed = last_accessed


class ScrapeInfo:
    def __init__(self, last_scraped):
        self.last_scraped = last_scraped
