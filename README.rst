django-cms-pagetags
===================

``pagetags`` is a `django-cms`_ plugin that allows you to tag django-cms pages.
With this functionality and corresponding templatetags in place you can group
and list pages by their similarity, used tags and even create tag clouds. It
works with `django-tagging`_ and `django-tagging-ng`_ and comes with
autocomplete functionality.


Usage
=====

This plugin is based on ``django-tagging`` application so it uses the `TagInput`_
to associate tags to a page.

In your ``settings.py`` add::

    INSTALLED_APPS = (
        'tagging',
        'pagetags',
        ...
    )

In your ``urls.py`` add::

    urlpatterns += patterns('',
        url(r'^admin/tagging/autocomplete', include('pagetags.urls')),
        ...
    )

To iterate over existing pages based on tags you can use this templatetags:

* ``pages_with_tags``: this templatetag takes tags as input strings and returns
  a list of pages that share the same tags. This result list can be ordered
  ``alphabetical`` or ``chronological`` using the optional ``order`` keyword and
  also limit the number of result using the optional ``limit`` keyword. The tags
  can be specified exactly as in ``TagInput`` field. Usage::

    {% pages_with_tags <"tag1, [tag2, tag3, ...]" | varname> [order chronological|alphabetical] [limit <int>] as <varname> %}

* ``pages_similar_with``: this templatetag takes a page slug as input and
  returns a list of pages that shares the same tags with the input page. This
  templatetag comes with a builtin ordering which will order the result pages
  after the number of shared tags in descending order. This result list can also
  be limited using the optional ``limit`` keyword. Usage::

    {% pages_similar_with <"pageslug" | varname> [limit <int>] as <varname> %}

Also checkout templatetags in documentation of `django-tagging`_ or
`django-tagging-ng`_.


Settings
========

Check ``django-tagging`` and ``django-tagging-ng`` documentation for
details about configuration options.

Quick list for ``django-tagging``:

* ``FORCE_LOWERCASE_TAGS``
* ``MAX_TAG_LENGTH``

Quick list for ``django-tagging-ng``:

* ``FORCE_LOWERCASE_TAGS``
* ``FORCE_TAG_DELIMITER``
* ``MAX_TAG_LENGTH``
* ``MULTILINGUAL_TAGS``


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

.. _django-tagging:
    http://code.google.com/p/django-tagging/

.. _django-tagging-ng:
    http://github.com/svetlyak40wt/django-tagging-ng

.. _TagInput:
    http://api.rst2a.com/1.0/rst2/html?uri=http://django-tagging.googlecode.com/svn/trunk/docs/overview.txt#tag-input
