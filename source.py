# -*- coding: utf-8 -*-
""" Source module
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

	def GetAll(self):
		return [self]


class Sources(Source):
	"""docstring for Sources."""

	def __init__(self, directory, names = None, basedir = None, namespace = None):
		super(Sources, self).__init__(Path.split(directory)[1], directory, namespace = namespace)
		self.basedir = basedir
		if callable(names):
			names = names(self)
		if names is None:
			self._names = []
		elif not isinstance(names, list):
			self._names = list(names)
		else:
			self._names = names

	def SourceFromName(self, name):
		return Source(name,
			directory = self.basedir + self.directory,
			namespace = None if self.namespace is None else self.namespace + self.name)

	def GetAll(self):
		ret = []
		for k in self._names:
			if isinstance(k, Source):
				ret += k.GetAll(self)
			else:
				ret.append(self.SourceFromName(k))
		return ret
