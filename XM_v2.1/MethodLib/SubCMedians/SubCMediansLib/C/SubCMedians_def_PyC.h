#ifndef PYC
#define PYC
#include <Python.h>
typedef struct {
	PyObject_HEAD
	void *pointer;
	const char *name;
	void *context;
	PyCapsule_Destructor destructor;
} PyCapsule;
#endif
