
PyAutoFunction_Register(Matrix4, inline, 16, Number, Number, Number, Number, Number, Number, Number, Number, Number, Number, Number, Number, Number, Number, Number, Number);
PyAutoFunction_RegisterVoid(identity, 2, memse, sizeo);
PyAutoFunction_Register(rotateVector, Vector3, 3, const, v, v);
PyAutoFunction_Register(getPosition, Vector3, 16, cons, n*, n*, n*, n*, n*, n*, n*, n*, n*, n*, n*, n*, n*, n*, n*);
PyAutoFunction_Register(multVector, Vector3, 3, const, v, v);
PyAutoFunction_Register(multVector, return, 1, v);
PyAutoFunction_RegisterVoid(setPosition, 10, Number, Number, Number, Numbe, Numbe, angle_, angle_, tr_, tr_, angle_);
PyAutoFunction_Register(transpose, Matrix4, 1, cons);
PyAutoFunction_Register(Inverse, Matrix4, 2, cons, int);

