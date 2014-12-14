
PyAutoFunction_RegisterVoid(setFromMatrix, 1, const);
PyAutoFunction_Register(Slerp, Quaternion, 4, Number, const, const, bool);
PyAutoFunction_Register(Dot, Number, 1, const);
PyAutoFunction_RegisterVoid(lookAt, 2, const, const);
PyAutoFunction_RegisterVoid(createFromMatrix, 4, const, int, static, t);
PyAutoFunction_Register(Squad, Quaternion, 6, Number, const, const, const, const, bool);
PyAutoFunction_Register(Inverse, Quaternion, 1, cons);
PyAutoFunction_RegisterVoid(set, 7, Number, Number, Number, Number, x*fInvNor, y*fInvNor, z*fInvNor);
PyAutoFunction_Register(InvSqrt, Number, 1, Number);
PyAutoFunction_RegisterVoid(fromAxes, 3, Number, Number, Number);
PyAutoFunction_RegisterVoid(fromAngleAxis, 2, const, const);
PyAutoFunction_Register(Vector3, return, 5, atan, *, asi, atan, *);
PyAutoFunction_RegisterVoid(createFromAxisAngle, 4, Number, Number, Number, Number);
PyAutoFunction_Register(createMatrix, Matrix4, 2, cons, *);
PyAutoFunction_Register(Vector3, return, 3, resul, resul, resul);

