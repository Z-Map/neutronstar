# -*- coding: utf-8 -*-
""" Toolchain module
"""

import os.path as Path

class Toolchain(object):
	"""Toolchain module"""

	def __init__(self, name, **kwargs):
		super(Toolchain, self).__init__()
		self.name = name
