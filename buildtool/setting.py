# -*- coding: utf-8 -*-
""" Setting module
"""

import uuid
import os.path as Path

class SettingNamespace(dict):

	NAMESPACE_VALUE = object()

	@classmethod
	def from_value(cls, val):
		ns = cls()
		ns[SettingNamespace.NAMESPACE_VALUE] = val
		return ns

	@property
	def has_value(self):
		if SettingNamespace.NAMESPACE_VALUE in self:
			return True
		return False

	def get_value(self, default):
		if self.has_value:
			return self[SettingNamespace.NAMESPACE_VALUE]
		self[SettingNamespace.NAMESPACE_VALUE] = default
		return default

class Setting(object):
	"""Setting class"""
	UNSET = object()

	def __init__(self, mgr, key=""):
		super(Setting, self).__init__()
		self._mgr = mgr
		self.key = key

	def get(self, key="", default=UNSET):
		if self.key:
			key = self.key + "." + key
		return self._mgr.get(key, default)

	def get_abs(self, key="", default=UNSET):
		return self._mgr.get(key, default)

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
		self._override_states = {}
		self._override_settings = {}

	def __getitem__(self, key):
		return self._settings[key]

	def __setitem__(self, key, val):
		self._settings[key] = val
		return val

	def __delitem__(self, key):
		del self._settings[key]

	def get(self, key, default=Setting.UNSET):
		if key:
			if key in self._override_settings:
				return self._override_settings[key]
			path = str(key).split('.')
			key = path[-1]
			path = path[:-1]
			target_dict = self._settings
			if path:
				for ns in path:
					if ns in target_dict:
						if isinstance(target_dict[ns], SettingNamespace):
							target_dict = target_dict[ns]
						else:
							target_dict[ns] = SettingNamespace.from_value(target_dict[ns])
					else:
						target_dict[ns] = SettingNamespace()
						target_dict = target_dict[ns]
			if key not in target_dict:
				target_dict[key] = default
			return target_dict[key]
		else:
			return self._settings

	@property
	def Settings(self):
		"""Access to sored settings"""
		return Setting(self)

	@property
	def Settings(self):
		"""Access to sored settings"""
		return self._override_settings

	def from_namespace(self, namespace):
		return Setting(self, key = namespace)

	def save_override(self):
		key = uuid.uuid1()
		self._override_states[key] = self._override_settings
		self._override_settings = self._override_settings.copy()
		return key

	def restore_override(self, key):
		if key in self._override_states:
			self._override_settings = self._override_states[key]
			del self._override_states[key]
			return True
		return False

	def discard_override(self, key=None):
		if key is None:
			if self._override_settings:
				self._override_settings = {}
				return True
		elif key in self._override_states:
			del self._override_states[key]
			return True
		return False
