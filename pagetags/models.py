# -*- coding: utf-8 -*-
"""
Models for Pagetags Django CMS plugin.
"""
from django.db import models
from django.utils.translation import ugettext_lazy as _
from cms.models.pagemodel import Page

from tagging.fields import TagField


class PageTagging(models.Model):
    """Model for `django-tagging` integration with Django CMS pages."""

    page = models.OneToOneField(Page, verbose_name=_('Page'))
    page_tags = TagField(verbose_name=_('Tags'),
        help_text=_("Please provide a comma-separated list of tags."))

    class Meta:
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')

    def __unicode__(self):
        return u'Tags on {0}'.format(self.page)

