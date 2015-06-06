#!/usr/bin/env python2

"""
	Lua api generator.
"""

import sys
import CppHeaderParser
import os
import errno
import re
from zipfile import *
import fnmatch
import re
import textwrap
import argparse

try:
    from cStringIO import StringIO
except:
    from StringIO import StringIO


ARGP = argparse.ArgumentParser(
	description=__doc__,
	formatter_class=argparse.RawTextHelpFormatter,
)

ARGP.add_argument('input-path', help='input path')
ARGP.add_argument('prefix', help='prefix')
ARGP.add_argument('main-include', help='main include')
ARGP.add_argument('lib-small-name', help='lib small name')
ARGP.add_argument('lib-name', help='lib name')
ARGP.add_argument('api-path', help='api path')
ARGP.add_argument('api-class-path', help='api class-path')
ARGP.add_argument('include-path', help='include path')
ARGP.add_argument('source-path', help='source path')

ARGP.add_argument('--lua-doc-path', help='lua doc path')
ARGP.add_argument('--inherit-in-module-file-path', help='inherit-in-module-file path')

def mkdir_p(path): # Same effect as mkdir -p, create dir and all necessary parent dirs
	try:
		os.makedirs(path)
	except OSError as e:
		if e.errno == errno.EEXIST: # Dir already exists; not really an error
			pass
		else: raise

class LuaBlocks(object):
	@staticmethod
	def PtrLookupArray(prefix, className, ptr):
		block = textwrap.dedent("""
			if {ptr} == nil then return nil end
			for i=1,count({ptr}) do
				local __c  = _G["{classname}"]("__skip_ptr__")
				__c.__ptr = {ptr}[i]
				{ptr}[i] = __c
			end
			return {ptr}
		""").format(
			classname=className.replace("*", ""),
			ptr=ptr,
		).replace('\n', '\n' + prefix.strip('\n')).lstrip('\n').rstrip(' \t')

		return block

	@staticmethod
	def PtrLookup(prefix, className, ptr):
		"""
			Note: We expect className to be a valid string.
		"""

		block = textwrap.dedent("""
			if {ptr} == nil then return nil end
			local __c = _G["{classname}"]("__skip_ptr__")
			__c.__ptr = {ptr}
			return __c
		""").format(
			classname=className.replace("*", ""),
			ptr=ptr,
		).replace('\n', '\n' + prefix.strip('\n')).lstrip('\n').rstrip(' \t')

		return block

def cleanDocs(docs):
	return docs.replace("/*", "").replace("*/", "").replace("*", "").replace("\n", "").replace("\r", "").replace("::", ".").replace("\t", "")

def toLuaType(t):
	return t.replace("void", "nil").replace("int", "Integer").replace("bool", "Boolean").replace("*", "")

# FIXME: Some "unsigned int *" functions are still being generated on the polycode API?
def typeFilter(ty):
	ty = ty.replace("Polycode::", "")
	ty = ty.replace("std::", "")
	ty = ty.replace("const", "")
	ty = ty.replace("inline", "")
	ty = ty.replace("static", "")
	ty = ty.replace("virtual", "")
	ty = ty.replace("&", "")
	ty = re.sub(r'^.*\sint\s*$', 'int', ty) # eg "unsigned int"
	ty = re.sub(r'^.*\schar\s*$', 'char', ty) # eg "unsigned int"
	ty = re.sub(r'^.*\slong\s*$', 'int', ty)
	ty = re.sub(r'^.*\swchar_t\s*$', 'int', ty)
	ty = re.sub(r'^.*\sshort\s*$', 'int', ty)
	ty = re.sub(r'^.*\sfloat\s*$', 'Number', ty)
	ty = re.sub(r'^.*\sdouble\s*$', 'Number', ty) # eg "long double"
	ty = ty.replace("unsigned", "int")
	ty = ty.replace("long", "int")
	ty = ty.replace("float", "Number")
	ty = ty.replace("double", "Number")
	ty = ty.replace(" ", "") # Not very safe!
	return ty

class LuaBindings(object):

	def __init__(self):
		super(LuaBindings, self).__init__()

		# Write out global files
		mkdir_p(self.includePath)
		mkdir_p(self.apiPath)
		mkdir_p(self.sourcePath)

		self.cppRegisterHeaderOut = open(os.path.join(self.luaDocPath,  self.prefix), 'w')  # Def: Global C++ *LUA.h
		self.luaIndexOut          = open(os.path.join(self.apiPath,     self.prefix), 'w')  # Def: Global Lua everything-gets-required-from-this file
		self.wrappersHeaderOut    = open(os.path.join(self.includePath, self.prefix), 'w')  # Def: Global C++ *LUAWrappers.h
		self.cppRegisterOut       = open(os.path.join(self.sourcePath,  self.prefix), 'w')  # Def: Global C++ *LUA.cpp

		self.luaDocOut = StringIO()
		self.cppLoaderOut = StringIO()  # Def: Global C++ *LUA.cpp


			# fout = open("%s/%s.lua" % (apiClassPath, ckey), "w")

	def main(self, argp=None):

		if argp is None:
			argp = ARGP.parse_args()

		self.argp = argp

		self.inputPath            = argp.input_path
		self.prefix               = argp.prefix
		self.mainInclude          = argp.main_include
		self.libSmallName         = argp.lib_small_name
		self.libName              = argp.lib_name
		self.apiPath              = argp.api_path
		self.apiClassPath         = argp.api_class_path
		self.includePath          = argp.include_path
		self.sourcePath           = argp.source_path
		self.luaDocPath           = argp.lua_doc_path
		self.inheritInModuleFiles = argp.inherit_in_module_file_path

		createLUABindings(
			self.inputPath,
			self.prefix,
			self.mainInclude,
			self.libSmallName,
			self.libName,
			self.apiPath,
			self.apiClassPath,
			self.includePath,
			self.sourcePath,
			self.luaDocPath,
			self.inheritInModuleFiles,
		)


