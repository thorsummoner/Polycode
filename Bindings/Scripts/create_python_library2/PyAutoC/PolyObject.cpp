
PyAutoFunction_Register(readNumber, bool, 2, String, Numbe);
PyAutoFunction_Register(if, else, 3, chil, false, in);
PyAutoFunction_Register(readInt, bool, 3, String, unsigne, in);
PyAutoFunction_Register(readString, bool, 2, String, Strin);
PyAutoFunction_Register(readBool, bool, 2, String, boo);
PyAutoFunction_Register(ObjectEntry, new, 0);
PyAutoFunction_Register(ObjectEntry, new, 0);
PyAutoFunction_Register(ObjectEntry, new, 0);
PyAutoFunction_Register(ObjectEntry, new, 0);
PyAutoFunction_Register(ObjectEntry, new, 0);
PyAutoFunction_Register(ObjectEntry, new, 0);
PyAutoFunction_Register(getTypedName, String, 1, cons);
PyAutoFunction_RegisterVoid(Clear, 0);
PyAutoFunction_Register(loadFromXML, bool, 1, const);
PyAutoFunction_Register(loadFromXMLString, bool, 1, const);
PyAutoFunction_RegisterVoid(saveToXML, 1, const);
PyAutoFunction_RegisterVoid(saveToBinary, 1, const);
PyAutoFunction_Register(loadFromBinary, bool, 1, const);
PyAutoFunction_RegisterVoid(createFromXMLElement, 2, TiXmlElemen, ObjectEntr);
PyAutoFunction_Register(parseEntryFromFile, bool, 1, ObjectEntr);
PyAutoFunction_Register(getKeyByIndex, String, 1, unsigned);
PyAutoFunction_Register(readFile, bool, 0);
PyAutoFunction_RegisterVoid(parseKeysFromObjectEntry, 1, ObjectEntr);
PyAutoFunction_RegisterVoid(writeEntryToFile, 1, ObjectEntr);
PyAutoFunction_Register(addKey, int, 1, const);
PyAutoFunction_Register(getKeyIndex, int, 1, const);
PyAutoFunction_Register(writeToFile, bool, 1, const);

