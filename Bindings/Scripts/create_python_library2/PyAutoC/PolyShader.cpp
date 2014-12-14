
PyAutoStruct_Register(TextureBinding);
PyAutoStruct_RegisterMember(TextureBinding, e, Textur);
PyAutoStruct_RegisterMember(TextureBinding, name, String);

PyAutoStruct_Register(CubemapBinding);
PyAutoStruct_RegisterMember(CubemapBinding, p, Cubema);
PyAutoStruct_RegisterMember(CubemapBinding, name, String);

PyAutoFunction_Register(ShaderProgram, explicit, 1, int);
PyAutoFunction_RegisterVoid(reloadProgram, 1, static);
PyAutoFunction_Register(Shader, explicit, 1, int);
PyAutoFunction_Register(getType, int, 1, cons);
PyAutoFunction_RegisterVoid(reload, 1, int);
PyAutoFunction_RegisterVoid(setVertexProgram, 1, ShaderProgra);
PyAutoFunction_Register(getNumber, Number, 0);
PyAutoFunction_Register(getVector2, Vector2, 0);
PyAutoFunction_Register(getVector3, Vector3, 0);
PyAutoFunction_Register(getMatrix4, Matrix4, 0);
PyAutoFunction_Register(getColor, Color, 0);
PyAutoFunction_RegisterVoid(setNumber, 1, Number);
PyAutoFunction_RegisterVoid(setVector2, 1, Vector2);
PyAutoFunction_RegisterVoid(setVector3, 1, Vector3);
PyAutoFunction_RegisterVoid(setMatrix4, 1, Matrix4);
PyAutoFunction_RegisterVoid(setColor, 1, Color);
PyAutoFunction_RegisterVoid(setParamValueFromString, 2, int, String);
PyAutoFunction_RegisterVoid(copyTo, 1, ShaderBindin);
PyAutoFunction_RegisterVoid(clearTexture, 1, const);
PyAutoFunction_RegisterVoid(clearCubemap, 1, const);
PyAutoFunction_RegisterVoid(addTexture, 2, const, Textur);
PyAutoFunction_RegisterVoid(addCubemap, 2, const, Cubema);
PyAutoFunction_Register(getNumLocalParams, int, 0);
PyAutoFunction_RegisterVoid(addRenderTargetBinding, 1, RenderTargetBindin);
PyAutoFunction_RegisterVoid(removeRenderTargetBinding, 1, RenderTargetBindin);
PyAutoFunction_Register(getNumRenderTargetBindings, int, 0);
PyAutoFunction_Register(getNumInTargetBindings, int, 0);
PyAutoFunction_Register(getNumColorTargetBindings, int, 0);
PyAutoFunction_Register(getNumDepthTargetBindings, int, 0);
PyAutoFunction_Register(getNumOutTargetBindings, int, 0);

