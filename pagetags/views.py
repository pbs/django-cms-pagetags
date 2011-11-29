# Create your views here.

from django.http import HttpResponse
from tagging.models import Tag
import json

def list_tags(request):
    q = request.GET.get('q')
    tags = []
    if q:
        tags = (Tag.objects
                .filter(name__istartswith=q)
                .values_list('name', flat=True))
    response = [dict(id=tag, label=tag, value=tag) for tag in tags]
    return HttpResponse(json.dumps(response), mimetype='application/json')
