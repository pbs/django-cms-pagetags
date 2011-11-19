import re

from django import template
from cms.models import Page

from tagging.models import TaggedItem
from pagetags.models import PageTagging


class TaggedPagesNode(template.Node):
    def __init__(self, format_string, var_name):
        self.format_string = format_string
        self.var_name = var_name
    def render(self, context):
        tagged_pages = TaggedItem.objects.get_by_model(PageTagging, self.format_string.split(' '))
        result_pages = [Page.objects.get(pk=tagged_page.page_id) for tagged_page in tagged_pages]
        context[self.var_name] = result_pages
        return ''


def get_tagged_pages(parser, token):
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
    return TaggedPagesNode(format_string[1:-1], var_name)


class SimilarPagesNode(template.Node):
    def __init__(self, format_string, var_name):
        self.format_string = format_string
        self.var_name = var_name
    def render(self, context):
        page = Page.objects.get(id=int(self.format_string))
        page_tags = page.page_tags.values()[0]['page_tags'].split(' ')
        tagged_pages = TaggedItem.objects.get_union_by_model(PageTagging, page_tags)
        result_pages = [Page.objects.get(pk=tagged_page.page_id) for tagged_page in tagged_pages]
        context[self.var_name] = result_pages
        return ''


def get_similar_pages(parser, token):
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
    return SimilarPagesNode(format_string[1:-1], var_name)


register = template.Library()
register.tag('pages_with_tags', get_tagged_pages)
register.tag('pages_similar_with', get_similar_pages)
