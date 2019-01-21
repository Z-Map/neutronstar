# -*- coding: utf-8 -*-
""" Compiler module
"""

import subprocess
import os.path as Path
import os

from .setting import SettingManager as SMgr

class Compiler(object):

	def __init__(self, name, settings = None):
		if settings is None:
			settings = SMgr.GetCurrent().from_namespace("compiler")
		self.smgr = settings
		self.name = name

	def _generate_args(self, source, context):
		args = []
		for asrc in source.GetAll():
			args.append(asrc.GetPath())
		return args

	def _compile(self, args, source, context):
		raise NotImplementedError("You need to use a valid compiler")

	def compile(self, source, context, cmd_override=None):
		args = self._generate_args(source, context)
		return cmd_override(args, source, context) if callable(cmd_override) else self._compile(args, source, context)


class ClangCompiler(Compiler):

	def __init__(self, name="clang", cmd="clang", settings = None):
		if settings is None:
			settings = SMgr.GetCurrent().from_namespace("compiler.clang")
		super(ClangCompiler, self).__init__(name, settings = settings)
		self.cmd = cmd

	def _generate_args(self, source, context):
		compile_type = self.smgr.get("compilation_type", "obj")
		as_lib = self.smgr.get("library", False)
		args = []
		if compile_type == "obj":
			args = ["-c"]
			if as_lib:
				args.append("-fPIC")
			for asrc in source.GetAll():
				args.append(asrc.GetPath())
			if len(source) == 1:
				args += ["-o", asrc.GetBuildPath()]
		elif compile_type == "exe":
			for asrc in source.GetAll():
				args.append(asrc.GetPath())
			if as_lib:
				args += ["-shared", "-o", source.GetBuildPath()]
			else:
				args += ["-o", source.GetBuildPath()]
		return args

	def _compile(self, args, source, context):
		try:
			ret = subprocess.run([self.cmd] + args, capture_output=True, text=True)
		except subprocess.CalledProcessError as err:
			print("Error ", err.returncode, " during compiling ", source.name)
			return False
		else:
			if ret.returncode == 0:
				print(ret.stdout)
			else:
				print(ret.stdout)
				print(ret.stderr)
				return False
		return True
