
PyAutoFunction_Register(getMousePosition, Vector2, 0);
PyAutoFunction_Register(getKeyState, bool, 1, PolyKEY);
PyAutoFunction_Register(getJoystickButtonState, bool, 2, int, int);
PyAutoFunction_Register(getJoystickAxisValue, Number, 2, int, int);
PyAutoFunction_Register(getMouseDelta, Vector2, 0);
PyAutoFunction_Register(getMouseButtonState, bool, 1, int);
PyAutoFunction_Register(getNumJoysticks, int, 0);
PyAutoFunction_RegisterVoid(addJoystick, 1, unsigned);
PyAutoFunction_RegisterVoid(removeJoystick, 1, unsigned);
PyAutoFunction_RegisterVoid(joystickAxisMoved, 3, unsigned, float, unsigned);
PyAutoFunction_RegisterVoid(joystickButtonDown, 2, unsigned, unsigned);
PyAutoFunction_RegisterVoid(joystickButtonUp, 2, unsigned, unsigned);
PyAutoFunction_RegisterVoid(mouseWheelUp, 1, int);
PyAutoFunction_RegisterVoid(mouseWheelDown, 1, int);
PyAutoFunction_RegisterVoid(setMouseButtonState, 3, int, bool, int);
PyAutoFunction_RegisterVoid(setMousePosition, 3, int, int, int);
PyAutoFunction_RegisterVoid(setKeyState, 4, PolyKEY, wchar_t, bool, int);
PyAutoFunction_RegisterVoid(setDeltaPosition, 2, int, int);
PyAutoFunction_RegisterVoid(touchesBegan, 3, TouchInfo, st, int);
PyAutoFunction_RegisterVoid(touchesMoved, 3, TouchInfo, st, int);
PyAutoFunction_RegisterVoid(touchesEnded, 3, TouchInfo, st, int);
PyAutoFunction_RegisterVoid(clearInput, 0);

