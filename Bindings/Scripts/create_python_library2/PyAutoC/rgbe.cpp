
PyAutoStruct_Register(rgbe_header_info);
PyAutoStruct_RegisterMember(rgbe_header_info, valid, int);
PyAutoStruct_RegisterMember(rgbe_header_info, indicate, *);
PyAutoStruct_RegisterMember(rgbe_header_info, listed, *);
PyAutoStruct_RegisterMember(rgbe_header_info, image, *);
PyAutoStruct_RegisterMember(rgbe_header_info, a, *);

PyAutoFunction_Register(RGBE_WriteHeader, int, 4, FIL, int, int, rgbe_header_inf);
PyAutoFunction_Register(RGBE_ReadHeader, int, 4, FIL, in, in, rgbe_header_inf);
PyAutoFunction_Register(RGBE_WritePixels, int, 3, FIL, floa, int);
PyAutoFunction_Register(RGBE_ReadPixels, int, 3, FIL, floa, int);
PyAutoFunction_Register(RGBE_WritePixels_RLE, int, 4, FIL, floa, int, int);
PyAutoFunction_Register(RGBE_ReadPixels_RLE, int, 4, FIL, floa, int, int);

