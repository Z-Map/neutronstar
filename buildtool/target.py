# -*- coding: utf-8 -*-
""" Target module
"""

import os.path as Path

class Target(object):
	"""Target module"""
	def __init__(self, name):
		super(Target, self).__init__()
		self.name = name
