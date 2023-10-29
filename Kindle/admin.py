from django.contrib import admin
from .models import Highlight, Tag

# registering both the Highlight and Tag models here
admin.site.register(Highlight)
admin.site.register(Tag)