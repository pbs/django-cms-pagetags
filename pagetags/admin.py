from django.contrib import admin
from cms.admin.pageadmin import PageAdmin
from cms.models import Page


class TaggedPageAdmin(PageAdmin):
    pass


admin.site.unregister(Page)
admin.site.register(Page, TaggedPageAdmin)
