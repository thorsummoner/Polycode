
PyAutoFunction_Register(getText, String, 0);
PyAutoFunction_RegisterVoid(setLabelActualHeight, 1, Number);
PyAutoFunction_Register(getLabelActualHeight, Number, 0);
PyAutoFunction_RegisterVoid(Render, 0);
PyAutoFunction_Register(getTextWidthForString, int, 1, String);
PyAutoFunction_RegisterVoid(setText, 1, const);
PyAutoFunction_RegisterVoid(applyClone, 3, Entit, bool, bool);

