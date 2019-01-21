# -*- coding: utf-8 -*-
""" Module module
"""

import os.path as Path

from .error import TaskError
from .toolchain import Toolchain

class Module(object):
	"""Module module"""
	def __init__(self, name, **kwargs):
		super(Module, self).__init__()
		self.name = name
		self.vars = kwargs.copy()
		self.toolchains = Toolchain(name)

	def __str__(self):
		return 'Module("{}", [{}])'.format(
			self.name,
			', '.join(['"{}":"{}"'.format(k, v) for k,v in self.vars.items()]))

	def add_toolchain(self, toolchain):
		self.toolchains.add(toolchain)
		return self

	def build(self, context):
		ctx = context
		ctx.update(self.vars)
		state = True
		print("Compile sources for module", self.name)
		state = self.toolchains(ctx)
		if not state:
			state = TaskError(type(self), self.name, state)
		return state
