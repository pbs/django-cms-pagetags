import re

from django import template
from django.conf import settings
from django.db.models import Q
from cms.models import Page

from tagging.models import TaggedItem
from pagetags.models import PageTagging


class TaggedPagesNode(template.Node):
    def __init__(self, format_string, var_name):
        self.format_string = format_string
        self.var_name = var_name
    def render(self, context):
        stripped_tags = [
            tag.strip() for tag in self.format_string.split(',') if tag.strip()]
        tagged_pages = TaggedItem.objects.get_by_model(
            PageTagging.objects.filter(page__site=settings.SITE_ID), stripped_tags)
        context[self.var_name] = [
            Page.objects.get(pk=tagged_page.page_id) for tagged_page in tagged_pages]
        return ''


class SimilarPagesNode(template.Node):
    def __init__(self, format_string, var_name):
        self.format_string = format_string
        self.var_name = var_name
    def render(self, context):
        page = Page.objects.get(
            Q(site=settings.SITE_ID), Q(title_set__slug=self.format_string))
        result_pages = TaggedItem.objects.get_related(
            page.pagetagging, PageTagging.objects.filter(page__site=settings.SITE_ID))
        context[self.var_name] = [page_tagging.page for page_tagging in result_pages]
        return ''


def get_tagged_pages(parser, token):
    format_string, var_name = _validate_template(parser, token)
    return TaggedPagesNode(format_string, var_name)


def get_similar_pages(parser, token):
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


register = template.Library()
register.tag('pages_with_tags', get_tagged_pages)
register.tag('pages_similar_with', get_similar_pages)
