
PyAutoFunction_Register(SceneImage, explicit, 1, const);
PyAutoFunction_Register(SceneImage, explicit, 1, Imag);
PyAutoFunction_Register(SceneImage, explicit, 1, Textur);
PyAutoFunction_Register(SceneImageWithImage, SceneImage*, 1, Imag);
PyAutoFunction_Register(SceneImageWithTexture, SceneImage*, 1, Textur);
PyAutoFunction_RegisterVoid(applyClone, 8, Entit, bool, bool, Number, Number, Number, Number, Number);

