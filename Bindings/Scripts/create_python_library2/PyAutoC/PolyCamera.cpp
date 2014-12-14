
PyAutoFunction_Register(Camera, explicit, 1, Scen);
PyAutoFunction_RegisterVoid(buildFrustumPlanes, 0);
PyAutoFunction_Register(canSee, see, 2, bool, Number);
PyAutoFunction_Register(isAABBInFrustum, bool, 1, const);
PyAutoFunction_RegisterVoid(setOrthoMode, 1, bool);
PyAutoFunction_RegisterVoid(setOrthoSize, 2, Number, Number);
PyAutoFunction_RegisterVoid(setFrustumMode, 6, Number, Number, Number, Number, Number, Number);
PyAutoFunction_Register(getOrthoMode, bool, 1, return);
PyAutoFunction_Register(getOrthoSizeY, Number, 0);
PyAutoFunction_RegisterVoid(setFOV, 1, Number);
PyAutoFunction_Register(getFOV, Number, 2, return, Number);
PyAutoFunction_Register(getNearClippingPlane, Number, 0);
PyAutoFunction_Register(getFarClippingPlane, Number, 0);
PyAutoFunction_RegisterVoid(setParentScene, 1, Scen);
PyAutoFunction_RegisterVoid(doCameraTransform, 0);
PyAutoFunction_Register(hasFilterShader, bool, 0);
PyAutoFunction_RegisterVoid(drawFilter, 5, Textur, Number, Number, Textur, Textur);
PyAutoFunction_RegisterVoid(setExposureLevel, 1, Number);
PyAutoFunction_RegisterVoid(setPostFilterByName, 1, const);
PyAutoFunction_RegisterVoid(removePostFilter, 0);
PyAutoFunction_Register(getNumLocalShaderOptions, int, 4, cons, bool, bool, bool);
PyAutoFunction_RegisterVoid(setProjectionMatrix, 1, Matrix4);
PyAutoFunction_Register(getViewport, Rectangle, 0);
PyAutoFunction_Register(setProjectionMode, use, 1, ProjectionMode);
PyAutoFunction_Register(getProjectionMode, use, 6, int, ORTHO_SIZE_LOCK_HEIGH, ORTHO_SIZE_LOCK_WIDT, ORTHO_SIZE_LOCK_WIDT, PERSPECTIVE_FO, PERSPECTIVE_FRUSTUM);
PyAutoFunction_Register(getProjectionMode, int, 1, cons);

