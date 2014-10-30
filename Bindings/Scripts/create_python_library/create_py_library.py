import sys
import CppHeaderParser
import os
import errno
import re
from zipfile import *
import fnmatch
import re
import time

def mkdir_p(path):
	"""Same effect as mkdir -p, create dir and all necessary parent dirs"""
	try:
		os.makedirs(path)
	except OSError as e:
		if e.errno == errno.EEXIST: # Dir already exists; not really an error
			pass
		else: raise

def template_returnPtrLookupArray(prefix, className, ptr):
	out = "%sif %s == None : return None\n" % (prefix, ptr)
	out += "%sfor i in range(len(%s)):\n" % (prefix, ptr)
	out += "%s\t__c  = _G[%s](\"__skip_ptr__\")\n" % (prefix, className.replace("*", ""))
	out += "%s\t__c.__ptr = %s[i]\n" % (prefix, ptr)
	out += "%s\t%s[i] = __c\n" % (prefix, ptr)
	out += "%sreturn %s\n" % (prefix,ptr)
	return out


def template_returnPtrLookup(prefix, className, ptr):
	# Note we expect className to be a valid string
	out = "%sif %s == None : return None\n" % (prefix, ptr)
	out += "%s__c = _G[%s](\"__skip_ptr__\")\n" % (prefix, className.replace("*", ""))
	out += "%s__c.__ptr = %s\n" % (prefix, ptr)
	out += "%sreturn __c\n" % (prefix)
	return out

def template_quote(str):
	return "\"%s\"" % str;

def cleanDocs(docs):
	return docs.replace("/*", "").replace("*/", "").replace("*", "").replace("\n", "").replace("\r", "").replace("::", ".").replace("\t", "")

def toPyType(t):
	return t.replace("void", "None").replace("int", "Integer").replace("bool", "Boolean").replace("*", "")

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

