# -*- coding: utf-8 -*-
""" Compiler module
"""

import os.path as Path

class Compiler(object):

	def __init__(self, name, settings = None):
		if settings is None:
			settings = SMgr.GetCurrent().Settings
		self.smgr = settings
		self.name = name

	def compile(self, source):
		raise NotImplementedError("You need to use a valid compiler")

class ClangCompiler(Compiler):

	def __init__(self, name="clang", settings = None):
		super(ClangCompiler, self).__init__(name, settings = settings)

	def compile(self, source):
		
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
