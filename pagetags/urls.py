from django.conf.urls.defaults import *

urlpatterns = patterns('pagetags.views',
    url(r'^$', 'list_tags'),
)
