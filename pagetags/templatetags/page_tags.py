import re

from django import template
from django.conf import settings
from django.db.models import Q
from cms.models import Page

from tagging.models import TaggedItem
from tagging.utils import parse_tag_input
from pagetags.models import PageTagging


register = template.Library()


class StaticSlug(unicode):
    def bind(self, context):
        pass

class DynamicSlug(unicode):
    def __init__(self, varname):
        self.varname = varname
        self._value = u''

    def bind(self, context):
        self._value = context[self.varname]

    def __unicode__(self):
        return self._value


class StaticTags(list):
    def __init__(self, tags):
        super(StaticTags, self).__init__(parse_tag_input(tags))

    def bind(self, context):
        pass


class DynamicTags(list):
    def __init__(self, varname):
        self.varname = varname
        super(DynamicTags, self).__init__()

    def bind(self, context):
        self[:] = parse_tag_input(context.get(self.varname, ''))



class TaggedPagesNode(template.Node):
    def __init__(self, parsed_tags, ordering, var_name):
        self.parsed_tags = parsed_tags
        self.var_name = var_name
        self.ordering = ordering or 'chronological'

    def render(self, context):
        self.parsed_tags.bind(context)
        pagetaggings_from_site = PageTagging.objects.filter(
            page__site=settings.SITE_ID
        ).select_related()

        if self.ordering == 'alphabetical':
            pagetaggings_from_site = pagetaggings_from_site.order_by(
                'page__title_set__slug'
            )

        if self.ordering == 'chronological':
            pagetaggings_from_site = pagetaggings_from_site.order_by(
                '-page__publication_date'
            )

        page_taggings = TaggedItem.objects.get_by_model(
            pagetaggings_from_site, self.parsed_tags
        )

        context[self.var_name] = [
            page_tagging.page for page_tagging in page_taggings
        ]
        return ''


class SimilarPagesNode(template.Node):
    def __init__(self, parsed_slug, var_name):
        self.parsed_slug = parsed_slug
        self.var_name = var_name

    def render(self, context):
        self.parsed_slug.bind(context)
        try:
            page = Page.objects.get(
                Q(site=settings.SITE_ID),
                Q(title_set__slug=self.parsed_slug)
            )
        except Page.DoesNotExist:
            return ''

        page_taggings = TaggedItem.objects.get_related(
            page.pagetagging,
            PageTagging.objects.select_related().filter(
                page__site=settings.SITE_ID
            )
        )
        context[self.var_name] = [
            page_tagging.page for page_tagging in page_taggings
        ]
        return ''


def _extract_tag_content(token):
    try:
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError(
            "%r tag requires additional arguments" % token.contents.split()[0]
        )
    return tag_name, arg

def parsed_tags(quoted_or_var):
    if (quoted_or_var[0] == quoted_or_var[-1]
    and quoted_or_var[0] in ('"', "'")):
        return StaticTags(tags=quoted_or_var[1:-1])
    return DynamicTags(varname=quoted_or_var)

def parse_slug(quoted_or_var):
    if (quoted_or_var[0] == quoted_or_var[-1]
    and quoted_or_var[0] in ('"', "'")):
        return StaticSlug(quoted_or_var[1:-1])
    return DynamicSlug(varname=quoted_or_var)


@register.tag
def pages_with_tags(parser, token):
    parsed_tags, ordering, var_name = _parse_pages_with_tags(parser, token)
    return TaggedPagesNode(parsed_tags, ordering, var_name)

def _parse_pages_with_tags(parser, token):
    tag_name, arg = _extract_tag_content(token)

    m = re.search(r'(.*?) (order (alphabetical|chronological) )*as (\w+)', arg)
    if not m:
        raise template.TemplateSyntaxError(
            "%r tag had invalid arguments" % tag_name
        )
    tags, _, ordering, var_name = m.groups()

    return parsed_tags(tags), ordering, var_name


@register.tag
def pages_similar_with(parser, token):
    parsed_slug, var_name = _parse_pages_similar_with(parser, token)
    return SimilarPagesNode(parsed_slug, var_name)

def _parse_pages_similar_with(parser, token):
    tag_name, arg = _extract_tag_content(token)

    m = re.search(r'(.*?) as (\w+)', arg)
    if not m:
        raise template.TemplateSyntaxError(
            "%r tag had invalid arguments" % tag_name
        )
    page_slug, var_name = m.groups()

    return parse_slug(page_slug), var_name
