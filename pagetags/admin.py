# -*- coding: utf-8 -*-
"""
Admin interface for Pagetags Django CMS plugin.
"""
from django.contrib import admin
from django.contrib.admin.sites import NotRegistered
from cms.models.pagemodel import Page

from tagging.fields import TagField
from pagetags import models
from pagetags.fields import AutocompleteWidget


def _get_registered_modeladmin(model):
    """Huge hack to get the registered modeladmin for the model.
    
    We need this functionality in case someone else already registered a
    different modeladmin for this model.
    """
    return type(admin.site._registry[model])


class PageTaggingAdmin(admin.StackedInline):
    """Inline admin interface for `PageTagging` model."""

    model = models.PageTagging
    fields = ('page_tags',)
    formfield_overrides = {
        TagField: {
            'widget': AutocompleteWidget(attrs={'size':'50'})
        }
    }

# Append inline admin to PageAdmin
RegisteredPageAdmin = _get_registered_modeladmin(Page)
RegisteredPageAdmin.inlines.append(PageTaggingAdmin)
RegisteredPageAdmin.change_form_template = 'pagetags/change_form.html'

try:
    admin.site.unregister(Page)
except NotRegistered:
    pass
admin.site.register(Page, RegisteredPageAdmin)

