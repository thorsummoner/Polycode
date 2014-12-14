
PyAutoFunction_Register(Material, explicit, 1, const);
PyAutoFunction_RegisterVoid(addShader, 2, Shade, ShaderBindin);
PyAutoFunction_RegisterVoid(addShaderAtIndex, 3, Shade, ShaderBindin, int);
PyAutoFunction_Register(getNumShaders, int, 1, cons);
PyAutoFunction_RegisterVoid(addShaderRenderTarget, 1, ShaderRenderTarge);
PyAutoFunction_Register(getNumShaderRenderTargets, int, 0);
PyAutoFunction_RegisterVoid(removeShaderRenderTarget, 1, int);
PyAutoFunction_RegisterVoid(recreateRenderTarget, 1, ShaderRenderTarge);
PyAutoFunction_RegisterVoid(recreateRenderTargets, 0);
PyAutoFunction_RegisterVoid(handleEvent, 1, Even);
PyAutoFunction_RegisterVoid(loadMaterial, 1, const);
PyAutoFunction_RegisterVoid(setName, 1, const);
PyAutoFunction_RegisterVoid(clearShaders, 0);

