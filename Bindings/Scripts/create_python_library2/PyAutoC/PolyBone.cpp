
PyAutoFunction_Register(Bone, explicit, 1, const);
PyAutoFunction_Register(getName, String, 1, cons);
PyAutoFunction_RegisterVoid(addChildBone, 1, Bon);
PyAutoFunction_Register(getParentBone, Bone*, 0);
PyAutoFunction_Register(getNumChildBones, int, 0);
PyAutoFunction_Register(getBoneMatrix, Matrix4, 1, cons);
PyAutoFunction_Register(getRestMatrix, Matrix4, 1, cons);
PyAutoFunction_RegisterVoid(setBaseMatrix, 1, const);
PyAutoFunction_Register(getFullBaseMatrix, Matrix4, 1, cons);

