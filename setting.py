# -*- coding: utf-8 -*-
""" Setting module
"""

import os.path as Path

class Setting(object):
	"""Setting class"""
	def __init__(self, mgr, key=""):
		super(Setting, self).__init__()
		self._mgr = mgr
		self.key = key


class SettingManager(object):
	""" Setting manager class """

	CURRENT_MGR = None

	@classmethod
	def GetCurrent(cls):
		if cls.CURRENT_MGR is None:
			cls.CURRENT_MGR = cls("default")
		return cls.CURRENT_MGR

	@classmethod
	def SetCurrent(cls, mgr):
		cls.CURRENT_MGR = mgr
		return cls.CURRENT_MGR

	def __init__(self, name, **kwargs):
		self.name = name
		self._settings = {}
		for k,v in kwargs.items():
			self._settings[k] = v

	def __getitem__(self, key):
		return self._settings[key]

	def __setitem__(self, key, val):
		self._settings[key] = val
		return val

	def __delitem__(self, key):
		del self._settings[key]

	@property
	def Settings(self):
		"""Access to sored settings"""
		return Setting(self)
