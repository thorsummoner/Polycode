
PyAutoFunction_RegisterVoid(utf8toWStr, 2, WSt, const);
PyAutoFunction_RegisterVoid(wstrToUtf8, 2, St, const);
PyAutoFunction_Register(size, size_t, 1, cons);
PyAutoFunction_Register(length, size_t, 1, cons);
PyAutoFunction_Register(substr, String, 2, size_t, size_t);
PyAutoFunction_Register(find_last_of, size_t, 3, const, size_t, po);
PyAutoFunction_Register(find_first_of, size_t, 3, const, size_t, po);
PyAutoFunction_Register(String, return, 1, content);
PyAutoFunction_Register(String, return, 1, content);
PyAutoFunction_Register(toLowerCase, String, 3, cons, const, int);
PyAutoFunction_Register(toNumber, Number, 0);
PyAutoFunction_Register(toInteger, int, 0);
PyAutoFunction_Register(IntToString, String, 1, int);
PyAutoFunction_Register(getDataSizeWithEncoding, see, 1, const);
PyAutoFunction_Register(getDataWithEncoding, see, 1, void);
PyAutoFunction_Register(getDataSizeWithEncoding, size_t, 2, int, int);
PyAutoFunction_Register(isNumber, bool, 0);
PyAutoFunction_Register(String, return, 1, Strin);
PyAutoFunction_Register(String, return, 1, Strin);

