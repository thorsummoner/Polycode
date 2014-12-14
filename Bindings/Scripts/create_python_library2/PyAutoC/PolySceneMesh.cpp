
PyAutoFunction_Register(SceneMesh, explicit, 1, const);
PyAutoFunction_Register(SceneMesh, explicit, 1, int);
PyAutoFunction_Register(SceneMesh, explicit, 1, Mes);
PyAutoFunction_RegisterVoid(Render, 0);
PyAutoFunction_RegisterVoid(loadTexture, 1, const);
PyAutoFunction_RegisterVoid(loadTextureFromImage, 1, Imag);
PyAutoFunction_RegisterVoid(setTexture, 1, Textur);
PyAutoFunction_RegisterVoid(clearMaterial, 0);
PyAutoFunction_RegisterVoid(setMaterial, 1, Materia);
PyAutoFunction_RegisterVoid(setMaterialByName, 2, const, ResourcePoo);
PyAutoFunction_RegisterVoid(setMesh, 1, Mes);
PyAutoFunction_RegisterVoid(setSkeleton, 1, Skeleto);
PyAutoFunction_RegisterVoid(renderMeshLocally, 0);
PyAutoFunction_RegisterVoid(cacheToVertexBuffer, 1, bool);
PyAutoFunction_RegisterVoid(setLineWidth, 1, Number);
PyAutoFunction_Register(getFilename, String, 0);
PyAutoFunction_RegisterVoid(setFilename, 1, String);
PyAutoFunction_RegisterVoid(loadFromFile, 1, String);
PyAutoFunction_Register(customHitDetection, bool, 1, const);

