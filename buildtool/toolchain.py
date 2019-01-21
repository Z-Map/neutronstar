# -*- coding: utf-8 -*-
""" Toolchain module
"""

import os.path as Path

from .source import Source, Sources
from .compiler import ClangCompiler
from .error import TaskError

class Toolchain(object):
	"""Toolchain module"""

	def __init__(self, name, **kwargs):
		super(Toolchain, self).__init__()
		self.name = name
		self.chain = []

	def __call__(self, context):
		return self.build(context)

	def __len__(self):
		return len(self.chain)

	def __add__(self, val):
		if isinstance(val, Toolchain):
			tc = self.copy()
			tc.chain += val.top_chain
			return tc
		elif isinstance(val, (list, tuple)) and all((callable(v for v in val))):
			tc = self.copy()
			tc.chain += val
			return tc
		raise NotImplementedError

	def __sub__(self, val):
		if callable(val) and val in self.chain:
			tc = self.copy()
			tc.chain.remove(val)
		elif isinstance(val, int):
			if val <= len(self.chain):
				tc = self.copy()
				tc.chain = tc.chain[:-val]
			else:
				raise ValueError("Not enough tools in the chain")
		raise NotImplementedError

	def __iadd__(self, val):
		if isinstance(val, Toolchain):
			self.chain += val.top_chain
			return self
		elif isinstance(val, (list, tuple)) and all((callable(v for v in val))):
			self.chain += val
			return self
		raise NotImplementedError

	def __isub__(self, val):
		if callable(val) and val in self.chain:
			self.chain.remove(val)
			return self
		elif isinstance(val, int):
			if val <= len(self.chain):
				self.chain = self.chain[:-val]
			else:
				raise ValueError("Not enough tools in the chain")
			return self
		raise NotImplementedError

	@property
	def top_chain(self):
		if all((isinstance(v, Toolchain) for v in self.chain)):
			return self.chain
		return [self]

	def add(self, *args):
		for val in args:
			if isinstance(val, Toolchain):
				self.chain += val.top_chain
			elif isinstance(val, (list, tuple)) and all((callable(v for v in val))):
				self.chain += val
			else:
				raise ValueError("object need to be callable to be added in toolchain")
		return self

	def remove(self, *args):
		for val in args:
			if callable(val) and val in self.chain:
				self.chain.remove(val)
			elif isinstance(val, int):
				if val <= len(self.chain):
					self.chain = self.chain[:-val]
				else:
					raise ValueError("Not enough tools in the chain")
		return self

	def copy(self):
		new_tc = Toolchain(self.name)
		new_tc.chain = list(self.chain)
		return new_tc

	def build(self, context):
		state = True
		for atool in self.chain:
			state = atool(context)
			if not state:
				state = TaskError(type(self), self.name, state)
				break
		return state

class CompileToolchain(Toolchain):
	""" Toolchain de compilation """

	def __init__(self, compiler, name="Compile toolchain",
		sources_names=None):
		super(CompileToolchain, self).__init__(name)
		self.compiler = compiler
		self.chain = [self.gathering_sources, self.compile]
		if sources_names is None:
			self.src_names = ("SOURCES", "SRC")
		elif isinstance(sources_names, str):
			self.src_names = (sources_names,)
		else:
			self.src_names = tuple(sources_names)

	def copy(self):
		ntc = CompileToolchain(self.compiler, name=self.name, sources_names=self.src_names)
		ntc.chain = list(self.chain)
		return ntc

	def gathering_sources(self, context):
		srcs = []
		for n in self.src_names:
			s = context.get(n)
			if s:
				srcs.append(s)
		if len(srcs) == 1 and isinstance(srcs[0], Sources):
			srcs = srcs[0]
		else:
			srcs = Sources("", names=srcs)
		context.sources = srcs
		return True

	def compile(self, context):
		ret = True
		if context.sources:
			ret = self.compiler.compile(context.sources, context)
		return ret

	def build(self, context):
		state = True
		for atool in self.chain:
			state = atool(context)
			if not state:
				state = TaskError(type(self), self.name, state)
				break
		return state

class CToolchain(CompileToolchain):
	"""Toolchain de compilation C"""

	def __init__(self, compiler=None, name="C toolchain",
		sources_names=None, headers_names=None,
		unique_o=False, library_mode=False):
		if compiler is None:
			compiler = ClangCompiler()
		super(CToolchain, self).__init__(compiler, name=name, sources_names=sources_names)
		self.chain = [self.gathering_headers] + self.chain
		self.unique_o = unique_o
		self.library_mode = library_mode
		if headers_names is None:
			self.headers_names = ("HEADERS",)
		elif isinstance(headers_names, str):
			self.headers_names = (headers_names,)
		else:
			self.headers_names = tuple(headers_names)

	def copy(self):
		ntc = CToolchain(self.compiler, name=self.name,
			sources_names=self.src_names, headers_names=self.headers_names,
			unique_o=self.unique_o, library_mode=self.library_mode)
		ntc.chain = list(self.chain)
		return ntc

	def gathering_headers(self, context):
		headers = []
		for n in self.headers_names:
			h = context.get(n)
			if h:
				headers.append(h)
		if len(headers) == 1 and isinstance(headers[0], Sources):
			headers = headers[0]
		else:
			headers = Sources("", names=headers)
		context.headers = headers
		return True

	def compile(self, context):
		ret = True
		if context.sources:
			ret = self.compiler.compile(context.sources, context)
		return ret
