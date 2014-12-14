
PyAutoFunction_RegisterVoid(addScene, 1, Scen);
PyAutoFunction_RegisterVoid(removeScene, 1, Scen);
PyAutoFunction_RegisterVoid(Update, 0);
PyAutoFunction_RegisterVoid(fixedUpdate, 0);
PyAutoFunction_RegisterVoid(Render, 0);
PyAutoFunction_RegisterVoid(renderVirtual, 0);
PyAutoFunction_RegisterVoid(registerRenderTexture, 1, SceneRenderTextur);
PyAutoFunction_RegisterVoid(unregisterRenderTexture, 1, SceneRenderTextur);
PyAutoFunction_RegisterVoid(setRenderer, 1, Rendere);
PyAutoFunction_RegisterVoid(updateRenderTextures, 1, Scen);

