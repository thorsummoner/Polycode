
PyAutoFunction_RegisterVoid(Play, 1, bool);
PyAutoFunction_RegisterVoid(Stop, 0);
PyAutoFunction_RegisterVoid(Update, 1, Number);
PyAutoFunction_RegisterVoid(Reset, 0);
PyAutoFunction_RegisterVoid(setSpeed, 1, Number);
PyAutoFunction_RegisterVoid(addBoneTrack, 1, BoneTrac);
PyAutoFunction_RegisterVoid(Play, 1, bool);
PyAutoFunction_RegisterVoid(Stop, 0);
PyAutoFunction_RegisterVoid(Reset, 0);
PyAutoFunction_RegisterVoid(Update, 0);
PyAutoFunction_RegisterVoid(setSpeed, 1, Number);
PyAutoFunction_RegisterVoid(setWeight, 1, Number);
PyAutoFunction_Register(getWeight, Number, 1, cons);
PyAutoFunction_RegisterVoid(loadSkeleton, 1, const);
PyAutoFunction_RegisterVoid(playAnimationByName, 4, const, Number, bool, bool);
PyAutoFunction_RegisterVoid(playAnimation, 4, SkeletonAnimatio, Number, bool, bool);
PyAutoFunction_RegisterVoid(setBaseAnimationByName, 1, const);
PyAutoFunction_RegisterVoid(setBaseAnimation, 1, SkeletonAnimatio);
PyAutoFunction_RegisterVoid(stopAllAnimations, 0);
PyAutoFunction_RegisterVoid(addAnimation, 2, const, const);
PyAutoFunction_RegisterVoid(stopAnimationByName, 1, const);
PyAutoFunction_RegisterVoid(stopAnimation, 1, SkeletonAnimatio);
PyAutoFunction_RegisterVoid(Update, 0);
PyAutoFunction_RegisterVoid(bonesVisible, 1, bool);