def createLUABindings(inputPath, prefix, mainInclude, libSmallName, libName, apiPath, apiClassPath, includePath, sourcePath, luaDocPath, inheritInModuleFiles):


	# Header boilerplate for wrappersHeaderOut and cppRegisterOut
	cppRegisterOut.write("#include \"%sLUA.h\"\n" % (prefix))
	cppRegisterOut.write("#include \"%sLUAWrappers.h\"\n" % (prefix))
	cppRegisterOut.write("#include \"PolyCoreServices.h\"\n\n")
	cppRegisterOut.write("using namespace Polycode;\n\n")
	cppRegisterOut.write("int luaopen_%s(lua_State *L) {\n" % (prefix))

	if prefix != "Polycode" and prefix != "Physics2D" and prefix != "Physics3D" and prefix != "UI":
		cppRegisterOut.write("CoreServices *inst = (CoreServices*) *((PolyBase**)lua_touserdata(L, 1));\n")
		cppRegisterOut.write("CoreServices::setInstance(inst);\n")
	cppRegisterOut.write("\tstatic const struct luaL_reg %sLib [] = {" % (libSmallName))

	self.wrappersHeaderOut.write("#pragma once\n\n")

	self.wrappersHeaderOut.write("extern \"C\" {\n\n")
	self.wrappersHeaderOut.write("#include <stdio.h>\n")
	self.wrappersHeaderOut.write("#include \"lua.h\"\n")
	self.wrappersHeaderOut.write("#include \"lualib.h\"\n")
	self.wrappersHeaderOut.write("#include \"lauxlib.h\"\n")
	self.wrappersHeaderOut.write("#undef near\n")
	self.wrappersHeaderOut.write("#undef far\n")
	self.wrappersHeaderOut.write("} // extern \"C\" \n\n")

	self.luaDocOut.write("<?xml version=\"1.0\" ?>\n")
	self.luaDocOut.write("<docs>\n")
	self.luaDocOut.write("<classes>\n")


	# Get list of headers to create bindings from
	inputPathIsDir = os.path.isdir(inputPath)
	if inputPathIsDir:
		files = os.listdir(inputPath)
	else:
		files = []
		with open(inputPath) as f:
			for line in f.readlines():
				files.append(line.strip()) # Strip whitespace, path/
	filteredFiles = []
	for fileName in files:
		if inputPathIsDir:
			fileName = "%s/%s" % (inputPath, fileName)
		if os.path.isdir(fileName):
			continue
		head, tail = os.path.split(fileName)
		ignore = ["PolyTween", "PolyTweenManager", "PolyGLSLProgram", "PolyGLSLShader", "PolyGLSLShaderModule", "PolyWinCore", "PolyCocoaCore", "PolyAGLCore", "PolySDLCore", "Poly_iPhone", "PolyGLES1Renderer", "PolyGLRenderer", "tinyxml", "tinystr", "OpenGLCubemap", "PolyiPhoneCore", "PolyGLES1Texture", "PolyGLTexture", "PolyGLVertexBuffer", "PolyThreaded", "PolyGLHeaders", "GLee", "PolyPeer", "PolySocket", "PolyClient", "PolyServer", "PolyServerWorld", "OSFILE", "OSFileEntry", "OSBasics", "PolyLogger", "PolyFontGlyphSheet"]
		if tail.split(".")[1] == "h" and tail.split(".")[0] not in ignore:
			filteredFiles.append(fileName)
			self.wrappersHeaderOut.write("#include \"%s\"\n" % (tail))

	self.wrappersHeaderOut.write("\nusing namespace std;\n\n")
	self.wrappersHeaderOut.write("\nnamespace Polycode {\n\n")


	# list of classes that don't get the garbage collection in their meta table

	disable_gc = ["Entity","SceneLabel", "SceneMesh", "Scene", "Texture", "Image", "Camera", "SceneParticleEmitter", "Mesh", "Vertex", "Polygon", "Polycode::Polygon", "Material", "ScenePrimitive", "SceneLine", "SceneLight", "SceneSound", "SceneImage", "SceneEntity", "SceneEntityInstance", "SceneSprite"]

	# Special case: If we are building the Polycode library itself, inject the LuaEventHandler class.
	# Note: so that event callbacks can work, any object inheriting from EventHandler will secretly
	# be modified to actually inherit from LuaEventHandler instead.
	if prefix == "Polycode":
		self.wrappersHeaderOut.write("class LuaEventHandler : public EventHandler {\n")
		self.wrappersHeaderOut.write("public:\n")
		self.wrappersHeaderOut.write("	LuaEventHandler() : EventHandler() {}\n")
		self.wrappersHeaderOut.write("	void handleEvent(Event *e) {\n")
		self.wrappersHeaderOut.write("		lua_getfield (L, LUA_GLOBALSINDEX, \"__customError\");\n")
		self.wrappersHeaderOut.write("		int errH = lua_gettop(L);\n")
		self.wrappersHeaderOut.write("		lua_getfield(L, LUA_GLOBALSINDEX, \"__handleEvent\");\n")
		self.wrappersHeaderOut.write("		lua_rawgeti( L, LUA_REGISTRYINDEX, wrapperIndex );\n")
		self.wrappersHeaderOut.write("		PolyBase **userdataPtr = (PolyBase**)lua_newuserdata(L, sizeof(PolyBase*));\n")
		self.wrappersHeaderOut.write("		*userdataPtr = (PolyBase*)e;\n")
		self.wrappersHeaderOut.write("		lua_pcall(L, 2, 0, errH);\n")
		self.wrappersHeaderOut.write("		lua_settop(L, 0);\n")
		self.wrappersHeaderOut.write("	}\n")
		self.wrappersHeaderOut.write("	int wrapperIndex;\n")
		self.wrappersHeaderOut.write("	lua_State *L;\n")
		self.wrappersHeaderOut.write("};\n\n")

	# Iterate, process each input file
	for fileName in filteredFiles:
		# "Package owned" classes that ship with Polycode
		inheritInModule = ["PhysicsEntity", "CollisionScene", "CollisionEntity", "UIElement", "UIWindow", "UIMenuItem", "UIImage", "UIRect"]

		# A file or comma-separated list of files can be given to specify classes which are "package owned"
		# and should not be inherited out of Polycode/. The files should contain one class name per line,
		# and the class name may be prefixed with a path (which will be ignored).
		if inheritInModuleFiles:
			for moduleFileName in inheritInModuleFiles.split(","):
				with open(moduleFileName) as f:
					for line in f.readlines():
						inheritInModule.append(line.strip().split("/",1)[-1]) # Strip whitespace, path/

		print("Parsing %s" % fileName)
		try: # One input file parse.
			f = open(fileName) # Def: Input file handle
			contents = f.read().replace("_PolyExport", "") # Def: Input file contents, strip out "_PolyExport"
			cppHeader = CppHeaderParser.CppHeader(contents, "string") # Def: Input file contents, parsed structure
			ignore_classes = ["PolycodeShaderModule", "Object", "Threaded", "OpenGLCubemap", "PolyBase", "Matrix4::union "]

			# Iterate, check each class in this file.
			for ckey in cppHeader.classes:
				print(">> Parsing class %s" % ckey)
				c = cppHeader.classes[ckey] # Def: The class structure

				luaClassBindingOut = "" # Def: The local lua file to generate for this class.
				inherits = False
				parentClass = ""
				if len(c["inherits"]) > 0: # Does this class have parents?
					if c["inherits"][0]["class"] not in ignore_classes:

						if c["inherits"][0]["class"] in inheritInModule: # Parent class is in this module
							luaClassBindingOut += "require \"%s/%s\"\n\n" % (prefix, c["inherits"][0]["class"])
						else: # Parent class is in Polycore
							luaClassBindingOut += "require \"Polycode/%s\"\n\n" % (c["inherits"][0]["class"])

						luaClassBindingOut += "class \"%s\" (%s)\n\n" % (ckey, c["inherits"][0]["class"])
						parentClass = c["inherits"][0]["class"]
						inherits = True
				if inherits == False: # Class does not have parents
					luaClassBindingOut += "class \"%s\"\n\n" % ckey

				if ckey in ignore_classes:
					print("INGORING class %s" % ckey)
					continue

				#if len(c["methods"]["public"]) < 2: # Used to, this was a continue.
				#	print("Warning: Lua-binding class with less than two methods")
				#	continue # FIXME: Remove this, move any non-compileable classes into ignore_classes

				extendString = ""
				if len(c["inherits"]) > 0:
					if c["inherits"][0]["class"] != "PolyBase":
						extendString = " extends=\"%s\"" % (c["inherits"][0]["class"])

				self.luaDocOut.write("\t<class name=\"%s\"%s>\n" % (ckey, extendString))

				if 'doxygen' in c:
					self.luaDocOut.write("\t\t<desc><![CDATA[%s]]></desc>\n" % (cleanDocs(c['doxygen'])))

				if ckey in disable_gc:
					self.luaDocOut.write("\t\t<class_notes>NOTE: %s instances are not automatically garbage collected.</class_notes>\n" % (ckey))

				parsed_methods = [] # Def: List of discovered methods
				ignore_methods = ["readByte32", "readByte16", "getCustomEntitiesByType", "Core", "Renderer", "Shader", "Texture", "handleEvent", "secondaryHandler", "getSTLString", "readInt"]
				luaClassBindingOut += "\n\n"

				self.luaDocOut.write("\t\t<static_members>\n")
				classProperties = [] # Def: List of found property structures ("properties" meaning "data members")
				for pp in c["properties"]["public"]:
					pp["type"] = pp["type"].replace("Polycode::", "")
					pp["type"] = pp["type"].replace("std::", "")
					if pp["type"].find("POLYIGNORE") != -1:
						continue
					if pp["type"].find("static ") != -1: # If static. FIXME: Static doesn't work?
						if "defaltValue" in pp: # FIXME: defaltValue is misspelled.
							defaltValue = pp["defaltValue"]

							# The "Default Value" is more or less a literal C++ string. This causes a problem:
							# Frequently we say static const int A = 1; static const int B = A + 1.
							# Put in a one-off hack to ensure namespacing works in this special case.
							if re.match(r'\s*[a-zA-Z_][a-zA-Z0-9_]*\s*\+', defaltValue):
								defaltValue = "%s.%s" % (ckey, defaltValue)

							luaClassBindingOut += "%s.%s = %s\n" % (ckey, pp["name"], defaltValue)
							self.luaDocOut.write("\t\t\t<static_member name=\"%s\" type=\"%s\" value=\"%s\">\n" % (pp["name"],  toLuaType(typeFilter(pp[)"type"])), pp["defaltValue"])
							if 'doxygen' in pp:
								self.luaDocOut.write("\t\t\t\t<desc><![CDATA[%s]]></desc>\n" % (cleanDocs(pp['doxygen'])))
							self.luaDocOut.write("\t\t\t</static_member>\n")
					else: # FIXME: Nonstatic method ? variable ?? found.
						#there are some bugs in the class parser that cause it to return junk
						if pp["type"].find("vector") == -1 and pp["name"] != "setScale" and pp["name"] != "setPosition" and pp["name"] != "BUFFER_CACHE_PRECISION" and not pp["name"].isdigit():
							classProperties.append(pp)

				self.luaDocOut.write("\t\t</static_members>\n")


				# Iterate over properties, creating getters
				pidx = 0 # Def: Count of properties processed so far

				# TODO: Remove or generalize ParticleEmitter special casing. These lines are marked with #SPEC

				self.luaDocOut.write("\t\t<members>\n")

				numGetVars = 0
				if len(classProperties) > 0: # If there are properties, add index lookup to the metatable
					luaClassBindingOut += "function %s:__getvar(name)\n" % ckey
					# Iterate over property structures, creating if/else clauses for each.
					# TODO: Could a table be more appropriate for
					for pp in classProperties:
						if pp["name"] == "" or pp["array"] == 1:
							continue

						numGetVars = numGetVars + 1

						pp["type"] = typeFilter(pp["type"])
						if pidx == 0:
							luaClassBindingOut += "\tif name == \"%s\" then\n" % (pp["name"])
						else:
							luaClassBindingOut += "\telseif name == \"%s\" then\n" % (pp["name"])

						# Generate Lua side of binding:

						# If type is a primitive such as Number/String/int/bool
						if pp["type"] == "PolyKEY" or pp["type"] == "Number" or  pp["type"] == "String" or pp["type"] == "int" or pp["type"] == "bool":
							luaClassBindingOut += "\t\treturn %s.%s_get_%s(self.__ptr)\n" % (libName, ckey, pp["name"])

						# If type is a particle emitter, specifically #SPEC
						elif (ckey == "ScreenParticleEmitter" or ckey == "SceneParticleEmitter") and pp["name"] == "emitter":
							luaClassBindingOut += "\t\tlocal ret = %s(\"__skip_ptr__\")\n" % (pp["type"])
							luaClassBindingOut += "\t\tret.__ptr = self.__ptr\n"
							luaClassBindingOut += "\t\treturn ret\n"

						# If type is a class
						else:
							luaClassBindingOut += "\t\tlocal retVal = %s.%s_get_%s(self.__ptr)\n" % (libName, ckey, pp["name"])
							luaClassBindingOut += LuaBlocks.PtrLookup("\t\t", pp["type"], "retVal")


						self.luaDocOut.write("\t\t\t<member name=\"%s\" type=\"%s\">\n" % (pp["name"],  toLuaType(typeFilter(pp["type"]))))
						if 'doxygen' in pp:
							self.luaDocOut.write("\t\t\t\t<desc><![CDATA[%s]]></desc>\n" % (cleanDocs(pp['doxygen'])))

						self.luaDocOut.write("\t\t\t</member>\n")

						# Generate C++ side of binding:
						if not ((ckey == "ScreenParticleEmitter" or ckey == "SceneParticleEmitter") and pp["name"] == "emitter"): #SPEC
							cppRegisterOut.write("\t\t{\"%s_get_%s\", %s_%s_get_%s},\n" % (ckey, pp["name"], libName, ckey, pp["name"]))
							self.wrappersHeaderOut.write("static int %s_%s_get_%s(lua_State *L) {\n" % (libName, ckey, pp["name"]))
							self.wrappersHeaderOut.write("\tluaL_checktype(L, 1, LUA_TUSERDATA);\n")
							self.wrappersHeaderOut.write("\t%s *inst = (%s*) *((PolyBase**)lua_touserdata(L, 1));\n" % (ckey, ckey))

							outfunc = "this_shouldnt_happen"
							retFunc = ""
							if pp["type"] == "Number":
								outfunc = "lua_pushnumber"
							if pp["type"] == "String":
								outfunc = "lua_pushstring"
								retFunc = ".c_str()"
							if pp["type"] == "int" or pp["type"] == "PolyKEY":
								outfunc = "lua_pushinteger"
							if pp["type"] == "bool":
								outfunc = "lua_pushboolean"

							if pp["type"] == "Number" or  pp["type"] == "String" or pp["type"] == "int" or pp["type"] == "bool" or pp["type"] == "PolyKEY":
								self.wrappersHeaderOut.write("\t%s(L, inst->%s%s);\n" % (outfunc, pp["name"], retFunc))
							else:
								if pp["type"].find("*") != -1:
									self.wrappersHeaderOut.write("\tif(!inst->%s%s) {\n" % (pp["name"], retFunc))
									self.wrappersHeaderOut.write("\t\tlua_pushnil(L);\n")
									self.wrappersHeaderOut.write("\t} else {\n")
									self.wrappersHeaderOut.write("\t\tPolyBase **userdataPtr = (PolyBase**)lua_newuserdata(L, sizeof(PolyBase*));\n")
									self.wrappersHeaderOut.write("\t\t*userdataPtr = (PolyBase*)inst->%s%s;\n" % (pp["name"], retFunc))
									self.wrappersHeaderOut.write("\t}\n")
								else:
									self.wrappersHeaderOut.write("\tPolyBase **userdataPtr = (PolyBase**)lua_newuserdata(L, sizeof(PolyBase*));\n")
									self.wrappersHeaderOut.write("\t*userdataPtr = (PolyBase*)&inst->%s%s;\n" % (pp["name"], retFunc))
							self.wrappersHeaderOut.write("\treturn 1;\n")
							self.wrappersHeaderOut.write("}\n\n")

						# Success
						pidx = pidx + 1
					if numGetVars != 0:
						luaClassBindingOut += "\tend\n"
					if inherits:
						luaClassBindingOut += "\tif %s[\"__getvar\"] ~= nil then\n" % (parentClass)
						luaClassBindingOut += "\t\treturn %s.__getvar(self, name)\n" % (parentClass)
						luaClassBindingOut += "\tend\n"
					luaClassBindingOut += "end\n"

				self.luaDocOut.write("\t\t</members>\n")

				luaClassBindingOut += "\n\n"

				# Iterate over properties again, creating setters
				pidx = 0 # Def: Count of
				if len(classProperties) > 0: # If there are properties, add index setter to the metatable
					luaClassBindingOut += "function %s:__setvar(name,value)\n" % ckey
					for pp in classProperties:
						if pp["name"] == "" or pp["array"] == 1:
							continue
						pp["type"] = typeFilter(pp["type"])

						# If type is a primitive: Create lua and C++ sides at the same time.
						if pp["type"] == "Number" or  pp["type"] == "String" or pp["type"] == "int" or pp["type"] == "bool" or pp["type"] == "PolyKEY":
							if pidx == 0:
								luaClassBindingOut += "\tif name == \"%s\" then\n" % (pp["name"])
							else:
								luaClassBindingOut += "\telseif name == \"%s\" then\n" % (pp["name"])
							luaClassBindingOut += "\t\t%s.%s_set_%s(self.__ptr, value)\n" % (libName, ckey, pp["name"])
							luaClassBindingOut += "\t\treturn true\n"

							cppRegisterOut.write("\t\t{\"%s_set_%s\", %s_%s_set_%s},\n" % (ckey, pp["name"], libName, ckey, pp["name"]))
							self.wrappersHeaderOut.write("static int %s_%s_set_%s(lua_State *L) {\n" % (libName, ckey, pp["name"]))
							self.wrappersHeaderOut.write("\tluaL_checktype(L, 1, LUA_TUSERDATA);\n")
							self.wrappersHeaderOut.write("\t%s *inst = (%s*) *((PolyBase**)lua_touserdata(L, 1));\n" % (ckey, ckey))

							outfunc = "this_shouldnt_happen"
							outfuncsuffix = ""
							if pp["type"] == "Number":
								outfunc = "lua_tonumber"
							if pp["type"] == "String":
								outfunc = "lua_tostring"
							if pp["type"] == "int":
								outfunc = "lua_tointeger"
							if pp["type"] == "PolyKEY":
								outfunc = "(PolyKEY)lua_tointeger"
							if pp["type"] == "bool":
								outfunc = "lua_toboolean"
								outfuncsuffix = " != 0"

							self.wrappersHeaderOut.write("\t%s param = %s(L, 2)%s;\n" % (pp["type"], outfunc, outfuncsuffix))
							self.wrappersHeaderOut.write("\tinst->%s = param;\n" % (pp["name"]))

							self.wrappersHeaderOut.write("\treturn 0;\n")
							self.wrappersHeaderOut.write("}\n\n")
							pidx = pidx + 1 # Success
						else:
							if pp["type"].find("*") == -1 and pp["type"].find("static") == -1:
								if pidx == 0:
									luaClassBindingOut += "\tif name == \"%s\" then\n" % (pp["name"])
								else:
									luaClassBindingOut += "\telseif name == \"%s\" then\n" % (pp["name"])
								luaClassBindingOut += "\t\t%s.%s_set_%s(self.__ptr, value.__ptr)\n" % (libName, ckey, pp["name"])
								luaClassBindingOut += "\t\treturn true\n"

								cppRegisterOut.write("\t\t{\"%s_set_%s\", %s_%s_set_%s},\n" % (ckey, pp["name"], libName, ckey, pp["name"]))
								self.wrappersHeaderOut.write("static int %s_%s_set_%s(lua_State *L) {\n" % (libName, ckey, pp["name"]))
								self.wrappersHeaderOut.write("\tluaL_checktype(L, 1, LUA_TUSERDATA);\n")
								self.wrappersHeaderOut.write("\t%s *inst = (%s*) *((PolyBase**)lua_touserdata(L, 1));\n" % (ckey, ckey))
								self.wrappersHeaderOut.write("\tluaL_checktype(L, 2, LUA_TUSERDATA);\n")
								self.wrappersHeaderOut.write("\t%s *argInst = (%s*) *((PolyBase**)lua_touserdata(L, 2));\n" % (typeFilter(pp["type"]), )typeFilter(pp["type"]))
								self.wrappersHeaderOut.write("\tinst->%s = *argInst;\n" % (pp["name"]))
								self.wrappersHeaderOut.write("\treturn 0;\n")
								self.wrappersHeaderOut.write("}\n\n")
								pidx = pidx + 1 # Success

						# Notice: Setters for object types are not created.
					if pidx != 0:
						luaClassBindingOut += "\tend\n"
					if inherits:
						luaClassBindingOut += "\tif %s[\"__setvar\"] ~= nil then\n" % (parentClass)
						luaClassBindingOut += "\t\treturn %s.__setvar(self, name, value)\n" % (parentClass)
						luaClassBindingOut += "\telse\n"
						luaClassBindingOut += "\t\treturn false\n"
						luaClassBindingOut += "\tend\n"
					else:
						luaClassBindingOut += "\treturn false\n"
					luaClassBindingOut += "end\n"

				# Iterate over methods
				luaClassBindingOut += "\n\n"

				self.luaDocOut.write("\t\t<methods>\n")

				for pm in c["methods"]["public"]:
					# Skip argument-overloaded methods and operators.
					# TODO: Instead of skipping arguemnt overloads, have special behavior.
					# TODO: Instead of skipping operators, add to metatable.
					if pm["name"] in parsed_methods or pm["name"].find("operator") > -1 or pm["rtnType"].find("POLYIGNORE") > -1 or pm["name"] in ignore_methods:
						continue

					# Skip destructors and methods which return templates.
					# TODO: Special-case certain kind of vector<>s?
					if pm["name"] == "~"+ckey or pm["name"] == "CoreServices":
						continue

					staticString = ""
					if pm["rtnType"].find("static ") != -1:
						staticString = " static=\"true\""

					if pm["rtnType"].find("std::vector") > -1:
						vectorReturnClass = pm["rtnType"].replace("std::vector<", "").replace(">","").replace(" ", "")
						self.luaDocOut.write("\t\t\t<method name=\"%s\" return_array=\"true\" return_type=\"%s\"%s>\n" % (pm["name"],  toLuaType()typeFilter(vectorReturnClass).replace("*", "")), staticString)
					else:
						self.luaDocOut.write("\t\t\t<method name=\"%s\" return_type=\"%s\"%s>\n" % (pm["name"],  toLuaType(typeFilter(pm["rtnType"].r)eplace("*", ""))), staticString)

					docs = None
					if 'doxygen' in pm:
						if pm['doxygen'].find("@return") > -1:
							docs = cleanDocs(pm['doxygen']).split("@return")[0].split("@param")
						else:
							docs = cleanDocs(pm['doxygen']).split("@param")
						self.luaDocOut.write("\t\t\t\t<desc><![CDATA[%s]]></desc>\n" % (docs[0]))

					if len(pm["parameters"]) > 0:
						self.luaDocOut.write("\t\t\t\t<params>\n")

						paramIndex = 0
						for param in pm["parameters"]:
							if "name" in param:
								if not "type" in param:
									continue
								if param["type"] == "0":
									continue
								if param["type"].find("vector<") != -1:
									vectorClass = param["type"].replace("std::vector<", "").replace(">","").replace(" ", "")
									self.luaDocOut.write("\t\t\t\t\t<param name=\"%s\" param_array=\"true\" type=\"%s\">\n" % (param["name"], toLuaType()vectorClass.replace("*","")))
								else:
									self.luaDocOut.write("\t\t\t\t\t<param name=\"%s\" type=\"%s\">\n" % (param["name"], toLuaType(typeFilter(param[")type"]).replace("*","")))
								if docs != None:
									if len(docs) > paramIndex+1:
										cdoc = docs[paramIndex+1].split()
										cdoc.pop(0)
										self.luaDocOut.write("\t\t\t\t\t\t<desc><![CDATA[%s]]></desc>\n" % (" ".join(cdoc).replace("\n", "")))
								self.luaDocOut.write("\t\t\t\t\t</param>\n")
								paramIndex = paramIndex + 1
						self.luaDocOut.write("\t\t\t\t</params>\n")


					self.luaDocOut.write("\t\t\t</method>\n")

					basicType = False
					voidRet = False
					vectorReturn = False
					vectorReturnClass = ""
					# Def: True if method takes a lua_State* as argument (i.e.: no preprocessing by us)
					rawMethod = len(pm["parameters"]) > 0 and pm["parameters"][0].get("type","").find("lua_State") > -1

					# Basic setup, C++ side: Add function to registry and start building wrapper function.
					if pm["name"] == ckey: # It's a constructor
						cppRegisterOut.write("\t\t{\"%s\", %s_%s},\n" % (ckey, libName, ckey))
						self.wrappersHeaderOut.write("static int %s_%s(lua_State *L) {\n" % (libName, ckey))
						idx = 1 # Def: Current stack depth (TODO: Figure out, is this correct?)
					else: # It's not a constructor
						cppRegisterOut.write("\t\t{\"%s_%s\", %s_%s_%s},\n" % (ckey, pm["name"], libName, ckey, pm["name"]))
						self.wrappersHeaderOut.write("static int %s_%s_%s(lua_State *L) {\n" % (libName, ckey, pm["name"]))

						# Skip static methods (TODO: Figure out, why is this being done here?). # FIXME
						if pm["rtnType"].find("static ") == -1:
							self.wrappersHeaderOut.write("\tluaL_checktype(L, 1, LUA_TUSERDATA);\n")
							self.wrappersHeaderOut.write("\t%s *inst = (%s*) *((PolyBase**)lua_touserdata(L, 1));\n" % (ckey, ckey))
							idx = 2
						else:
							idx = 1

					if rawMethod:
						self.wrappersHeaderOut.write("\treturn inst->%s(L);\n" % (pm["name"]))
					else:
						# Generate C++ side parameter pushing
						paramlist = []
						lparamlist = []
						for param in pm["parameters"]:
							if not "type" in param:
								continue
							if param["type"] == "0":
								continue

							param["type"] = typeFilter(param["type"])

							param["name"] = param["name"].replace("end", "_end").replace("repeat", "_repeat")
							if"type" in param:
								luatype = "LUA_TUSERDATA"
								checkfunc = "lua_isuserdata"
								if param["type"].find("*") > -1:
									luafunc = "(%s) *((PolyBase**)lua_touserdata" % (param["type"].replace("Polygon", "Polycode::Polygon").replace("Rectangle", "Polycode::Rectangle"))
								elif param["type"].find("&") > -1:
									luafunc = "*(%s*) *((PolyBase**)lua_touserdata" % (param["type"].replace("const", "").replace("&", "").replace("Polygon", "Polycode::Polygon").replace("Rectangle", "Polycode::Rectangle"))
								else:
									luafunc = "*(%s*) *((PolyBase**)lua_touserdata" % (param["type"].replace("Polygon", "Polycode::Polygon").replace("Rectangle", "Polycode::Rectangle"))
								lend = ".__ptr"
								luafuncsuffix = ")"
								if param["type"] == "int" or param["type"] == "unsigned int" or param["type"] == "short":
									luafunc = "lua_tointeger"
									luatype = "LUA_TNUMBER"
									checkfunc = "lua_isnumber"
									luafuncsuffix = ""
									lend = ""
								if param["type"] == "PolyKEY":
									luafunc = "(PolyKEY)lua_tointeger"
									luatype = "LUA_TNUMBER"
									checkfunc = "lua_isnumber"
									luafuncsuffix = ""
									lend = ""
								if param["type"] == "bool":
									luafunc = "lua_toboolean"
									luatype = "LUA_TBOOLEAN"
									checkfunc = "lua_isboolean"
									luafuncsuffix = " != 0"
									lend = ""
								if param["type"] == "Number" or param["type"] == "float" or param["type"] == "double":
									luatype = "LUA_TNUMBER"
									luafunc = "lua_tonumber"
									checkfunc = "lua_isnumber"
									luafuncsuffix = ""
									lend = ""
								if param["type"] == "String":
									luatype = "LUA_TSTRING"
									luafunc = "lua_tostring"
									checkfunc = "lua_isstring"
									luafuncsuffix = ""
									lend = ""

								param["type"] = param["type"].replace("Polygon", "Polycode::Polygon").replace("Rectangle", "Polycode::Rectangle")

								if "defaltValue" in param:
									if checkfunc != "lua_isuserdata" or (checkfunc == "lua_isuserdata" and param["defaltValue"] == "NULL"):
										#param["defaltValue"] = param["defaltValue"].replace(" 0f", ".0f")
										param["defaltValue"] = param["defaltValue"].replace(": :", "::")
										#param["defaltValue"] = param["defaltValue"].replace("0 ", "0.")
										param["defaltValue"] = re.sub(r'([0-9]+) ([0-9])+', r'\1.\2', param["defaltValue"])

										self.wrappersHeaderOut.write("\t%s %s;\n" % (param["type"], param["name"]))
										self.wrappersHeaderOut.write("\tif(%s(L, %d)) {\n" % (checkfunc, idx))
										self.wrappersHeaderOut.write("\t\t%s = %s(L, %d)%s;\n" % (param["name"], luafunc, idx, luafuncsuffix))
										self.wrappersHeaderOut.write("\t} else {\n")
										self.wrappersHeaderOut.write("\t\t%s = %s;\n" % (param["name"], param["defaltValue"]))
										self.wrappersHeaderOut.write("\t}\n")
									else:
										self.wrappersHeaderOut.write("\tluaL_checktype(L, %d, %s);\n" % (idx, luatype);)
										if param["type"] == "String":
											self.wrappersHeaderOut.write("\t%s %s = String(%s(L, %d));\n" % (param["type"], param["name"], luafunc, idx))
										else:
											self.wrappersHeaderOut.write("\t%s %s = %s(L, %d)%s;\n" % (param["type"], param["name"], luafunc, idx,)luafuncsuffix)
								else:
									self.wrappersHeaderOut.write("\tluaL_checktype(L, %d, %s);\n" % (idx, luatype);)
									if param["type"] == "String":
										self.wrappersHeaderOut.write("\t%s %s = String(%s(L, %d));\n" % (param["type"], param["name"], luafunc, idx))
									else:
										self.wrappersHeaderOut.write("\t%s %s = %s(L, %d)%s;\n" % (param["type"], param["name"], luafunc, idx, )luafuncsuffix)
								paramlist.append(param["name"])

								lparamlist.append(param["name"]+lend)
								idx = idx +1 # Param parse success-- mark the increased stack

						# Generate C++-side method call / generate return value
						if pm["name"] == ckey: # If constructor
							if ckey == "EventHandler": # See LuaEventHandler above
								self.wrappersHeaderOut.write("\tLuaEventHandler *inst = new LuaEventHandler();\n")
								self.wrappersHeaderOut.write("\tinst->wrapperIndex = luaL_ref(L, LUA_REGISTRYINDEX );\n")
								self.wrappersHeaderOut.write("\tinst->L = L;\n")
							else:
								self.wrappersHeaderOut.write("\t%s *inst = new %s(%s);\n" % (ckey, ckey, ", ".join(paramlist)))

							self.wrappersHeaderOut.write("\tPolyBase **userdataPtr = (PolyBase**)lua_newuserdata(L, sizeof(PolyBase*));\n")
							self.wrappersHeaderOut.write("\t*userdataPtr = (PolyBase*)inst;\n")
							self.wrappersHeaderOut.write("\tluaL_getmetatable(L, \"%s.%s\");\n" % (libName, ckey))
							self.wrappersHeaderOut.write("\tlua_setmetatable(L, -2);\n")
							self.wrappersHeaderOut.write("\treturn 1;\n")
						else: #If non-constructor
							if pm["rtnType"].find("static ") == -1: # If non-static
								call = "inst->%s(%s)" % (pm["name"], ", ".join(paramlist))
							else: # If static (FIXME: Why doesn't this work?)
								call = "%s::%s(%s)" % (ckey, pm["name"], ", ".join(paramlist))

							#check if returning a template
							if pm["rtnType"].find("<") > -1:
								#if returning a vector, convert to lua table
								if pm["rtnType"].find("std::vector") > -1:
									vectorReturnClass = pm["rtnType"].replace("std::vector<", "").replace(">","").replace(" ", "")
									if vectorReturnClass.find("&") == -1 and vectorReturnClass.find("*") > -1: #FIXME: return references to std::vectors and basic types
										vectorReturn = True
										self.wrappersHeaderOut.write("\tstd::vector<%s> retVector = %s;\n" % (vectorReturnClass,call))
										self.wrappersHeaderOut.write("\tlua_newtable(L);\n")
										self.wrappersHeaderOut.write("\tfor(int i=0; i < retVector.size(); i++) {\n")
										self.wrappersHeaderOut.write("\t\tPolyBase **userdataPtr = (PolyBase**)lua_newuserdata(L, sizeof(PolyBase*));\n")
										self.wrappersHeaderOut.write("\t\t*userdataPtr = (PolyBase*)retVector[i];\n")
										self.wrappersHeaderOut.write("\t\tlua_rawseti(L, -2, i+1);\n")
										self.wrappersHeaderOut.write("\t}\n")
										self.wrappersHeaderOut.write("\treturn 1;\n")
									else:
										self.wrappersHeaderOut.write("\treturn 0;\n")

							# else If void-typed:
							elif pm["rtnType"] == "void" or pm["rtnType"] == "static void" or pm["rtnType"] == "virtual void" or pm["rtnType"] == "inline void":
								self.wrappersHeaderOut.write("\t%s;\n" % (call))
								basicType = True
								voidRet = True
								vectorReturn = False
								self.wrappersHeaderOut.write("\treturn 0;\n" # 0 arguments returned)
							else: # If there is a return value:
								# What type is the return value? Default to pointer
								outfunc = "this_shouldnt_happen"
								retFunc = ""
								basicType = False
								vectorReturn = False
								if pm["rtnType"] == "Number" or  pm["rtnType"] == "inline Number":
									outfunc = "lua_pushnumber"
									basicType = True
								if pm["rtnType"] == "String" or pm["rtnType"] == "static String": # TODO: Path for STL strings?
									outfunc = "lua_pushstring"
									basicType = True
									retFunc = ".c_str()"
								if pm["rtnType"] == "int" or pm["rtnType"] == "unsigned int" or pm["rtnType"] == "static int" or  pm["rtnType"] == "size_t" or pm["rtnType"] == "static size_t" or pm["rtnType"] == "long" or pm["rtnType"] == "unsigned int" or pm["rtnType"] == "static long" or pm["rtnType"] == "short" or pm["rtnType"] == "PolyKEY" or pm["rtnType"] == "wchar_t":
									outfunc = "lua_pushinteger"
									basicType = True
								if pm["rtnType"] == "bool" or pm["rtnType"] == "static bool" or pm["rtnType"] == "virtual bool":
									outfunc = "lua_pushboolean"
									basicType = True

								if pm["rtnType"].find("*") > -1: # Returned var is definitely a pointer.
									self.wrappersHeaderOut.write("\tPolyBase *ptrRetVal = (PolyBase*)%s%s;\n" % (call, retFunc))
									self.wrappersHeaderOut.write("\tif(ptrRetVal == NULL) {\n")
									self.wrappersHeaderOut.write("\t\tlua_pushnil(L);\n")
									self.wrappersHeaderOut.write("\t} else {\n")
									self.wrappersHeaderOut.write("\t\tPolyBase **userdataPtr = (PolyBase**)lua_newuserdata(L, sizeof(PolyBase*));\n")
									self.wrappersHeaderOut.write("\t\t*userdataPtr = ptrRetVal;\n")
									self.wrappersHeaderOut.write("\t}\n")
								elif basicType == True: # Returned var has been flagged as a recognized primitive type
									self.wrappersHeaderOut.write("\t%s(L, %s%s);\n" % (outfunc, call, retFunc))
								else: # Some static object is being returned. Convert it to a pointer, then return that.
									className = pm["rtnType"].replace("const", "").replace("&", "").replace("inline", "").replace("virtual", "").replace("static", "")
									if className == "Polygon": # Deal with potential windows.h conflict
										className = "Polycode::Polygon"
									if className == "Rectangle":
										className = "Polycode::Rectangle"
									if className == "Polycode : : Rectangle":
										className = "Polycode::Rectangle"
									self.wrappersHeaderOut.write("\t%s *retInst = new %s();\n" % (className, className))
									self.wrappersHeaderOut.write("\t*retInst = %s;\n" % (call))
									self.wrappersHeaderOut.write("\tPolyBase **userdataPtr = (PolyBase**)lua_newuserdata(L, sizeof(PolyBase*));\n")
									self.wrappersHeaderOut.write("\tluaL_getmetatable(L, \"%s.%s\");\n" % (libName, className))
									self.wrappersHeaderOut.write("\tlua_setmetatable(L, -2);\n")
									self.wrappersHeaderOut.write("\t*userdataPtr = (PolyBase*)retInst;\n")
								self.wrappersHeaderOut.write("\treturn 1;\n")
					self.wrappersHeaderOut.write("}\n\n" # Close out C++ generation)

					# Now generate the Lua side method.
					if rawMethod:
						luaClassBindingOut += "function %s:%s(...)\n" % (ckey, pm["name"])
						luaClassBindingOut += "\treturn %s.%s_%s(self.__ptr, ...)\n" % (libName, ckey, pm["name"])
						luaClassBindingOut += "end\n"
					elif pm["name"] == ckey: # Constructors
						luaClassBindingOut += "function %s:%s(...)\n" % (ckey, ckey)
						luaClassBindingOut += "\tlocal arg = {...}\n"
						if inherits:
							luaClassBindingOut += "\tif type(arg[1]) == \"table\" and count(arg) == 1 then\n"
							luaClassBindingOut += "\t\tif \"\"..arg[1].__classname == \"%s\" then\n" % (c["inherits"][0]["class"])
							luaClassBindingOut += "\t\t\tself.__ptr = arg[1].__ptr\n"
							luaClassBindingOut += "\t\t\treturn\n"
							luaClassBindingOut += "\t\tend\n"
							luaClassBindingOut += "\tend\n"
						luaClassBindingOut += "\tfor k,v in pairs(arg) do\n"
						luaClassBindingOut += "\t\tif type(v) == \"table\" then\n"
						luaClassBindingOut += "\t\t\tif v.__ptr ~= nil then\n"
						luaClassBindingOut += "\t\t\t\targ[k] = v.__ptr\n"
						luaClassBindingOut += "\t\t\tend\n"
						luaClassBindingOut += "\t\tend\n"
						luaClassBindingOut += "\tend\n"
						luaClassBindingOut += "\tif self.__ptr == nil and arg[1] ~= \"__skip_ptr__\" then\n"
						if ckey == "EventHandler": # See LuaEventHandler above
							luaClassBindingOut += "\t\tself.__ptr = %s.%s(self)\n" % (libName, ckey)
						else:
							luaClassBindingOut += "\t\tself.__ptr = %s.%s(unpack(arg))\n" % (libName, ckey)
						luaClassBindingOut += "\tend\n"
						luaClassBindingOut += "end\n\n"
					else: # Non-constructors.
						if pm["rtnType"].find("static ") == -1: # Non-static method
							luaClassBindingOut += "function %s:%s(%s)\n" % (ckey, pm["name"], ", ".join(paramlist))
							if len(lparamlist):
								luaClassBindingOut += "\tlocal retVal = %s.%s_%s(self.__ptr, %s)\n" % (libName, ckey, pm["name"], ", ".join(lparamlist))
							else:
								luaClassBindingOut += "\tlocal retVal =  %s.%s_%s(self.__ptr)\n" % (libName, ckey, pm["name"])
						else: # Static method
							luaClassBindingOut += "function %s.%s(%s)\n" % (ckey, pm["name"], ", ".join(paramlist))
							if len(lparamlist):
								luaClassBindingOut += "\tlocal retVal = %s.%s_%s(%s)\n" % (libName, ckey, pm["name"], ", ".join(lparamlist))
							else:
								luaClassBindingOut += "\tlocal retVal =  %s.%s_%s()\n" % (libName, ckey, pm["name"])

						if not voidRet: # Was there a return value?
							if basicType == True: # Yes, a primitive
								luaClassBindingOut += "\treturn retVal\n"
							else: # Yes, a pointer was returned
								if vectorReturn == True:
									className = vectorReturnClass.replace("*", "")
									luaClassBindingOut += LuaBlocks.PtrLookupArray("\t",className,"retVal")
								else:
									className = pm["rtnType"].replace("const", "").replace("&", "").replace("inline", "").replace("virtual", "").replace("static", "").replace("*","").replace(" ", "")
									luaClassBindingOut += LuaBlocks.PtrLookup("\t",className,"retVal")
						luaClassBindingOut += "end\n\n" # Close out Lua generation

					parsed_methods.append(pm["name"]) # Method parse success

				self.luaDocOut.write("\t\t</methods>\n")

				# With methods out of the way, do some final cleanup:

				# user pointer metatable creation in C++
				self.cppLoaderOut.write("\n\tluaL_newmetatable(L, \"%s.%s\");\n" % (libName, ckey))
				if ckey not in disable_gc:
					self.cppLoaderOut.write("\tlua_pushstring(L, \"__gc\");\n")
					self.cppLoaderOut.write("\tlua_pushcfunction(L, %s_delete_%s);\n" % (libName, ckey))
					self.cppLoaderOut.write("\tlua_settable(L, -3);\n")
				self.cppLoaderOut.write("\tlua_pop(L, 1);\n")

				# Delete method (C++ side)
				cppRegisterOut.write("\t\t{\"delete_%s\", %s_delete_%s},\n" % (ckey, libName, ckey))
				self.wrappersHeaderOut.write("static int %s_delete_%s(lua_State *L) {\n" % (libName, ckey))
				self.wrappersHeaderOut.write("\tluaL_checktype(L, 1, LUA_TUSERDATA);\n")
				self.wrappersHeaderOut.write("\tPolyBase **inst = (PolyBase**)lua_touserdata(L, 1);\n")
				self.wrappersHeaderOut.write("\tdelete ((%s*) *inst);\n" % (ckey))
				self.wrappersHeaderOut.write("\t*inst = NULL;\n")
				self.wrappersHeaderOut.write("\treturn 0;\n")
				self.wrappersHeaderOut.write("}\n\n")

				# Delete method (Lua side)
				luaClassBindingOut += "function %s:__delete()\n" % (ckey)
				luaClassBindingOut += "\tif self then %s.delete_%s(self.__ptr) end\n" % (libName, ckey)
				luaClassBindingOut += "end\n"

				# Add class to lua index file
				self.luaIndexOut.write("require \"%s/%s\"\n" % (prefix, ckey))
				# Write lua file
				mkdir_p(apiClassPath)
				if ckey != "EventDispatcher":
					fout = open("%s/%s.lua" % (apiClassPath, ckey), "w")
					fout.write(luaClassBindingOut)

				self.luaDocOut.write("\t</class>\n")

		except CppHeaderParser.CppParseError as e: # One input file parse; failed.
			print(e)
			sys.exit(1)

	self.luaDocOut.write("</classes>\n")
	self.luaDocOut.write("</docs>\n")

	# Footer boilerplate for wrappersHeaderOut and cppRegisterOut.
	self.wrappersHeaderOut.write("} // namespace Polycode\n")

	cppRegisterOut.write("\t\t{NULL, NULL}\n")
	cppRegisterOut.write("\t};\n")
	cppRegisterOut.write("\tluaL_openlib(L, \"%s\", %sLib, 0);\n" % (libName, libSmallName))
	cppRegisterOut.write(self.cppLoaderOut.getvalue())
	cppRegisterOut.write("\treturn 1;\n")
	cppRegisterOut.write("}")


	self.cppRegisterHeaderOut.write("#pragma once\n")
	self.cppRegisterHeaderOut.write("#include <%s>\n" % (mainInclude))
	self.cppRegisterHeaderOut.write("extern \"C\" {\n")
	self.cppRegisterHeaderOut.write("#include <stdio.h>\n")
	self.cppRegisterHeaderOut.write("#include \"lua.h\"\n")
	self.cppRegisterHeaderOut.write("#include \"lualib.h\"\n")
	self.cppRegisterHeaderOut.write("#include \"lauxlib.h\"\n")
	self.cppRegisterHeaderOut.write("int _PolyExport luaopen_%s(lua_State *L);\n" % (prefix))
	self.cppRegisterHeaderOut.write("}\n")

	self.cppRegisterHeaderOut.close()
	self.luaIndexOut.close()
	self.wrappersHeaderOut.close()
	self.cppRegisterOut.close()

	self.luaDocOut.close()
	if self.luaDocPath is None:
		self.luaDocPath = os.path.join("../../../Documentation/Lua/xml", self.prefix)
	if self.luaDocPath != "-":
		self.luaDocPath = os.path.join(self.luaDocPath, self.prefix)
	else
		self.luaDocPath = os.path.join(self.includePath, self.prefix)

	with open(self.luaDocPath) as file_handle:
		file_handle.write(self.luaDocOut.getvalue())

	# Create .pak zip archive
	pattern = '*.lua'
	os.chdir(apiPath)
	if libName == "Polycore":
		with ZipFile("api.pak", 'w') as myzip:
			for root, dirs, files in os.walk("."):
				for filename in fnmatch.filter(files, pattern):
					myzip.write(os.path.join(root, filename))
	else:
		with ZipFile("%s.pak" % (libName), 'w') as myzip:
			for root, dirs, files in os.walk("."):
				for filename in fnmatch.filter(files, pattern):
					myzip.write(os.path.join(root, filename))

if __name__ == '__main__':
	LuaBindings().main(argp)
