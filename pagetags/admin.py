from django.contrib import admin
from django.contrib.admin.sites import NotRegistered

from cms.admin.pageadmin import PageAdmin
from cms.models.pagemodel import Page

from models import PageTagging


class PageTaggingAdmin(admin.TabularInline):
    model = PageTagging


PageAdmin.inlines.append(PageTaggingAdmin)

try:
    admin.site.unregister(Page)
except NotRegistered:
    pass
admin.site.register(Page, PageAdmin)
