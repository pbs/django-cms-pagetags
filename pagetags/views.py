# -*- coding: utf-8 -*-
"""
Views for Pagetags Django CMS plugin.

.. seealso::
    http://docs.djangoproject.com/en/1.4/ref/class-based-views/
"""
from django.http import JsonResponse

from tagging.models import Tag


def list_tags(request):
    q = request.GET.get('q')
    tags = []
    if q:
        tags = (Tag.objects
                .filter(name__istartswith=q)
                .values_list('name', flat=True))
    response = [ {'id':tag, 'label':tag, 'value':tag}  for tag in tags ]
    return JsonResponse(response, safe=False)
