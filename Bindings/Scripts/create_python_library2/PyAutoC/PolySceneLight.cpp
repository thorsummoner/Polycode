
PyAutoFunction_Register(getIntensity, Number, 1, cons);
PyAutoFunction_RegisterVoid(setAttenuation, 3, Number, Number, Number);
PyAutoFunction_Register(getConstantAttenuation, Number, 1, cons);
PyAutoFunction_RegisterVoid(Render, 0);
PyAutoFunction_RegisterVoid(setSpecularLightColor, 9, Number, Number, Number, Number, Number, Number, Number, Number, Number);
PyAutoFunction_RegisterVoid(setSpotlightProperties, 5, Number, Number, the, enables, unsigned);
PyAutoFunction_RegisterVoid(setShadowMapFOV, 1, Number);
PyAutoFunction_Register(getShadowMapFOV, Number, 1, cons);
PyAutoFunction_Register(getLightImportance, int, 1, cons);
PyAutoFunction_RegisterVoid(applyClone, 3, Entit, bool, bool);

