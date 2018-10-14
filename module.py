# -*- coding: utf-8 -*-
""" Module module
"""

import os.path as Path

class Module(object):
	"""Module module"""
	def __init__(self, name, slots=None):
		super(Module, self).__init__()
		self.name = name
		self.slots = {} if slots is None else {k:(None,None) for k in slots}

	def __str__(self):
		return 'Module("{}", [{}])'.format(
			self.name,
			', '.join(['"{}"'.format(k) for k in self.slots.keys()]))

	def bind(self, slot_name, src=None, toolchain=None):
		if src is None:
			src = self.slots.get(slot_name, (None, None))[0]
		if toolchain is None:
			toolchain = self.slots.get(slot_name, (None, None))[1]
		self.slots[slot_name] = (src, toolchain)
		return self

	def build(self):
		
		return True
