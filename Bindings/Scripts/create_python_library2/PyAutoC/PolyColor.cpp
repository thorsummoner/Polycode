
PyAutoFunction_Register(ColorWithInts, Color, 4, int, int, int, int);
PyAutoFunction_Register(ColorWithHex, Color, 1, unsigned);
PyAutoFunction_Register(Color, return, 4, n, n, n, n);
PyAutoFunction_Register(Color, return, 4, n, n, n, n);
PyAutoFunction_Register(Color, return, 4, n, n, n, n);
PyAutoFunction_RegisterVoid(setColorHex, 1, unsigned);
PyAutoFunction_RegisterVoid(setColorHexRGB, 1, unsigned);
PyAutoFunction_RegisterVoid(setColorHexFromString, 1, String);
PyAutoFunction_RegisterVoid(setColorHexRGBFromString, 1, String);
PyAutoFunction_RegisterVoid(setColorHSV, 3, Number, Number, Number);
PyAutoFunction_RegisterVoid(setColorRGBA, 4, int, int, int, int);
PyAutoFunction_RegisterVoid(setColorRGB, 3, int, int, int);
PyAutoFunction_RegisterVoid(setColor, 4, Number, Number, Number, Number);
PyAutoFunction_RegisterVoid(setColor, 1, const);
PyAutoFunction_Register(blendColor, Color, 4, Color, int, Number, Color);
PyAutoFunction_RegisterVoid(Random, 0);
PyAutoFunction_Register(getBrightness, Number, 6, cons, const, const, Numbe, Numbe, Numbe);

