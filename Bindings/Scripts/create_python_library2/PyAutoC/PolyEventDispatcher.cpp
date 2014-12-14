
PyAutoStruct_Register(EventEntry);
PyAutoStruct_RegisterMember(EventEntry, r, EventHandle);
PyAutoStruct_RegisterMember(EventEntry, eventCode, int);

PyAutoFunction_RegisterVoid(removeAllHandlers, 0);
PyAutoFunction_RegisterVoid(removeAllHandlersForListener, 1, EventHandle);
PyAutoFunction_Register(handleEvent, the, 2, metho, int);
PyAutoFunction_RegisterVoid(addEventListenerUnique, 2, EventHandle, int);
PyAutoFunction_Register(hasEventListener, bool, 2, EventHandle, int);
PyAutoFunction_RegisterVoid(removeEventListener, 2, EventHandle, int);
PyAutoFunction_RegisterVoid(__dispatchEvent, 2, Even, int);
PyAutoFunction_RegisterVoid(dispatchEvent, 2, Even, int);
PyAutoFunction_RegisterVoid(dispatchEventNoDelete, 2, Even, int);

