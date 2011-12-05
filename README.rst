django-cms-pagetags
===================

``pagetags`` is a `django-cms`_ plugin that allows you to tag django-cms pages. With
this functionality in place now you can group pages and iterate over them using custom
templatetags. For your convenience it comes with autocomplete functionality.


Usage
=====

This plugin is based on django-tagging application so it uses the `TagInput`_ to
associate tags to a page.

To iterate over existing pages based on tags you can use this templatetags:

* ``pages_with_tags``: this templatetag takes tags as input strings and returns a list
  of pages that share the same tags. This result list can be ordered ``alphabetical`` or
  ``chronological`` using the optional ``order`` keyword and also limit the number of result
  using the optional ``limit`` keyword. The tags can be specified exactly as in ``TagInput`` field.

Usage::

    {% pages_with_tags <"tag1, [tag2, tag3, ...]" | varname> [order chronological|alphabetical] [limit <int>] as <varname> %}

* ``pages_similar_with``: this templatetag takes a page slug as input and returns a
  list of pages that shares the same tags with the input page. This templatetag comes
  with a builtin ordering which will order the result pages after the number of
  shared tags in descending order. This result list can also be limited using
  the optional ``limit`` keyword.

Usage::

    {% pages_similar_with <"pageslug" | varname> [limit <int>] as <varname> %}


Settings
========

You can use the django-tagging configuration variable:

* ``FORCE_LOWERCASE_TAGS``:  this variable will enforce to create only lowercase
  tags. Default is set to False.


Example
=======

Templatetag usage::

    {% load page_tags %}

    {% pages_with_tags 'literature, painting' order alphabetical limit 10 as page_list %}
    <ul>
        {% for page in page_list %}
            <li>{{ page }}</li>
        {% endfor %}
    </ul>

    {% pages_similar_with 'space_news' limit 5 as pagelist %}
    <ul>
    {% for page in pagelist %}
        <li>{{ page }}</li>
        {% endfor %}
    </ul>

.. _django-cms:
    http://django-cms.org/

.. _TagInput:
    http://api.rst2a.com/1.0/rst2/html?uri=http://django-tagging.googlecode.com/svn/trunk/docs/overview.txt#tag-input
