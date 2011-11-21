from django.contrib import admin
from django.contrib.admin.sites import NotRegistered

from cms.models.pagemodel import Page

from models import PageTagging


def _get_registered_modeladmin(model):
    """ This is a huge hack to get the registered modeladmin for the model.
        We need this functionality in case someone else already registered
        a different modeladmin for this model. """
    return type(admin.site._registry[model])


class PageTaggingAdmin(admin.TabularInline):
    model = PageTagging


RegisteredPageAdmin = _get_registered_modeladmin(Page)
RegisteredPageAdmin.inlines.append(PageTaggingAdmin)

try:
    admin.site.unregister(Page)
except NotRegistered:
    pass
admin.site.register(Page, RegisteredPageAdmin)
