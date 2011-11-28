import random
import string
from django.forms.widgets import TextInput
from django.utils.safestring import mark_safe
from django.contrib import admin
from django.contrib.admin.sites import NotRegistered
from django.core.urlresolvers import reverse


from tagging.fields import TagField
from cms.models.pagemodel import Page

from models import PageTagging


def _get_registered_modeladmin(model):
    """ This is a huge hack to get the registered modeladmin for the model.
        We need this functionality in case someone else already registered
        a different modeladmin for this model. """
    return type(admin.site._registry[model])


class AutocompleteWidget(TextInput):
    def render(self, *args, **kwargs):
        id = (kwargs
                .get('attrs', {})
                .get('id', random.sample(string.letters, 15)))
        html = super(AutocompleteWidget, self).render(*args, **kwargs)
        url = reverse('pagetags.views.list_tags')
        js = '<script type="text/javascript">autocomplete("%s", "%s")</script>'
        js %= (id, url)
        return mark_safe(html + js)


class PageTaggingAdmin(admin.TabularInline):
    model = PageTagging
    fields = ('page_tags',)
    formfield_overrides = {
        TagField: {
            'widget': AutocompleteWidget(attrs={'size':'50'})
        }
    }



RegisteredPageAdmin = _get_registered_modeladmin(Page)
RegisteredPageAdmin.inlines.append(PageTaggingAdmin)
RegisteredPageAdmin.change_form_template = 'pagetags/change_form.html'

try:
    admin.site.unregister(Page)
except NotRegistered:
    pass
admin.site.register(Page, RegisteredPageAdmin)
