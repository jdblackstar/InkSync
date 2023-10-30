from datetime import datetime

from django.db import models


class Tag(models.Model):
    color = models.CharField(max_length=50)


class Highlight(models.Model):
    book_title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    highlight_text = models.TextField()
    location = models.IntegerField()
    tags = models.ManyToManyField(Tag)
    last_accessed = models.DateTimeField(default=datetime.now)


class ScrapeInfo(models.Model):
    last_scraped = models.DateTimeField()
