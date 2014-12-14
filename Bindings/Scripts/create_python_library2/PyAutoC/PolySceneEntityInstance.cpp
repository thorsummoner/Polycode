
PyAutoFunction_Register(SceneEntityInstance, explicit, 1, Scen);
PyAutoFunction_RegisterVoid(applyClone, 3, Entit, bool, bool);
PyAutoFunction_RegisterVoid(clearInstance, 0);
PyAutoFunction_RegisterVoid(parseObjectIntoCurve, 2, ObjectEntr, BezierCurv);
PyAutoFunction_Register(loadFromFile, bool, 1, const);
PyAutoFunction_RegisterVoid(applySceneMesh, 2, ObjectEntr, SceneMes);
PyAutoFunction_RegisterVoid(linkResourcePool, 1, ResourcePoo);
PyAutoFunction_Register(getNumLinkedResourePools, int, 0);
PyAutoFunction_RegisterVoid(unlinkResourcePool, 1, ResourcePoo);
PyAutoFunction_Register(hasLayerID, bool, 1, unsigned);
PyAutoFunction_Register(getFileName, String, 1, cons);
PyAutoFunction_RegisterVoid(setLayerVisibility, 1, bool);
PyAutoFunction_RegisterVoid(reloadResource, 0);

