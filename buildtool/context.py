# -*- coding: utf-8 -*-
""" Context module
"""

class Context(dict):
    """Context object based on dict."""

    UNUSED = object()

    SourcesKey = object()
    HeadersKey = object()

    def __init__(self, *args, **kwargs):
        super(Context, self).__init__(*args, **kwargs)

    @property
    def sources(self):
        return self[Context.SourcesKey]

    @sources.setter
    def sources(self, value):
        self[Context.SourcesKey] = value
        return value

    @property
    def headers(self):
        return self[Context.HeadersKey]

    @headers.setter
    def headers(self, value):
        self[Context.HeadersKey] = value
        return value
