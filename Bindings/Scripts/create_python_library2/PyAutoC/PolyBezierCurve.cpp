
PyAutoFunction_Register(getNumControlPoints, int, 0);
PyAutoFunction_Register(addControlPoint3dWithHandles, see, 9, void, Number, Number, Number, Number, Number, Number, Number, Number);
PyAutoFunction_RegisterVoid(addControlPoint3dWithHandles, 9, Number, Number, Number, Number, Number, Number, Number, Number, Number);
PyAutoFunction_RegisterVoid(addControlPoint3d, 3, Number, Number, Number);
PyAutoFunction_RegisterVoid(addControlPoint2dWithHandles, 6, Number, Number, Number, Number, Number, Number);
PyAutoFunction_RegisterVoid(addControlPoint2d, 2, Number, Number);
PyAutoFunction_Register(getPointAt, Vector3, 1, Number);
PyAutoFunction_Register(getPointBetween, Vector3, 3, Number, BezierPoin, BezierPoin);
PyAutoFunction_RegisterVoid(clearControlPoints, 0);
PyAutoFunction_Register(getYValueAtX, Number, 1, Number);
PyAutoFunction_Register(getTValueAtX, Number, 1, Number);
PyAutoFunction_RegisterVoid(removePoint, 1, BezierPoin);
PyAutoFunction_RegisterVoid(setHeightCacheResolution, 1, Number);
PyAutoFunction_RegisterVoid(rebuildHeightCache, 0);
PyAutoFunction_RegisterVoid(recalculateDistances, 0);