def createPYBindings(inputPath, prefix, mainInclude, libSmallName, libName, apiPath, apiClassPath, includePath, sourcePath, pyDocPath, inheritInModuleFiles):
	wrappersHeaderOut = "" # Def: Global C++ *PYWrappers.h
	cppRegisterOut = "" # Def: Global C++ *PY.cpp
	cppLoaderOut = "" # Def: Global C++ *PY.cpp
	pyDocOut = ""

	pyIndexOut = "" # Def: Global Py everything-gets-required-from-this-file file

	# Header boilerplate for wrappersHeaderOut and cppRegisterOut
	cppRegisterOut += "#include \"%sPY.h\"\n" % (prefix)
	cppRegisterOut += "#include \"%sPYWrappers.h\"\n" % (prefix)
	cppRegisterOut += "#include \"PolyCoreServices.h\"\n\n"
	cppRegisterOut += "using namespace Polycode;\n\n"
	cppRegisterOut += "int pyopen_%s(py_State *L) {\n" % (prefix)

	if prefix != "Polycode" and prefix != "Physics2D" and prefix != "Physics3D" and prefix != "UI":
		cppRegisterOut += "CoreServices *inst = (CoreServices*) *((PolyBase**)py_touserdata(L, 1));\n"
		cppRegisterOut += "CoreServices::setInstance(inst);\n"
	cppRegisterOut += "\tstatic const struct pyL_reg %sLib [] = {" % (libSmallName)

	wrappersHeaderOut += "#pragma once\n\n"

	wrappersHeaderOut += "extern \"C\" {\n\n"
	wrappersHeaderOut += "#include <stdio.h>\n"
	wrappersHeaderOut += "#include \"py.h\"\n"
	wrappersHeaderOut += "#include \"pylib.h\"\n"
	wrappersHeaderOut += "#include \"lauxlib.h\"\n"
	wrappersHeaderOut += "#undef near\n"
	wrappersHeaderOut += "#undef far\n"
	wrappersHeaderOut += "} // extern \"C\" \n\n"

	pyDocOut += "<?xml version=\"1.0\" ?>\n"
	pyDocOut += "<docs>\n"
	pyDocOut += "<classes>\n"


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
			fileName = os.path.join(inputPath, fileName)
		if os.path.isdir(fileName):
			continue
		head, tail = os.path.split(fileName)
		ignore = [
			"PolyTween", "PolyTweenManager", "PolyGLSLProgram", "PolyGLSLShader",
			"PolyGLSLShaderModule", "PolyWinCore", "PolyCocoaCore", "PolyAGLCore",
			"PolySDLCore", "Poly_iPhone", "PolyGLES1Renderer", "PolyGLRenderer",
			"tinyxml", "tinystr", "OpenGLCubemap", "PolyiPhoneCore",
			"PolyGLES1Texture", "PolyGLTexture", "PolyGLVertexBuffer",
			"PolyThreaded", "PolyGLHeaders", "GLee", "PolyPeer", "PolySocket",
			"PolyClient", "PolyServer", "PolyServerWorld", "OSFILE", "OSFileEntry",
			"OSBasics", "PolyLogger", "PolyFontGlyphSheet"
		]
		if tail.split(".")[1] == "h" and tail.split(".")[0] not in ignore:
			filteredFiles.append(fileName)
			wrappersHeaderOut += "#include \"%s\"\n" % (tail)

	wrappersHeaderOut += "\nusing namespace std;\n\n"
	wrappersHeaderOut += "\nnamespace Polycode {\n\n"


	# list of classes that don't get the garbage collection in their meta table

	disable_gc = [
		"Entity","SceneLabel", "SceneMesh", "Scene", "Texture", "Image", "Camera",
		"SceneParticleEmitter", "Mesh", "Vertex", "Polygon", "Polycode::Polygon",
		"Material", "ScenePrimitive", "SceneLine", "SceneLight", "SceneSound",
		"SceneImage", "SceneEntity", "SceneEntityInstance", "SceneSprite"
	]

	# Special case: If we are building the Polycode library itself, inject the PyEventHandler class.
	# Note: so that event callbacks can work, any object inheriting from EventHandler will secretly
	# be modified to actually inherit from PyEventHandler instead.
	if prefix == "Polycode":
		wrappersHeaderOut += "class PyEventHandler : public EventHandler {\n"
		wrappersHeaderOut += "public:\n"
		wrappersHeaderOut += "	PyEventHandler() : EventHandler() {}\n"
		wrappersHeaderOut += "	void handleEvent(Event *e) {\n"
		wrappersHeaderOut += "		py_getfield (L, PY_GLOBALSINDEX, \"__customError\");\n"
		wrappersHeaderOut += "		int errH = py_gettop(L);\n"
		wrappersHeaderOut += "		py_getfield(L, PY_GLOBALSINDEX, \"__handleEvent\");\n"
		wrappersHeaderOut += "		py_rawgeti( L, PY_REGISTRYINDEX, wrapperIndex );\n"
		wrappersHeaderOut += "		PolyBase **userdataPtr = (PolyBase**)py_newuserdata(L, sizeof(PolyBase*));\n"
		wrappersHeaderOut += "		*userdataPtr = (PolyBase*)e;\n"
		wrappersHeaderOut += "		py_pcall(L, 2, 0, errH);\n"
		wrappersHeaderOut += "		py_settop(L, 0);\n"
		wrappersHeaderOut += "	}\n"
		wrappersHeaderOut += "	int wrapperIndex;\n"
		wrappersHeaderOut += "	py_State *L;\n"
		wrappersHeaderOut += "};\n\n"

	# Iterate, process each input file
	for fileName in filteredFiles:
		# "Package owned" classes that ship with Polycode
		inheritInModule = [
			"PhysicsEntity", "CollisionScene", "CollisionEntity", "UIElement",
			"UIWindow", "UIMenuItem", "UIImage", "UIRect"
		]

		# A file or comma-separated list of files can be given to specify classes which are "package owned"
		# and should not be inherited out of Polycode/. The files should contain one class name per line,
		# and the class name may be prefixed with a path (which will be ignored).
		if inheritInModuleFiles:
			for moduleFileName in inheritInModuleFiles.split(","):
				with open(moduleFileName) as f:
					for line in f.readlines():
						inheritInModule.append(line.strip().split("/",1)[-1]) # Strip whitespace, path/

		# print("Parsing %s" % fileName)
		try: # One input file parse.
			f = open(fileName) # Def: Input file handle
			contents = f.read().replace("_PolyExport", "") # Def: Input file contents, strip out "_PolyExport"
			cppHeader = CppHeaderParser.CppHeader(contents, "string") # Def: Input file contents, parsed structure
			ignore_classes = [
				"PolycodeShaderModule", "Object", "Threaded", "OpenGLCubemap",
				"PolyBase", "Matrix4::union "
			]

			# Iterate, check each class in this file.
			for ckey in cppHeader.classes:
				# print(">> Parsing class %s" % ckey)
				c = cppHeader.classes[ckey] # Def: The class structure

				pyClassBindingOut = "" # Def: The local py file to generate for this class.
				inherits = False
				parentClass = ""
				if len(c["inherits"]) > 0: # Does this class have parents?
					if c["inherits"][0]["class"] not in ignore_classes:

						if c["inherits"][0]["class"] in inheritInModule:
							# Parent class is in this module
							pyClassBindingOut += "from %s.%s import %s\n\n" % (
								prefix, c["inherits"][0]["class"], c["inherits"][0]["class"]
							)
						else:
							# Parent class is in Polycore
							pyClassBindingOut += "from %s import %s\n\n" % (
								c["inherits"][0]["class"], c["inherits"][0]["class"]
							)

						pyClassBindingOut += "class %s(%s):\n\n" % (
							ckey, c["inherits"][0]["class"]
						)
						parentClass = c["inherits"][0]["class"]
						inherits = True
				if inherits == False: # Class does not have parents
					pyClassBindingOut += "class %s(object):\n\n" % ckey

				if ckey in ignore_classes:
					# print("INGORING class %s" % ckey)
					continue

				#if len(c["methods"]["public"]) < 2: # Used to, this was a continue.
					print("Warning: Py-binding class with less than two methods")
				#	continue # FIXME: Remove this, move any non-compileable classes into ignore_classes

				extendString = ""
				if len(c["inherits"]) > 0:
					if c["inherits"][0]["class"] != "PolyBase":
						extendString = " extends=\"%s\"" % (c["inherits"][0]["class"])

				pyDocOut += "\t<class name=\"%s\"%s>\n" % (ckey, extendString)

				if 'doxygen' in c:
					pyDocOut += "\t\t<desc><![CDATA[%s]]></desc>\n" % (cleanDocs(c['doxygen']))

				if ckey in disable_gc:
					pyDocOut += "\t\t<class_notes>NOTE: %s instances are not automatically garbage collected.</class_notes>\n" % (ckey)

				parsed_methods = [] # Def: List of discovered methods
				ignore_methods = ["readByte32", "readByte16", "getCustomEntitiesByType", "Core", "Renderer", "Shader", "Texture", "handleEvent", "secondaryHandler", "getSTLString", "readInt"]
				pyClassBindingOut += "\n\n"

				pyDocOut += "\t\t<static_members>\n"
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
								defaltValue = "%s" % defaltValue

							pyClassBindingOut += "\t%s = %s\n" % (pp["name"], defaltValue)
							pyDocOut += "\t\t\t<static_member name=\"%s\" type=\"%s\" value=\"%s\">\n" % (pp["name"],  toPyType(typeFilter(pp["type"])), pp["defaltValue"])
							if 'doxygen' in pp:
								pyDocOut += "\t\t\t\t<desc><![CDATA[%s]]></desc>\n" % (cleanDocs(pp['doxygen']))
							pyDocOut += "\t\t\t</static_member>\n"
					else: # FIXME: Nonstatic method ? variable ?? found.
						#there are some bugs in the class parser that cause it to return junk
						if pp["type"].find("vector") == -1 and pp["name"] != "setScale" and pp["name"] != "setPosition" and pp["name"] != "BUFFER_CACHE_PRECISION" and not pp["name"].isdigit():
							classProperties.append(pp)

				pyDocOut += "\t\t</static_members>\n"


				# Iterate over properties, creating getters
				pidx = 0 # Def: Count of properties processed so far

				# TODO: Remove or generalize ParticleEmitter special casing. These lines are marked with #SPEC

				pyDocOut += "\t\t<members>\n"

				numGetVars = 0
				if len(classProperties) > 0: # If there are properties, add index lookup to the metatable
					pyClassBindingOut += "\tdef __getattr__(self, name):\n\t\tpass\n"
					# Iterate over property structures, creating if/else clauses for each.
					# TODO: Could a table be more appropriate for
					for pp in classProperties:
						if pp["name"] == "" or pp["array"] == 1:
							continue

						numGetVars = numGetVars + 1

						pp["type"] = typeFilter(pp["type"])
						if pidx == 0:
							pyClassBindingOut += "\t\tif name == \"%s\" :\n" % (pp["name"])
						else:
							pyClassBindingOut += "\t\telif name == \"%s\" :\n" % (pp["name"])

						# Generate Py side of binding:

						# If type is a primitive such as Number/String/int/bool
						if pp["type"] == "PolyKEY" or pp["type"] == "Number" or  pp["type"] == "String" or pp["type"] == "int" or pp["type"] == "bool":
							pyClassBindingOut += "\t\t\treturn %s.%s_get_%s(self.__ptr)\n" % (libName, ckey, pp["name"])

						# If type is a particle emitter, specifically #SPEC
						elif (ckey == "ScreenParticleEmitter" or ckey == "SceneParticleEmitter") and pp["name"] == "emitter":
							pyClassBindingOut += "\t\t\tret = %s(\"__skip_ptr__\")\n" % (pp["type"])
							pyClassBindingOut += "\t\t\tret.__ptr = self.__ptr\n"
							pyClassBindingOut += "\t\t\treturn ret\n"

						# If type is a class
						else:
							pyClassBindingOut += "\t\t\tretVal = %s.%s_get_%s(self.__ptr)\n" % (libName, ckey, pp["name"])
							pyClassBindingOut += template_returnPtrLookup("\t\t\t", template_quote(pp["type"]), "retVal")


						pyDocOut += "\t\t\t\t<member name=\"%s\" type=\"%s\">\n" % (pp["name"],  toPyType(typeFilter(pp["type"])))
						if 'doxygen' in pp:
							pyDocOut += "\t\t\t\t\t<desc><![CDATA[%s]]></desc>\n" % (cleanDocs(pp['doxygen']))

						pyDocOut += "\t\t\t\t</member>\n"

						# Generate C++ side of binding:
						if not ((ckey == "ScreenParticleEmitter" or ckey == "SceneParticleEmitter") and pp["name"] == "emitter"): #SPEC
							cppRegisterOut += "\t\t{\"%s_get_%s\", %s_%s_get_%s},\n" % (ckey, pp["name"], libName, ckey, pp["name"])
							wrappersHeaderOut += "static int %s_%s_get_%s(py_State *L) {\n" % (libName, ckey, pp["name"])
							wrappersHeaderOut += "\tpyL_checktype(L, 1, PY_TUSERDATA);\n"
							wrappersHeaderOut += "\t%s *inst = (%s*) *((PolyBase**)py_touserdata(L, 1));\n" % (ckey, ckey)

							outfunc = "this_shouldnt_happen"
							retFunc = ""
							if pp["type"] == "Number":
								outfunc = "py_pushnumber"
							if pp["type"] == "String":
								outfunc = "py_pushstring"
								retFunc = ".c_str()"
							if pp["type"] == "int" or pp["type"] == "PolyKEY":
								outfunc = "py_pushinteger"
							if pp["type"] == "bool":
								outfunc = "py_pushboolean"

							if pp["type"] == "Number" or  pp["type"] == "String" or pp["type"] == "int" or pp["type"] == "bool" or pp["type"] == "PolyKEY":
								wrappersHeaderOut += "\t%s(L, inst->%s%s);\n" % (outfunc, pp["name"], retFunc)
							else:
								if pp["type"].find("*") != -1:
									wrappersHeaderOut += "\tif(!inst->%s%s) {\n" % (pp["name"], retFunc)
									wrappersHeaderOut += "\t\tpy_pushNone(L);\n"
									wrappersHeaderOut += "\t} else {\n"
									wrappersHeaderOut += "\t\tPolyBase **userdataPtr = (PolyBase**)py_newuserdata(L, sizeof(PolyBase*));\n"
									wrappersHeaderOut += "\t\t*userdataPtr = (PolyBase*)inst->%s%s;\n" % (pp["name"], retFunc)
									wrappersHeaderOut += "\t}\n"
								else:
									wrappersHeaderOut += "\tPolyBase **userdataPtr = (PolyBase**)py_newuserdata(L, sizeof(PolyBase*));\n"
									wrappersHeaderOut += "\t*userdataPtr = (PolyBase*)&inst->%s%s;\n" % (pp["name"], retFunc)
							wrappersHeaderOut += "\treturn 1;\n"
							wrappersHeaderOut += "}\n\n"

						# Success
						pidx = pidx + 1
					if inherits:
						pyClassBindingOut += "\t\treturn getattr(%s, name)\n" % (parentClass)

				pyDocOut += "\t\t</members>\n"

				pyClassBindingOut += "\n\n"

				# Iterate over properties again, creating setters
				pidx = 0 # Def: Count of
				if len(classProperties) > 0: # If there are properties, add index setter to the metatable
					pyClassBindingOut += "\tdef __setattr__(self, name, value):\n"
					for pp in classProperties:
						if pp["name"] == "" or pp["array"] == 1:
							continue
						pp["type"] = typeFilter(pp["type"])

						# If type is a primitive: Create py and C++ sides at the same time.
						if pp["type"] == "Number" or  pp["type"] == "String" or pp["type"] == "int" or pp["type"] == "bool" or pp["type"] == "PolyKEY":
							if pidx == 0:
								pyClassBindingOut += "\t\tif name == \"%s\" :\n" % (pp["name"])
							else:
								pyClassBindingOut += "\t\telif name == \"%s\" :\n" % (pp["name"])
							pyClassBindingOut += "\t\t\t%s.%s_set_%s(self.__ptr, value)\n" % (libName, ckey, pp["name"])
							pyClassBindingOut += "\t\t\treturn true\n"

							cppRegisterOut += "\t\t\t{\"%s_set_%s\", %s_%s_set_%s},\n" % (ckey, pp["name"], libName, ckey, pp["name"])
							wrappersHeaderOut += "static int %s_%s_set_%s(py_State *L) {\n" % (libName, ckey, pp["name"])
							wrappersHeaderOut += "\t\tpyL_checktype(L, 1, PY_TUSERDATA);\n"
							wrappersHeaderOut += "\t\t%s *inst = (%s*) *((PolyBase**)py_touserdata(L, 1));\n" % (ckey, ckey)

							outfunc = "this_shouldnt_happen"
							outfuncsuffix = ""
							if pp["type"] == "Number":
								outfunc = "py_tonumber"
							if pp["type"] == "String":
								outfunc = "py_tostring"
							if pp["type"] == "int":
								outfunc = "py_tointeger"
							if pp["type"] == "PolyKEY":
								outfunc = "(PolyKEY)py_tointeger"
							if pp["type"] == "bool":
								outfunc = "py_toboolean"
								outfuncsuffix = " != 0"

							wrappersHeaderOut += "\t\t%s param = %s(L, 2)%s;\n" % (pp["type"], outfunc, outfuncsuffix)
							wrappersHeaderOut += "\t\tinst->%s = param;\n" % (pp["name"])

							wrappersHeaderOut += "\t\treturn 0;\n"
							wrappersHeaderOut += "}\n\n"
							pidx = pidx + 1 # Success
						else:
							if pp["type"].find("*") == -1 and pp["type"].find("static") == -1:
								if pidx == 0:
									pyClassBindingOut += "\t\tif name == \"%s\" :\n" % (pp["name"])
								else:
									pyClassBindingOut += "\t\telif name == \"%s\" :\n" % (pp["name"])
								pyClassBindingOut += "\t\t\t%s.%s_set_%s(self.__ptr, value.__ptr)\n" % (libName, ckey, pp["name"])
								pyClassBindingOut += "\t\t\treturn true\n"

								cppRegisterOut += "\t\t\t{\"%s_set_%s\", %s_%s_set_%s},\n" % (ckey, pp["name"], libName, ckey, pp["name"])
								wrappersHeaderOut += "static int %s_%s_set_%s(py_State *L) {\n" % (libName, ckey, pp["name"])
								wrappersHeaderOut += "\t\tpyL_checktype(L, 1, PY_TUSERDATA);\n"
								wrappersHeaderOut += "\t\t%s *inst = (%s*) *((PolyBase**)py_touserdata(L, 1));\n" % (ckey, ckey)
								wrappersHeaderOut += "\t\tpyL_checktype(L, 2, PY_TUSERDATA);\n"
								wrappersHeaderOut += "\t\t%s *argInst = (%s*) *((PolyBase**)py_touserdata(L, 2));\n" % (typeFilter(pp["type"]), typeFilter(pp["type"]))
								wrappersHeaderOut += "\t\tinst->%s = *argInst;\n" % (pp["name"])
								wrappersHeaderOut += "\t\treturn 0;\n"
								wrappersHeaderOut += "}\n\n"
								pidx = pidx + 1 # Success

						# Notice: Setters for object types are not created.
					if inherits:
						pyClassBindingOut += "\t\tif %s[\"__setvar\"] != None :\n" % (parentClass)
						pyClassBindingOut += "\t\t\treturn %s.__setvar(self, name, value)\n" % (parentClass)
						pyClassBindingOut += "\t\telse:\n"
						pyClassBindingOut += "\t\t\treturn false\n"
					else:
						pyClassBindingOut += "\t\treturn false\n"

				# Iterate over methods
				pyClassBindingOut += "\n\n"

				pyDocOut += "\t\t<methods>\n"

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
						pyDocOut += "\t\t\t<method name=\"%s\" return_array=\"true\" return_type=\"%s\"%s>\n" % (pm["name"],  toPyType(typeFilter(vectorReturnClass).replace("*", "")), staticString)
					else:
						pyDocOut += "\t\t\t<method name=\"%s\" return_type=\"%s\"%s>\n" % (pm["name"],  toPyType(typeFilter(pm["rtnType"].replace("*", ""))), staticString)

					docs = None
					if 'doxygen' in pm:
						if pm['doxygen'].find("@return") > -1:
							docs = cleanDocs(pm['doxygen']).split("@return")[0].split("@param")
						else:
							docs = cleanDocs(pm['doxygen']).split("@param")
						pyDocOut += "\t\t\t\t<desc><![CDATA[%s]]></desc>\n" % (docs[0])

					if len(pm["parameters"]) > 0:
						pyDocOut += "\t\t\t\t<params>\n"

						paramIndex = 0
						for param in pm["parameters"]:
							if "name" in param:
								if not "type" in param:
									continue
								if param["type"] == "0":
									continue
								if param["type"].find("vector<") != -1:
									vectorClass = param["type"].replace("std::vector<", "").replace(">","").replace(" ", "")
									pyDocOut += "\t\t\t\t\t<param name=\"%s\" param_array=\"true\" type=\"%s\">\n" % (param["name"], toPyType(vectorClass.replace("*","")))
								else:
									pyDocOut += "\t\t\t\t\t<param name=\"%s\" type=\"%s\">\n" % (param["name"], toPyType(typeFilter(param["type"]).replace("*","")))
								if docs != None:
									if len(docs) > paramIndex+1:
										cdoc = docs[paramIndex+1].split()
										cdoc.pop(0)
										pyDocOut += "\t\t\t\t\t\t<desc><![CDATA[%s]]></desc>\n" % (" ".join(cdoc).replace("\n", ""))
								pyDocOut += "\t\t\t\t\t</param>\n"
								paramIndex = paramIndex + 1
						pyDocOut += "\t\t\t\t</params>\n"


					pyDocOut += "\t\t\t</method>\n"

					basicType = False
					voidRet = False
					vectorReturn = False
					vectorReturnClass = ""
					# Def: True if method takes a py_State* as argument (i.e.: no preprocessing by us)
					rawMethod = len(pm["parameters"]) > 0 and pm["parameters"][0].get("type","").find("py_State") > -1

					# Basic setup, C++ side: Add function to registry and start building wrapper function.
					if pm["name"] == ckey: # It's a constructor
						cppRegisterOut += "\t\t{\"%s\", %s_%s},\n" % (ckey, libName, ckey)
						wrappersHeaderOut += "static int %s_%s(py_State *L) {\n" % (libName, ckey)
						idx = 1 # Def: Current stack depth (TODO: Figure out, is this correct?)
					else: # It's not a constructor
						cppRegisterOut += "\t\t{\"%s_%s\", %s_%s_%s},\n" % (ckey, pm["name"], libName, ckey, pm["name"])
						wrappersHeaderOut += "static int %s_%s_%s(py_State *L) {\n" % (libName, ckey, pm["name"])

						# Skip static methods (TODO: Figure out, why is this being done here?). # FIXME
						if pm["rtnType"].find("static ") == -1:
							wrappersHeaderOut += "\tpyL_checktype(L, 1, PY_TUSERDATA);\n"
							wrappersHeaderOut += "\t%s *inst = (%s*) *((PolyBase**)py_touserdata(L, 1));\n" % (ckey, ckey)
							idx = 2
						else:
							idx = 1

					if rawMethod:
						wrappersHeaderOut += "\treturn inst->%s(L);\n" % (pm["name"])
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
								pytype = "PY_TUSERDATA"
								checkfunc = "py_isuserdata"
								if param["type"].find("*") > -1:
									pyfunc = "(%s) *((PolyBase**)py_touserdata" % (param["type"].replace("Polygon", "Polycode::Polygon").replace("Rectangle", "Polycode::Rectangle"))
								elif param["type"].find("&") > -1:
									pyfunc = "*(%s*) *((PolyBase**)py_touserdata" % (param["type"].replace("const", "").replace("&", "").replace("Polygon", "Polycode::Polygon").replace("Rectangle", "Polycode::Rectangle"))
								else:
									pyfunc = "*(%s*) *((PolyBase**)py_touserdata" % (param["type"].replace("Polygon", "Polycode::Polygon").replace("Rectangle", "Polycode::Rectangle"))
								lend = ".__ptr"
								pyfuncsuffix = ")"
								if param["type"] == "int" or param["type"] == "unsigned int" or param["type"] == "short":
									pyfunc = "py_tointeger"
									pytype = "PY_TNUMBER"
									checkfunc = "py_isnumber"
									pyfuncsuffix = ""
									lend = ""
								if param["type"] == "PolyKEY":
									pyfunc = "(PolyKEY)py_tointeger"
									pytype = "PY_TNUMBER"
									checkfunc = "py_isnumber"
									pyfuncsuffix = ""
									lend = ""
								if param["type"] == "bool":
									pyfunc = "py_toboolean"
									pytype = "PY_TBOOLEAN"
									checkfunc = "py_isboolean"
									pyfuncsuffix = " != 0"
									lend = ""
								if param["type"] == "Number" or param["type"] == "float" or param["type"] == "double":
									pytype = "PY_TNUMBER"
									pyfunc = "py_tonumber"
									checkfunc = "py_isnumber"
									pyfuncsuffix = ""
									lend = ""
								if param["type"] == "String":
									pytype = "PY_TSTRING"
									pyfunc = "py_tostring"
									checkfunc = "py_isstring"
									pyfuncsuffix = ""
									lend = ""

								param["type"] = param["type"].replace("Polygon", "Polycode::Polygon").replace("Rectangle", "Polycode::Rectangle")

								if "defaltValue" in param:
									if checkfunc != "py_isuserdata" or (checkfunc == "py_isuserdata" and param["defaltValue"] == "NULL"):
										#param["defaltValue"] = param["defaltValue"].replace(" 0f", ".0f")
										param["defaltValue"] = param["defaltValue"].replace(": :", "::")
										#param["defaltValue"] = param["defaltValue"].replace("0 ", "0.")
										param["defaltValue"] = re.sub(r'([0-9]+) ([0-9])+', r'\1.\2', param["defaltValue"])

										wrappersHeaderOut += "\t%s %s;\n" % (param["type"], param["name"])
										wrappersHeaderOut += "\tif(%s(L, %d)) {\n" % (checkfunc, idx)
										wrappersHeaderOut += "\t\t%s = %s(L, %d)%s;\n" % (param["name"], pyfunc, idx, pyfuncsuffix)
										wrappersHeaderOut += "\t} else {\n"
										wrappersHeaderOut += "\t\t%s = %s;\n" % (param["name"], param["defaltValue"])
										wrappersHeaderOut += "\t}\n"
									else:
										wrappersHeaderOut += "\tpyL_checktype(L, %d, %s);\n" % (idx, pytype);
										if param["type"] == "String":
											wrappersHeaderOut += "\t%s %s = String(%s(L, %d));\n" % (param["type"], param["name"], pyfunc, idx)
										else:
											wrappersHeaderOut += "\t%s %s = %s(L, %d)%s;\n" % (param["type"], param["name"], pyfunc, idx,pyfuncsuffix)
								else:
									wrappersHeaderOut += "\tpyL_checktype(L, %d, %s);\n" % (idx, pytype);
									if param["type"] == "String":
										wrappersHeaderOut += "\t%s %s = String(%s(L, %d));\n" % (param["type"], param["name"], pyfunc, idx)
									else:
										wrappersHeaderOut += "\t%s %s = %s(L, %d)%s;\n" % (param["type"], param["name"], pyfunc, idx, pyfuncsuffix)
								paramlist.append(param["name"])

								lparamlist.append(param["name"]+lend)
								idx = idx +1 # Param parse success-- mark the increased stack

						# Generate C++-side method call / generate return value
						if pm["name"] == ckey: # If constructor
							if ckey == "EventHandler": # See PyEventHandler above
								wrappersHeaderOut += "\tPyEventHandler *inst = new PyEventHandler();\n"
								wrappersHeaderOut += "\tinst->wrapperIndex = pyL_ref(L, PY_REGISTRYINDEX );\n"
								wrappersHeaderOut += "\tinst->L = L;\n"
							else:
								wrappersHeaderOut += "\t%s *inst = new %s(%s);\n" % (ckey, ckey, ", ".join(paramlist))

							wrappersHeaderOut += "\tPolyBase **userdataPtr = (PolyBase**)py_newuserdata(L, sizeof(PolyBase*));\n"
							wrappersHeaderOut += "\t*userdataPtr = (PolyBase*)inst;\n"
							wrappersHeaderOut += "\tpyL_getmetatable(L, \"%s.%s\");\n" % (libName, ckey)
							wrappersHeaderOut += "\tpy_setmetatable(L, -2);\n"
							wrappersHeaderOut += "\treturn 1;\n"
						else: #If non-constructor
							if pm["rtnType"].find("static ") == -1: # If non-static
								call = "inst->%s(%s)" % (pm["name"], ", ".join(paramlist))
							else: # If static (FIXME: Why doesn't this work?)
								call = "%s::%s(%s)" % (ckey, pm["name"], ", ".join(paramlist))

							#check if returning a template
							if pm["rtnType"].find("<") > -1:
								#if returning a vector, convert to py table
								if pm["rtnType"].find("std::vector") > -1:
									vectorReturnClass = pm["rtnType"].replace("std::vector<", "").replace(">","").replace(" ", "")
									if vectorReturnClass.find("&") == -1 and vectorReturnClass.find("*") > -1: #FIXME: return references to std::vectors and basic types
										vectorReturn = True
										wrappersHeaderOut += "\tstd::vector<%s> retVector = %s;\n" % (vectorReturnClass,call)
										wrappersHeaderOut += "\tpy_newtable(L);\n"
										wrappersHeaderOut += "\tfor(int i=0; i < retVector.size(); i++) {\n"
										wrappersHeaderOut += "\t\tPolyBase **userdataPtr = (PolyBase**)py_newuserdata(L, sizeof(PolyBase*));\n"
										wrappersHeaderOut += "\t\t*userdataPtr = (PolyBase*)retVector[i];\n"
										wrappersHeaderOut += "\t\tpy_rawseti(L, -2, i+1);\n"
										wrappersHeaderOut += "\t}\n"
										wrappersHeaderOut += "\treturn 1;\n"
									else:
										wrappersHeaderOut += "\treturn 0;\n"

							# else If void-typed:
							elif pm["rtnType"] == "void" or pm["rtnType"] == "static void" or pm["rtnType"] == "virtual void" or pm["rtnType"] == "inline void":
								wrappersHeaderOut += "\t%s;\n" % (call)
								basicType = True
								voidRet = True
								vectorReturn = False
								wrappersHeaderOut += "\treturn 0;\n" # 0 arguments returned
							else: # If there is a return value:
								# What type is the return value? Default to pointer
								outfunc = "this_shouldnt_happen"
								retFunc = ""
								basicType = False
								vectorReturn = False
								if pm["rtnType"] == "Number" or  pm["rtnType"] == "inline Number":
									outfunc = "py_pushnumber"
									basicType = True
								if pm["rtnType"] == "String" or pm["rtnType"] == "static String": # TODO: Path for STL strings?
									outfunc = "py_pushstring"
									basicType = True
									retFunc = ".c_str()"
								if pm["rtnType"] == "int" or pm["rtnType"] == "unsigned int" or pm["rtnType"] == "static int" or  pm["rtnType"] == "size_t" or pm["rtnType"] == "static size_t" or pm["rtnType"] == "long" or pm["rtnType"] == "unsigned int" or pm["rtnType"] == "static long" or pm["rtnType"] == "short" or pm["rtnType"] == "PolyKEY" or pm["rtnType"] == "wchar_t":
									outfunc = "py_pushinteger"
									basicType = True
								if pm["rtnType"] == "bool" or pm["rtnType"] == "static bool" or pm["rtnType"] == "virtual bool":
									outfunc = "py_pushboolean"
									basicType = True

								if pm["rtnType"].find("*") > -1: # Returned var is definitely a pointer.
									wrappersHeaderOut += "\tPolyBase *ptrRetVal = (PolyBase*)%s%s;\n" % (call, retFunc)
									wrappersHeaderOut += "\tif(ptrRetVal == NULL) {\n"
									wrappersHeaderOut += "\t\tpy_pushNone(L);\n"
									wrappersHeaderOut += "\t} else {\n"
									wrappersHeaderOut += "\t\tPolyBase **userdataPtr = (PolyBase**)py_newuserdata(L, sizeof(PolyBase*));\n"
									wrappersHeaderOut += "\t\t*userdataPtr = ptrRetVal;\n"
									wrappersHeaderOut += "\t}\n"
								elif basicType == True: # Returned var has been flagged as a recognized primitive type
									wrappersHeaderOut += "\t%s(L, %s%s);\n" % (outfunc, call, retFunc)
								else: # Some static object is being returned. Convert it to a pointer, then return that.
									className = pm["rtnType"].replace("const", "").replace("&", "").replace("inline", "").replace("virtual", "").replace("static", "")
									if className == "Polygon": # Deal with potential windows.h conflict
										className = "Polycode::Polygon"
									if className == "Rectangle":
										className = "Polycode::Rectangle"
									if className == "Polycode : : Rectangle":
										className = "Polycode::Rectangle"
									wrappersHeaderOut += "\t%s *retInst = new %s();\n" % (className, className)
									wrappersHeaderOut += "\t*retInst = %s;\n" % (call)
									wrappersHeaderOut += "\tPolyBase **userdataPtr = (PolyBase**)py_newuserdata(L, sizeof(PolyBase*));\n"
									wrappersHeaderOut += "\tpyL_getmetatable(L, \"%s.%s\");\n" % (libName, className)
									wrappersHeaderOut += "\tpy_setmetatable(L, -2);\n"
									wrappersHeaderOut += "\t*userdataPtr = (PolyBase*)retInst;\n"
								wrappersHeaderOut += "\treturn 1;\n"
					wrappersHeaderOut += "}\n\n" # Close out C++ generation

					# Now generate the Py side method.
					if rawMethod:
						pyClassBindingOut += "\def %s(self, **kwargs):\n" % pm["name"]
						pyClassBindingOut += "\t\treturn %s.%s_%s(self.__ptr, **kwargs)\n" % (libName, ckey, pm["name"])
					elif pm["name"] == ckey: # Constructors
						pyClassBindingOut += "\tdef %s(**kwargs):\n" % ckey
						pyClassBindingOut += "\t\targ = kwargs\n"
						if inherits:
							pyClassBindingOut += "\t\tif type(arg[1]) == \"table\" and count(arg) == 1 :\n"
							pyClassBindingOut += "\t\t\tif arg[1].__classname == \"%s\" :\n" % (c["inherits"][0]["class"])
							pyClassBindingOut += "\t\t\t\tself.__ptr = arg[1].__ptr\n"
							pyClassBindingOut += "\t\t\t\treturn\n"
						pyClassBindingOut += "\t\tfor k, v in enumerate(arg):\n"
						pyClassBindingOut += "\t\t\tif type(v) == \"table\" :\n"
						pyClassBindingOut += "\t\t\t\tif v.__ptr != None :\n"
						pyClassBindingOut += "\t\t\t\t\targ[k] = v.__ptr\n"
						pyClassBindingOut += "\t\tif self.__ptr == None and arg[1] != \"__skip_ptr__\" :\n"
						if ckey == "EventHandler": # See PyEventHandler above
							pyClassBindingOut += "\t\t\tself.__ptr = %s.%s(self)\n" % (libName, ckey)
						else:
							pyClassBindingOut += "\t\t\tself.__ptr = %s.%s(unpack(arg))\n" % (libName, ckey)
					else: # Non-constructors.
						if pm["rtnType"].find("static ") == -1: # Non-static method
							pyClassBindingOut += "\tdef %s(%s):\n" % (pm["name"], ", ".join(paramlist))
							if len(lparamlist):
								pyClassBindingOut += "\t\tretVal = %s.%s_%s(self.__ptr, %s)\n" % (libName, ckey, pm["name"], ", ".join(lparamlist))
							else:
								pyClassBindingOut += "\t\tretVal =  %s.%s_%s(self.__ptr)\n" % (libName, ckey, pm["name"])
						else: # Static method
							pyClassBindingOut += "\tdef %s(%s):\n" % (pm["name"], ", ".join(paramlist))
							if len(lparamlist):
								pyClassBindingOut += "\t\tretVal = %s.%s_%s(%s)\n" % (libName, ckey, pm["name"], ", ".join(lparamlist))
							else:
								pyClassBindingOut += "\t\tretVal =  %s.%s_%s()\n" % (libName, ckey, pm["name"])

						if not voidRet: # Was there a return value?
							if basicType == True: # Yes, a primitive
								pyClassBindingOut += "\t\treturn retVal\n"
							else: # Yes, a pointer was returned
								if vectorReturn == True:
									className = vectorReturnClass.replace("*", "")
									pyClassBindingOut += template_returnPtrLookupArray("\t\t",template_quote(className),"retVal")
								else:
									className = pm["rtnType"].replace("const", "").replace("&", "").replace("inline", "").replace("virtual", "").replace("static", "").replace("*","").replace(" ", "")
									pyClassBindingOut += template_returnPtrLookup("\t\t",template_quote(className),"retVal")

					parsed_methods.append(pm["name"]) # Method parse success

				pyDocOut += "\t\t</methods>\n"

				# With methods out of the way, do some final cleanup:

				# user pointer metatable creation in C++
				cppLoaderOut += "\n\tpyL_newmetatable(L, \"%s.%s\");\n" % (libName, ckey)
				if ckey not in disable_gc:
					cppLoaderOut += "\tpy_pushstring(L, \"__gc\");\n"
					cppLoaderOut += "\tpy_pushcfunction(L, %s_delete_%s);\n" % (libName, ckey)
					cppLoaderOut += "\tpy_settable(L, -3);\n"
				cppLoaderOut +="\tpy_pop(L, 1);\n"

				# Delete method (C++ side)
				cppRegisterOut += "\t\t{\"delete_%s\", %s_delete_%s},\n" % (ckey, libName, ckey)
				wrappersHeaderOut += "static int %s_delete_%s(py_State *L) {\n" % (libName, ckey)
				wrappersHeaderOut += "\tpyL_checktype(L, 1, PY_TUSERDATA);\n"
				wrappersHeaderOut += "\tPolyBase **inst = (PolyBase**)py_touserdata(L, 1);\n"
				wrappersHeaderOut += "\tdelete ((%s*) *inst);\n" % (ckey)
				wrappersHeaderOut += "\t*inst = NULL;\n"
				wrappersHeaderOut += "\treturn 0;\n"
				wrappersHeaderOut += "}\n\n"

				# Add class to py index file
				pyIndexOut += "import %s.%s\n" % (prefix, ckey)
				# Write py file
				mkdir_p(apiClassPath)
				if ckey != "EventDispatcher":
					fout = open("%s/%s.py" % (apiClassPath, ckey), "w")
					fout.write(pyClassBindingOut)

				pyDocOut += "\t</class>\n"

		except CppHeaderParser.CppParseError as e: # One input file parse; failed.
			# print(e)
			sys.exit(1)

	pyDocOut += "</classes>\n"
	pyDocOut += "</docs>\n"

	# Footer boilerplate for wrappersHeaderOut and cppRegisterOut.
	wrappersHeaderOut += "} // namespace Polycode\n"

	cppRegisterOut += "\t\t{NULL, NULL}\n"
	cppRegisterOut += "\t};\n"
	cppRegisterOut += "\tpyL_openlib(L, \"%s\", %sLib, 0);\n" % (libName, libSmallName)
	cppRegisterOut += cppLoaderOut
	cppRegisterOut += "\treturn 1;\n"
	cppRegisterOut += "}"


	cppRegisterHeaderOut = "" # Def: Global C++ *PY.h
	cppRegisterHeaderOut += "#pragma once\n"
	cppRegisterHeaderOut += "#include <%s>\n" % (mainInclude)
	cppRegisterHeaderOut += "extern \"C\" {\n"
	cppRegisterHeaderOut += "#include <stdio.h>\n"
	cppRegisterHeaderOut += "#include \"py.h\"\n"
	cppRegisterHeaderOut += "#include \"pylib.h\"\n"
	cppRegisterHeaderOut += "#include \"lauxlib.h\"\n"
	cppRegisterHeaderOut += "int _PolyExport pyopen_%s(py_State *L);\n" % (prefix)
	cppRegisterHeaderOut += "}\n"

	# Write out global files
	mkdir_p(includePath)
	mkdir_p(apiPath)
	mkdir_p(sourcePath)

	fout = open("%s/%sPY.h" % (includePath, prefix), "w")
	fout.write(cppRegisterHeaderOut)

	if pyDocPath is None:
		pyDocPath = "../../../Documentation/Py/xml"
	if pyDocPath != "-":
		fout = open("%s/%s.xml" % (pyDocPath, prefix), "w")
		fout.write(pyDocOut)

	fout = open("%s/%s.py" % (apiPath, prefix), "w")
	fout.write(pyIndexOut)

	fout = open("%s/%sPYWrappers.h" % (includePath, prefix), "w")
	fout.write(wrappersHeaderOut)

	fout = open("%s/%sPY.cpp" % (sourcePath, prefix), "w")
	fout.write(cppRegisterOut)

	# Create .pak zip archive
	pattern = '*.py'
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

if len(sys.argv) < 10:
	# print ("Usage:\n%s [input path] [prefix] [main include] [lib small name] [lib name] [api path] [api class-path] [include path] [source path] [py doc path (optional) (or - for omit)] [inherit-in-module-file path (optional)]" % (sys.argv[0]))
	sys.exit(1)
else:
	start = time.time()
	createPYBindings(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8], sys.argv[9], sys.argv[10] if len(sys.argv)>10 else None, sys.argv[11] if len(sys.argv)>11 else None)
	print(time.time() - start)
