# -*- coding: utf-8 -*-
""" Source module
"""

import re
import os.path as Path
try:
	from os import scandir as ScanDir
except ImportError:
	from os import listdir as ScanDir
from os import getcwd

from .setting import SettingManager as SMgr

class Source(object):
	"""docstring for Source."""

	def __init__(self, name,
		directory = None, namespace = None, ext = None,
		settings = None):
		super(Source, self).__init__()
		if settings is None:
			settings = SMgr.GetCurrent().Settings
		if directory is None:
			directory, name = Path.split(name)
		if ext is None:
			name, ext = Path.splitext(name)
		self.name = name
		self.directory = directory
		self.namespace = namespace
		self.ext = ext
		self.smgr = settings

	def __len__(self):
		return 1

	def GetAll(self):
		return [self]

	def GetPath(self):
		return Path.join(self.directory, ".".join([self.name, self.ext]))

	def GetAbsPath(self):
		return Path.join(self.smgr.get("source.basedir", getcwd()), self.GetPath())

	def GetBuildPath(self):
		path = [self.smgr.get("source.build.dir", "build")]
		path += self.namespace.split('.')
		ext = self.smgr.get("source.build.ext.{}".format(self.ext), "build")
		path += [".".join([self.name, ext])]
		return Path.join(*path)

	def GetAbsBuildPath(self):
		return Path.join(self.smgr.get("source.basedir", getcwd()), self.GetBuildPath())


class Sources(Source):
	"""docstring for Sources."""

	def __init__(self, directory, names = None,
				 basedir = None, namespace = None,
				 settings = None, name = None):
		if name is None:
			name = Path.split(directory)[1]
		super(Sources, self).__init__(name, directory, namespace = namespace, settings=settings)
		self.basedir = basedir
		if callable(names):
			names = names(self)
		if names is None:
			self._names = []
		elif not isinstance(names, list):
			self._names = list(names)
		else:
			self._names = names

	def __len__(self):
		return len(self._names)

	def SourceFromName(self, name):
		return Source(name,
			directory = self.basedir + self.directory,
			namespace = (None if self.namespace is None
				else self.namespace + '.' + self.name))

	def GetAll(self):
		ret = []
		for k in self._names:
			if isinstance(k, Source):
				ret += k.GetAll(self)
			else:
				ret.append(self.SourceFromName(k))
		return ret

	def GetBuildPath(self):
		path = [self.smgr.get("source.build.dir", "build")]
		path += self.namespace.split('.')
		ext = self.smgr.get("source.build.ext", None)
		name = self.name + ("." + ext if ext is not None else "")
		path += [name]
		return Path.join(*path)

class SourceDir(Sources):
	"""docstring for SourceDir."""

	@staticmethod
	def _RecursiveFind(adir, num, f_filter = None):
		dlst = []
		ret = []
		with ScanDir(adir) as it:
			for entry in it:
				if entry.is_dir():
					dlst.append(entry.path)
				elif not f_filter or f_filter(entry.name):
					ret.append(entry.path)
		if num != 0:
			for aodir in dlst:
				ret.extend(SourceDir._RecursiveFind(
					Path.join(adir, aodir), num - 1, f_filter))
		return ret

	@staticmethod
	def get_names(self):
		recursive = self.recursive
		if recursive and not isinstance(recursive, int):
			recursive = self.settings.get("SourceDir.recursion.default", 32)
		path_filter = self.path_filter
		if isinstance(path_filter, re.Pattern):
			path_filter = path_filter.fullmatch
		return SourceDir._RecursiveFind(self.basedir + self.directory, self.recursive, path_filter)

	def __init__(self, directory,
				 recursive = False, path_filter = None,
				 basedir = None, namespace = None,
				 settings = None, name = None):
		if path_filter is not None:
			if isinstance(path_filter, str):
				path_filter = re.compile(path_filter)
			elif not isinstance(path_filter, re.Pattern) and not callable(path_filter):
				raise Exception("Path filter is not callable")
		self.path_filter = path_filter
		self.recursive = recursive if recursive else 0
		super(SourceDir, self).__init__(directory,
			basedir = basedir, namespace = namespace,
			settings = settings, name = name)

	def __len__(self):
		if not self._names:
			self._names = SourceDir.get_names(self)
		return len(self._names)

	def GetAll(self):
		if not self._names:
			self._names = SourceDir.get_names(self)
		return super().GetAll()
