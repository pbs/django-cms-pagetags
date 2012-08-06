# -*- coding: utf-8 -*-
"""
Form fields for Pagetags Django CMS plugin.
"""
from django.forms import widgets
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe

import random
import string


class AutocompleteWidget(widgets.TextInput):
    """Autocomplete widget for `TagField`."""

    def render(self, *args, **kwargs):
        id = (kwargs
                .get('attrs', {})
                .get('id', random.sample(string.letters, 15)))
        html = super(AutocompleteWidget, self).render(*args, **kwargs)
        url = reverse('pagetags.views.list_tags')
        js = '<script type="text/javascript">autocomplete("%s", "%s")</script>'
        js %= (id, url)
        return mark_safe(html + js)

