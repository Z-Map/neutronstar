# -*- coding: utf-8 -*-
""" Compiler module
"""

import subprocess
import os.path as Path
from .setting import SettingManager as SMgr

class Compiler(object):

	def __init__(self, name, settings = None):
		if settings is None:
			settings = SMgr.GetCurrent().from_namespace("compiler")
		self.smgr = settings
		self.name = name

	def _generate_args(self, source):
		args = []
		for asrc in source.GettALl():
			args.append(asrc.GetPath())
		return args

	def _compile(self, args, source):
		raise NotImplementedError("You need to use a valid compiler")

	def compile(self, source, cmd_override=None):
		args = self._generate_args(source)
		return cmd_override(args, source) if callable(cmd_override) else self._compile(args, source)


class ClangCompiler(Compiler):

	def __init__(self, name="clang", cmd="clang", settings = None):
		if settings is None:
			settings = SMgr.GetCurrent().from_namespace("compiler.clang")
		super(ClangCompiler, self).__init__(name, settings = settings)
		self.cmd = cmd

	def _generate_args(self, source):
		compile_type =self.smgr.get("compilation_type", "obj")
		args = []
		if compile_type == "obj":
			args = ["-c"]
			for asrc in source.GettALl():
				args.append(asrc.GetPath())
			if len(source) == 1:
				args += ["-o", asrc.GetBuildPath()]
		elif compile_type == "exe":
			args = ["-o", source.GetBuildPath()]
			for asrc in source.GettALl():
				args.append(asrc.GetPath())
		elif compile_type == "lib":
			for asrc in source.GettALl():
				args.append(asrc.GetPath())
			args += ["-shared", "-o", source.GetBuildPath()]

		return args

	def _compile(self, args, source):
		try:
			ret = subprocess.run([self.cmd] + args, stdout=subprocess.PIPE)
		except subprocess.CalledProcessError as err:
			print("Error ", err.returncode, " during compiling ", source.name)
			return False
		return True


class CCompiler(object):

	FNAME = 0
	TARGNAME = 1

	def __init__(self, cmd, objbc = ("-o", TARGNAME, "-c", FNAME),
		lobjbc = ("-fPIC", "-o", TARGNAME , "-c", FNAME),
		exebc = ("-o", TARGNAME, FNAME),
		libbc = (FNAME, "-shared", "-o", TARGNAME)):
		self.cmd = cmd
		self.lobjbc = lobjbc
		self.objbc = objbc
		self.exebc = exebc
		self.libbc = libbc
		self._libmode = False

	@property
	def libmode(self):
		return (self._libmode)

	@libmode.setter
	def set_libmode(self, val):
		if val:
			self._libmode = True
		else:
			self._libmode = False
		return val

	def arg_assemble(self, argptrn, inarg):
		args = []
		for anarg in argptrn:
			if type(anarg) != str:
				if type(inarg[anarg]) == str:
					args.append(inarg[anarg])
				else:
					args += inarg[anarg]
			else:
				args.append(anarg)
		return args

	def _lbuildfile(self, env, fname, tfname):
		args = env["CFLAGS"] + self.arg_assemble(self.lobjbc,(fname, tfname)) + env["LCFLAGS"]
		try:
			ret = subprocess.run([self.cmd] + args, stdout=subprocess.PIPE)
		except subprocess.CalledProcessError as err:
			print("Error on file ", fname)
			return 0
		print(self.cmd, " ".join(args))
		return 1

	def _buildfile(self, env, fname, tfname):
		args = env["CFLAGS"] + self.arg_assemble(self.objbc,(fname, tfname)) + env["LCFLAGS"]
		try:
			ret = subprocess.run([self.cmd] + args, stdout=subprocess.PIPE)
		except subprocess.CalledProcessError as err:
			print("Error on file ", fname)
			return 0
		print(self.cmd, " ".join(args))
		return 1

	def _buildexe(self, env, fname, tfname):
		args = env["CFLAGS"] + self.arg_assemble(self.exebc,(fname, tfname)) + env["LCFLAGS"]
		try:
			ret = subprocess.run([self.cmd] + args, stdout=subprocess.PIPE)
		except subprocess.CalledProcessError as err:
			print("Error on file ", fname)
			return 0
		print(self.cmd, " ".join(args))
		return 1

	def _buildlib(self, env, fnames, tfname):
		args = env["CFLAGS"] + self.arg_assemble(self.libbc,(fname, tfname)) + env["LCFLAGS"]
		try:
			ret = subprocess.run([self.cmd] + args, stdout=subprocess.PIPE)
		except subprocess.CalledProcessError as err:
			print("Error on file ", fname)
			return 0
		print(self.cmd, " ".join(args))
		return 1

	def buildsrc(self, env, fname, tfname):
		if self._libmode:
			return self._lbuildfile(env, fname, tfname)
		else:
			return self._buildfile(env, fname, tfname)

	def build(self, env, srclst, tfname):
		if self._libmode:
			return self._buildlib(env, srclst, tfname)
		else:
			return self._buildexe(env, srclst, tfname)
