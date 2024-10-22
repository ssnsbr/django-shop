from django.utils.http import urlencode
from django.urls import reverse as original_reverse


def query_reverse(*args, **kwargs):

    query = kwargs.pop("query", {})
    url = original_reverse(*args, **kwargs)

    if query:
        url += "?" + urlencode(query)

    return url
