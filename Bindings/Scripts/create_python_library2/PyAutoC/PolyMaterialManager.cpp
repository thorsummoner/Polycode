
PyAutoFunction_RegisterVoid(Update, 1, int);
PyAutoFunction_RegisterVoid(deleteTexture, 1, Textur);
PyAutoFunction_RegisterVoid(reloadTextures, 0);
PyAutoFunction_RegisterVoid(reloadProgramsAndTextures, 0);
PyAutoFunction_RegisterVoid(reloadPrograms, 0);
PyAutoFunction_RegisterVoid(addShaderModule, 1, PolycodeShaderModul);
PyAutoFunction_RegisterVoid(loadMaterialLibraryIntoPool, 2, ResourcePoo, const);
PyAutoFunction_RegisterVoid(addMaterial, 1, Materia);
PyAutoFunction_RegisterVoid(addShader, 1, Shade);
PyAutoFunction_Register(getNumShaders, int, 0);

