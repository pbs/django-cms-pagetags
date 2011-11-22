from django.db import models
from cms.models.pagemodel import Page

from tagging.fields import TagField

class PageTagging(models.Model):
    page = models.OneToOneField(Page)
    page_tags = TagField()
