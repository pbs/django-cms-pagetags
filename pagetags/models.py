from django.db import models
from django.utils.translation import ugettext_lazy as _
from cms.models.pagemodel import Page

from tagging.fields import TagField

class PageTagging(models.Model):
    page = models.ForeignKey(Page, unique=True, verbose_name=_("Page"),
        editable=False, related_name='page_tags')
    page_tags = TagField()
