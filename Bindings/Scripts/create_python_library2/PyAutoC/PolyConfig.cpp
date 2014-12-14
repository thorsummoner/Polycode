
PyAutoFunction_RegisterVoid(loadConfig, 2, const, const);
PyAutoFunction_RegisterVoid(saveConfig, 2, const, const);
PyAutoFunction_RegisterVoid(setStringValue, 3, const, const, const);
PyAutoFunction_RegisterVoid(setNumericValue, 3, const, const, Number);
PyAutoFunction_Register(getNumericValue, Number, 2, const, const);
PyAutoFunction_RegisterVoid(setBoolValue, 3, const, const, bool);
PyAutoFunction_Register(getBoolValue, bool, 2, const, const);

