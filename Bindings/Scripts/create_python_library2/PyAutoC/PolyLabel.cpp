
PyAutoFunction_RegisterVoid(clearData, 0);
PyAutoFunction_RegisterVoid(setText, 1, const);
PyAutoFunction_Register(getTextWidthForString, int, 1, const);
PyAutoFunction_Register(getTextHeightForString, int, 1, const);
PyAutoFunction_Register(getTextWidth, Number, 6, cons, not, so, you, unsigned, unsigned);
PyAutoFunction_RegisterVoid(clearColors, 0);
PyAutoFunction_Register(getColorForIndex, Color, 1, unsigned);
PyAutoFunction_Register(getPremultiplyAlpha, bool, 2, cons, will);
PyAutoFunction_RegisterVoid(setFont, 1, Fon);
PyAutoFunction_RegisterVoid(setSize, 1, int);
PyAutoFunction_Register(getSize, int, 2, cons, ANTIALIAS_NONE);
PyAutoFunction_Register(getBaselineAdjust, int, 0);
PyAutoFunction_Register(optionsChanged, bool, 0);
PyAutoFunction_RegisterVoid(computeStringBbox, 2, GlyphDat, FT_BBo);
PyAutoFunction_RegisterVoid(precacheGlyphs, 2, String, GlyphDat);
PyAutoFunction_RegisterVoid(renderGlyphs, 1, GlyphDat);
PyAutoFunction_RegisterVoid(drawGlyphBitmap, 4, FT_Bitma, unsigned, unsigned, Color);

