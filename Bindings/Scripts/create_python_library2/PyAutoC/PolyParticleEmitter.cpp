
PyAutoFunction_RegisterVoid(setParticleCount, 1, unsigned);
PyAutoFunction_Register(getParticleCount, int, 1, cons);
PyAutoFunction_Register(getParticleLifetime, Number, 1, cons);
PyAutoFunction_Register(getDirectionDeviation, Vector3, 1, cons);
PyAutoFunction_Register(getEmitterSize, Vector3, 1, cons);
PyAutoFunction_Register(getGravity, Vector3, 1, cons);
PyAutoFunction_RegisterVoid(Render, 0);
PyAutoFunction_RegisterVoid(updateParticles, 0);
PyAutoFunction_RegisterVoid(rebuildParticles, 0);
PyAutoFunction_RegisterVoid(triggerParticles, 1, bool);
PyAutoFunction_RegisterVoid(enableParticleSystem, 1, bool);
PyAutoFunction_RegisterVoid(setUseFloorPlane, 1, bool);
PyAutoFunction_RegisterVoid(setFloorPlaneOffset, 1, Number);
PyAutoFunction_RegisterVoid(setFloorDamping, 1, Number);
PyAutoFunction_RegisterVoid(setParticlesInWorldSpace, 1, bool);
PyAutoFunction_Register(getParticlesInWorldSpace, bool, 1, cons);
PyAutoFunction_Register(getPerlinEnabled, bool, 1, cons);
PyAutoFunction_RegisterVoid(setPerlinValue, 1, const);
PyAutoFunction_Register(getPerlinValue, Vector3, 1, cons);
PyAutoFunction_Register(getParticleType, int, 1, cons);
PyAutoFunction_Register(getParticleSize, Number, 1, cons);
PyAutoFunction_Register(getParticleRotationSpeed, Vector3, 1, cons);
PyAutoFunction_Register(getParticleDirection, Vector3, 1, cons);
PyAutoFunction_Register(getLoopParticles, bool, 1, cons);
PyAutoFunction_Register(getNumSourceMeshes, int, 0);
PyAutoFunction_RegisterVoid(removeSourceMeshAtIndex, 1, int);
PyAutoFunction_RegisterVoid(applyClone, 3, Entit, bool, bool);

