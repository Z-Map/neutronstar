# -*- coding: utf-8 -*-
""" Project module
"""

import os.path as Path

from .context import *
from .toolchain import *
from .target import *
from .module import *

class Project(object):
	"""Project object"""
	def __init__(self, name):
		super(Project, self).__init__()
		self.name = name
		self.toolchains = []
		self.targets = []
		self.modules = []

	def add_toolchain(self, tc, *args, **kwargs):
		if not isinstance(tc, Toolchain):
			tname = tc
			try:
				tc = Toolchain(tname, *args, **kwargs)
			except Exception as e:
				raise Exception("Error when creating toolchain {}".format(str(tname))) from e
		self.toolchains.append(tc)
		return tc

	def add_target(self, tgt, *args, **kwargs):
		if not isinstance(tgt, Target):
			tname = tgt
			try:
				tgt = Target(tname, *args, **kwargs)
			except Exception as e:
				raise Exception("Error when creating target {}".format(str(tname))) from e
		self.targets.append(tgt)
		return tgt

	def add_module(self, mod, *args, **kwargs):
		if not isinstance(mod, Module):
			modname = mod
			try:
				mod = Module(modname, *args, **kwargs)
			except Exception as e:
				raise Exception("Error when creating module {}".format(str(modname))) from e
		self.modules.append(mod)
		return mod

	def display(self):
		print('Project "{name}"\n'.format(name=self.name))
		pading = 1
		print(" " * pading, "Toolchains :")
		pading += 1
		if self.toolchains:
			for t in self.toolchains:
				print(" " * pading, t)
		else:
			print(" " * pading, "No toolchain in the project")
		pading -= 1
		print(" " * pading, "Targets :")
		pading += 1
		if self.targets:
			for t in self.targets:
				print(" " * pading, t)
		else:
			print(" " * pading, "No target in the project")
		pading -= 1
		print(" " * pading, "Modules :")
		pading += 1
		if self.modules:
			for m in self.modules:
				print(" " * pading, m)
		else:
			print(" " * pading, "No module in the project")
		pading -= 1

	def build(self):
		ctx = Context()
		ret = True
		for mod in self.modules:
			ret = mod.build(ctx)
			if not ret:
				raise ret
