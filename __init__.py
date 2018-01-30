# -*- coding: utf-8 -*-
"""

"""
import os.path as Path

class Source(object):
	"""docstring for Source."""

	def __init__(self, name, directory = None, namespace = None, ext = None):
		super(Source, self).__init__()
		if directory is None:
			directory, name = Path.split(name)
		if ext is None:
			name, ext = Path.splitext(name)
		self.name = name
		self.directory = directory
		self.namespace = namespace
		self.ext = ext


class Sources(Source):
	"""docstring for Sources."""

	def __init__(self, arg):
		super(Sources, self).__init__()
		self.arg = arg
