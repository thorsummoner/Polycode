INCLUDE(FindPythonModule)

FIND_PACKAGE(PythonInterp REQUIRED)

FILE(GLOB XML_DEPENDENCIES ${CMAKE_CURRENT_SOURCE_DIR}/../xml/*.xml)

ADD_CUSTOM_COMMAND(
OUTPUT pyGenerateDocsCmd
COMMAND ${PYTHON_EXECUTABLE} make_html.py
COMMAND ${CMAKE_COMMAND} -E touch ${CMAKE_CURRENT_BINARY_DIR}/pyGenerateDocsCmd # Generate the given output file(empty file), to keep track of whether we need to rebuild.
DEPENDS ${XML_DEPENDENCIES}
WORKING_DIRECTORY ${CMAKE_CURRENT_LIST_DIR}
)

ADD_CUSTOM_TARGET(PolycodePyGenerateDocs
	DEPENDS Polycore PolycodePyGenerate pyGenerateDocsCmd
	COMMENT "Generating Py Documentation"
	SOURCES make_html.py)

