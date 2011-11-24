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
    def __init__(self, format_string, var_name):
        self.format_string = format_string
        self.var_name = var_name

    def render(self, context):
        parsed_tags = parse_tag_input(self.format_string)

        pagetaggings_from_site = PageTagging.objects.filter(
            page__site=settings.SITE_ID
        ).select_related()

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
    format_string, var_name = _validate_template(parser, token)
    return TaggedPagesNode(format_string, var_name)

@register.tag
def pages_similar_with(parser, token):
    format_string, var_name = _validate_template(parser, token)
    return SimilarPagesNode(format_string, var_name)

def _validate_template(parser, token):
    try:
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires a single argument" % token.contents.split()[0])
    m = re.search(r'(.*?) as (\w+)', arg)
    if not m:
        raise template.TemplateSyntaxError("%r tag had invalid arguments" % tag_name)
    format_string, var_name = m.groups()
    if not (format_string[0] == format_string[-1] and format_string[0] in ('"', "'")):
        raise template.TemplateSyntaxError("%r tag's argument should be in quotes" % tag_name)
    return format_string[1:-1], var_name
