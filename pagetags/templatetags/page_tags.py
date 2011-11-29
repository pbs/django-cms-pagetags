import re

from django import template
from django.conf import settings
from django.db.models import Q
from cms.models import Page

from tagging.models import TaggedItem
from tagging.utils import parse_tag_input
from pagetags.models import PageTagging


register = template.Library()


class TaggedPagesNode(template.Node):
    def __init__(self, format_string, ordering, var_name):
        self.format_string = format_string
        self.var_name = var_name
        self.ordering = ordering

    def render(self, context):
        parsed_tags = parse_tag_input(self.format_string)

        pagetaggings_from_site = PageTagging.objects.filter(
            page__site=settings.SITE_ID
        ).select_related()

        if self.ordering == 'alphabetical':
            pagetaggings_from_site = pagetaggings_from_site.order_by(
                'page__title_set__slug'
            )

        elif self.ordering == 'chronological':
            pagetaggings_from_site = pagetaggings_from_site.order_by(
                'page__publication_date'
            ).reverse()

        pagetaggings = TaggedItem.objects.get_by_model(
            pagetaggings_from_site, parsed_tags
        )

        context[self.var_name] = [pt.page for pt in pagetaggings]
        return ''


class SimilarPagesNode(template.Node):

    def __init__(self, format_string, var_name):
        self.format_string = format_string
        self.var_name = var_name

    def render(self, context):
        try:
            page = Page.objects.get(
                Q(site=settings.SITE_ID),
                Q(title_set__slug=self.format_string)
            )
        except Page.DoesNotExist:
            return ''

        pagetaggings = TaggedItem.objects.get_related(
            page.pagetagging,
            PageTagging.objects.select_related().filter(
                page__site=settings.SITE_ID
            )
        )
        context[self.var_name] = [pt.page for pt in pagetaggings]
        return ''


@register.tag
def pages_with_tags(parser, token):
    format_string, ordering, var_name = _parse_templatetag(parser, token)
    return TaggedPagesNode(format_string, ordering, var_name)

@register.tag
def pages_similar_with(parser, token):
    format_string, var_name = _parse_templatetag(parser, token)
    return SimilarPagesNode(format_string, var_name)

def _parse_templatetag(parser, token):
    tag_name, arg = token.contents.split(None, 1)
    m = re.search(r'(.*?) order (\w+) as (\w+)', arg)
    format_string, ordering, var_name = m.groups()
    return format_string[1:-1], ordering, var_name
