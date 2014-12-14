
PyAutoFunction_RegisterVoid(setFallbackPool, 1, ResourcePoo);
PyAutoFunction_RegisterVoid(addResource, 1, Resourc);
PyAutoFunction_RegisterVoid(removeResource, 1, Resourc);
PyAutoFunction_Register(hasResource, bool, 1, Resourc);
PyAutoFunction_Register(getName, String, 0);
PyAutoFunction_RegisterVoid(setName, 1, const);
PyAutoFunction_RegisterVoid(Update, 1, int);
PyAutoFunction_RegisterVoid(checkForChangedFiles, 0);
PyAutoFunction_RegisterVoid(addDirResource, 2, const, bool);
PyAutoFunction_RegisterVoid(addArchive, 1, const);
PyAutoFunction_RegisterVoid(removeArchive, 1, const);
PyAutoFunction_RegisterVoid(parseTexturesIntoPool, 4, ResourcePoo, const, bool, const);
PyAutoFunction_RegisterVoid(parseMaterialsIntoPool, 3, ResourcePoo, const, bool);
PyAutoFunction_RegisterVoid(parseShadersIntoPool, 3, ResourcePoo, const, bool);
PyAutoFunction_RegisterVoid(parseProgramsIntoPool, 3, ResourcePoo, const, bool);
PyAutoFunction_RegisterVoid(parseCubemapsIntoPool, 3, ResourcePoo, const, bool);
PyAutoFunction_RegisterVoid(parseOtherIntoPool, 3, ResourcePoo, const, bool);
PyAutoFunction_RegisterVoid(addResourcePool, 1, ResourcePoo);
PyAutoFunction_RegisterVoid(removeResourcePool, 1, ResourcePoo);
PyAutoFunction_RegisterVoid(removeResource, 1, Resourc);
PyAutoFunction_RegisterVoid(subscribeToResourcePool, 1, ResourcePoo);
PyAutoFunction_RegisterVoid(unsubscibeFromResourcePool, 1, ResourcePoo);
PyAutoFunction_RegisterVoid(Update, 1, int);
PyAutoFunction_RegisterVoid(handleEvent, 1, Even);

