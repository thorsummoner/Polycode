
PyAutoFunction_RegisterVoid(addEntity, 1, Entit);
PyAutoFunction_RegisterVoid(addChild, 1, Entit);
PyAutoFunction_RegisterVoid(removeEntity, 1, Entit);
PyAutoFunction_RegisterVoid(setActiveCamera, 1, Camer);
PyAutoFunction_RegisterVoid(enableLighting, 1, bool);
PyAutoFunction_RegisterVoid(enableFog, 1, bool);
PyAutoFunction_RegisterVoid(setFogProperties, 5, int, Color, Number, Number, Number);
PyAutoFunction_RegisterVoid(setSceneType, 1, int);
PyAutoFunction_RegisterVoid(fixedUpdate, 0);
PyAutoFunction_RegisterVoid(Update, 0);
PyAutoFunction_RegisterVoid(setVirtual, 1, bool);
PyAutoFunction_Register(isVirtual, bool, 0);
PyAutoFunction_Register(isEnabled, bool, 0);
PyAutoFunction_RegisterVoid(setEnabled, 1, bool);
PyAutoFunction_RegisterVoid(Render, 1, Camer);
PyAutoFunction_RegisterVoid(RenderDepthOnly, 1, Camer);
PyAutoFunction_RegisterVoid(setOverrideMaterial, 1, Materia);
PyAutoFunction_RegisterVoid(handleEvent, 1, Even);
PyAutoFunction_Register(projectRayFromCameraAndViewportCoordinate, Ray, 2, Camer, Vector2);
PyAutoFunction_RegisterVoid(addLight, 1, SceneLigh);
PyAutoFunction_RegisterVoid(removeLight, 1, SceneLigh);
PyAutoFunction_Register(getNumLights, int, 0);
PyAutoFunction_RegisterVoid(doVisibilityChecking, 1, bool);
PyAutoFunction_Register(doesVisibilityChecking, bool, 0);
PyAutoFunction_RegisterVoid(initScene, 2, int, bool);
PyAutoFunction_RegisterVoid(setEntityVisibility, 2, Entit, Camer);
PyAutoFunction_RegisterVoid(setEntityVisibilityBool, 2, Entit, bool);

