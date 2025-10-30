# yourapp/templatetags/query_utils.py
from django import template
from urllib.parse import urlencode

register = template.Library()

@register.filter
def preserve_query(query_string, exclude=None):
    """
    Remove specific param(s) from query string.
    Usage: {{ request.META.QUERY_STRING|preserve_query:"scroll_to" }}
    """
    if not query_string:
        return ''
    params = {}
    for part in query_string.split('&'):
        if '=' in part:
            key, val = part.split('=', 1)
            if key != exclude:
                params[key] = val
    return urlencode(params)

@register.filter
def add_query(query_string, add_param):
    """
    Add a param to query string.
    Usage: {{ request.META.QUERY_STRING|add_query:"scroll_to=my-slug" }}
    """
    if not query_string:
        return add_param
    return query_string + '&' + add_param