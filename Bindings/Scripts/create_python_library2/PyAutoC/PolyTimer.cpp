
PyAutoFunction_RegisterVoid(Pause, 1, bool);
PyAutoFunction_Register(isPaused, bool, 0);
PyAutoFunction_Register(getTicks, int, 0);
PyAutoFunction_RegisterVoid(Update, 1, unsigned);
PyAutoFunction_RegisterVoid(Reset, 0);
PyAutoFunction_Register(hasElapsed, bool, 0);
PyAutoFunction_Register(getElapsedf, Number, 0);
PyAutoFunction_RegisterVoid(setTimerInterval, 1, int);

