#include "SubCMedians_def.h"
#include "CPrng.h"
#include "CSubCMediansClust.h"
#include "SubCMedians_def_PyC.h"
#ifdef __cplusplus
extern "C" {
#endif
#include <Python.h>//include the "Python.h" header before any other include
#include <stdio.h>
#include <stdlib.h>
#include <string>
#include <math.h>
#include <zlib.h>
#include <errno.h>

#define PyDIMID     0
#define PyDIMWEIGHT 1
#define PyDIMPOS    2

#define PyPOINTWEIGHT 0
#define PyPOINTINDEX  1
#define PyPOINTGROUPID 2
#define PyPOINTCLASSID 3
#define PyPOINTDISPERSION 4
#define PyNBPOINTSINCLUSTER 5
#define PyLASTDESCRIPTORINPOINT 6

#define PyCLASSINPOINTDUAL 0
#define PyCLUSTERINPOINTDUAL 1


#define PyDISPERSIONFEATURE 0
#define PyKFEATURE 1
#define PyNBCOREPOINTS 2
#define PyNBCLUSTERS 3
#define PyMEANDIMCOREPOINTS 4
#define PyMEANDIMCLUSTERS 5
#define PyMEANATOMCOREPOINTS 6
#define PyMEANATOMCLUSTERS 7
#define PyMEANATOMDIMCOREPOINTS 8
#define PyMEANATOMDIMCLUSTERS 9
#define PyCOVERAGE 10

#define NAME_CAPSULE_SubCMediansCLUST   "SubCMediansClust"
#define NAME_CAPSULE_SubCMediansPOINTARRAY   "arraySubCMediansPoint"
#define NAME_CAPSULE_SubCMediansPOINT "SubCMediansPoint"
#define NAME_CAPSULE_PRNG "prng"

static CSubCMediansClust* SubCMediansPythonToC(PyObject* args){
	CSubCMediansClust* SubCMedians;
	PyObject* capsule;
	if (!PyArg_ParseTuple(args, "O", &capsule)){
		return NULL;
	}
	SubCMedians = (CSubCMediansClust*) PyCapsule_GetPointer(capsule,NAME_CAPSULE_SubCMediansCLUST);
	return SubCMedians;
}
static PyObject*  PrintSubCMediansClustModel(PyObject* self, PyObject* args){
    CSubCMediansClust*  SubCMedians = SubCMediansPythonToC(args);
    SubCMedians->a_G->Print();
    Py_INCREF(Py_None);
    return Py_None;
}

void SubCMediansPointDestructor(PyObject* capsule){
	CSubCMediansPoint* SubCMediansPoint = (CSubCMediansPoint*) PyCapsule_GetPointer(capsule,NAME_CAPSULE_SubCMediansPOINT);
    delete SubCMediansPoint;
}

void CprngDestructor(PyObject* capsule){
    CPrng* prng;
    prng = (CPrng*) PyCapsule_GetPointer(capsule,NAME_CAPSULE_PRNG);
    delete prng;
}

void SubCMediansArrayPointDestructor(PyObject* capsule){
	CArraySubCMediansPoint* arraySubCMediansPoint = (CArraySubCMediansPoint*) PyCapsule_GetPointer(capsule,NAME_CAPSULE_SubCMediansPOINTARRAY);
    delete arraySubCMediansPoint;
}

void SubCMediansCapsuleDestructor(PyObject* capsule){
	CSubCMediansClust* SubCMedians = (CSubCMediansClust*) PyCapsule_GetPointer(capsule,NAME_CAPSULE_SubCMediansCLUST);
	delete SubCMedians;
}

static PyObject* DeleteSubCMediansTranslator(PyObject* self, PyObject* args){
	CSubCMediansClust*  SubCMedians = SubCMediansPythonToC(args);
	delete SubCMedians;
	Py_INCREF(Py_None);
	return Py_None;
	}
		
static PyObject*  GetParameters(PyObject* self,PyObject* args){
	CSubCMediansClust* SubCMedians    = SubCMediansPythonToC(args);
	return Py_BuildValue("hhhhkhhhhH", SubCMedians->a_Kmax, SubCMedians->a_maxNbDims, SubCMedians->a_H, SubCMedians->a_M,
                         SubCMedians->a_seed,SubCMedians->a_optionGenerateDeletion,SubCMedians->a_optionGenerateInsertion,
						 SubCMedians->a_optionFIFO,SubCMedians->a_optionTrainWithLatestObject,
						 SubCMedians->a_optionDoNotOptimizeIfDistanceDecrease);
}

static PyObject* CreatArraySubCMediansPoint(PyObject* self, PyObject* args){
    PyObject* capsule;
    CPrng* prng;
	TModelComplexity nbElements;
	TModelComplexity elementsSize;
	if (!PyArg_ParseTuple(args, "Ohh",&capsule,&nbElements,&elementsSize)){
		return NULL;
	}
    prng = (CPrng*) PyCapsule_GetPointer(capsule,NAME_CAPSULE_PRNG);
    CArraySubCMediansPoint* arraySubCMediansPoint = new CArraySubCMediansPoint(nbElements, elementsSize,prng);
	PyObject* capsuleReturn = PyCapsule_New(arraySubCMediansPoint,NAME_CAPSULE_SubCMediansPOINTARRAY, SubCMediansArrayPointDestructor);
	return capsuleReturn;
}

static PyObject* CreatSubCMediansPoint(PyObject* self, PyObject* args){
    PyObject* capsule;
    CPrng* prng;
	TModelComplexity elementsSize;
	if (!PyArg_ParseTuple(args, "Oh", &capsule,&elementsSize)){
		return NULL;
	}
    prng = (CPrng*) PyCapsule_GetPointer(capsule,NAME_CAPSULE_PRNG);
    CSubCMediansPoint* SubCMediansPoint = new CSubCMediansPoint(elementsSize, prng);
	PyObject* capsuleReturn = PyCapsule_New(SubCMediansPoint,NAME_CAPSULE_SubCMediansPOINT, SubCMediansPointDestructor);
	return capsuleReturn;
}

static PyObject* CreatPrng(PyObject* self, PyObject* args){
    TSeed seed;
    if (!PyArg_ParseTuple(args, "k",&seed)){
        return NULL;
    }
    CPrng* prng = new CPrng(seed);
    PyObject* capsuleReturn = PyCapsule_New(prng,NAME_CAPSULE_PRNG, CprngDestructor);
    return capsuleReturn;
}

static PyObject* CreatSubCMediansTranslator(PyObject* self, PyObject* args){
	TPointId             H;
	TPointId             M;
	TModelComplexity     Kmax;
	TDimId               maxNbDims;
	TSeed                seed;
    TOption              optionGenerateDeletion;
    TOption              optionGenerateInsertion;
	TOption              optionFIFO;
	TOption              optionTrainWithLatestObject;
	TOption              optionDoNotOptimizeIfDistanceDecrease;
	TModelComplexity     lambda;
	TModelComplexity     mu;
	if (!PyArg_ParseTuple(args, "hhhhkhhhhhhh",&Kmax, &maxNbDims, &H, &M, &seed, &optionGenerateDeletion, &optionGenerateInsertion,&optionFIFO,&optionTrainWithLatestObject,&optionDoNotOptimizeIfDistanceDecrease,&lambda,&mu)){
		return NULL;
	}
	CSubCMediansClust* SubCMedians = new CSubCMediansClust(Kmax, maxNbDims, H, M, seed, optionGenerateDeletion, optionGenerateInsertion, optionFIFO, optionTrainWithLatestObject,optionDoNotOptimizeIfDistanceDecrease,lambda,mu);
	PyObject* capsule = PyCapsule_New(SubCMedians,NAME_CAPSULE_SubCMediansCLUST, SubCMediansCapsuleDestructor);
	return capsule;
}

static PyObject* SetParameters(PyObject* self, PyObject* args){
	PyObject* capsule;
	CSubCMediansClust* SubCMedians;
	TPointId             H;
	TPointId             M;
	TModelComplexity     Kmax;
	TDimId               maxNbDims;
	TSeed                seed;
    TOption              optionGenerateDeletion;
    TOption              optionGenerateInsertion;
	TOption              optionFIFO;
	TOption              optionTrainWithLatestObject;
	TOption              optionDoNotOptimizeIfDistanceDecrease;
	TModelComplexity     lambda;
	TModelComplexity     mu;
	if (PyArg_ParseTuple(args, "Ohhhhkhhhhhhh",&capsule,&Kmax, &maxNbDims, &H, &M, &seed, &optionGenerateDeletion, &optionGenerateInsertion,&optionFIFO,&optionTrainWithLatestObject,&optionDoNotOptimizeIfDistanceDecrease,&lambda,&mu)){
		SubCMedians = (CSubCMediansClust*) PyCapsule_GetPointer(capsule,NAME_CAPSULE_SubCMediansCLUST);
        //printf("HHHHHH %i, %i \n",SubCMedians->a_H ,H);
		SubCMedians->a_H = H;
		SubCMedians->a_M = M;
		SubCMedians->a_Kmax = Kmax;
		SubCMedians->a_maxNbDims = maxNbDims;
		SubCMedians->a_seed = seed;
		SubCMedians->a_p_prng->setSeed(seed);
        SubCMedians->a_optionGenerateInsertion = optionGenerateInsertion;
        SubCMedians->a_optionGenerateDeletion = optionGenerateDeletion;
		SubCMedians->a_optionFIFO = optionFIFO;
		SubCMedians->a_optionTrainWithLatestObject = optionTrainWithLatestObject;
		SubCMedians->a_optionDoNotOptimizeIfDistanceDecrease = optionDoNotOptimizeIfDistanceDecrease;
        SubCMedians->a_lambda = lambda;
        SubCMedians->a_mu = mu;
        //printf("%i %i %i %lu %i %i %i %i %i\n",SubCMedians->a_H,SubCMedians->a_M,SubCMedians->a_Kmax, SubCMedians->a_seed,SubCMedians->a_optionGenerateInsertion,SubCMedians->a_optionGenerateDeletion,SubCMedians->a_optionFIFO, SubCMedians->a_optionTrainWithLatestObject, SubCMedians->a_optionDoNotOptimizeIfDistanceDecrease);
        //printf("reallocation ok\n");
		return Py_BuildValue("i", 1);
	}
	else{
		return NULL;
	}
}

static void C2PySubCMediansPoint(CSubCMediansPoint* SubCMediansPoint,PyObject* object){
	PyList_SetItem(object,(Py_ssize_t) PyPOINTWEIGHT,  PyInt_FromLong((long) SubCMediansPoint->weight ));
	PyList_SetItem(object,(Py_ssize_t) PyPOINTINDEX,  PyInt_FromLong((long) SubCMediansPoint->id ));
	PyList_SetItem(object,(Py_ssize_t) PyPOINTGROUPID,  PyInt_FromLong((long) SubCMediansPoint->groupId  ));
	PyList_SetItem(object,(Py_ssize_t) PyPOINTCLASSID,  PyInt_FromLong((long) SubCMediansPoint->classId  ));
	PyList_SetItem(object,(Py_ssize_t) PyPOINTDISPERSION,  PyFloat_FromDouble((double) SubCMediansPoint->dispersionToGroup));
	PyList_SetItem(object,(Py_ssize_t) PyNBPOINTSINCLUSTER, PyInt_FromLong((long) SubCMediansPoint->nbPointsInCluster));
	for (TDimId j = 0; j < SubCMediansPoint->usefullDims->size; j++){
		TDimId coordDim          = SubCMediansPoint->usefullDims->array[j];
		TWeight coordWeight      = SubCMediansPoint->dimWeights[coordDim];
		TPosition coordPos       = SubCMediansPoint->positions[coordDim];
		PyObject* coordinate = (PyObject*) PyList_GetItem( object, (Py_ssize_t)  (PyLASTDESCRIPTORINPOINT + j));
		PyList_SetItem(coordinate, (Py_ssize_t) PyDIMID, PyInt_FromLong((long) coordDim) );
		PyList_SetItem(coordinate, (Py_ssize_t) PyDIMWEIGHT, PyInt_FromLong((long) coordWeight) );
		PyList_SetItem(coordinate, (Py_ssize_t) PyDIMPOS, PyFloat_FromDouble((double) coordPos) );
	}
}

static void FillSubCMediansPointUsingPyList(PyListObject** object, CSubCMediansPoint* SubCMediansPoint){
    SubCMediansPoint->weight            = (TPointId) PyInt_AsLong(PyList_GetItem( (PyObject*) object , (Py_ssize_t) PyPOINTWEIGHT));
    SubCMediansPoint->id                = (TPointId) PyInt_AsLong(PyList_GetItem( (PyObject*) object , (Py_ssize_t) PyPOINTINDEX));
    SubCMediansPoint->groupId           = (TDimId) PyInt_AsLong(PyList_GetItem( (PyObject*) object , (Py_ssize_t) PyPOINTGROUPID));
    SubCMediansPoint->classId           = (TDimId) PyInt_AsLong(PyList_GetItem( (PyObject*) object , (Py_ssize_t) PyPOINTCLASSID));
    SubCMediansPoint->dispersionToGroup = (TDispersion) PyFloat_AsDouble(PyList_GetItem( (PyObject*) object , (Py_ssize_t) PyPOINTDISPERSION));
    SubCMediansPoint->nbPointsInCluster = (TDimId) PyInt_AsLong(PyList_GetItem( (PyObject*) object , (Py_ssize_t) PyNBPOINTSINCLUSTER));
    //printf("groupID %i classID %i classID %lu\n",SubCMediansPoint->groupId,SubCMediansPoint->classId,(long)PyInt_AsLong(PyList_GetItem( (PyObject*) object , (Py_ssize_t) PyPOINTCLASSID)));
    SubCMediansPoint->usefullDims->size = 0;
    TDimId size_to_modify = MIN((TPointId) PyList_Size((PyObject*) object) - PyLASTDESCRIPTORINPOINT , SubCMediansPoint->maxNbDims);
    for (TDimId j = PyLASTDESCRIPTORINPOINT ; j < size_to_modify+PyLASTDESCRIPTORINPOINT ; j++){
        PyListObject* coordinate = (PyListObject*) PyList_GetItem( (PyObject*) object, (Py_ssize_t) j);
        TDimId coordDim          = (TDimId) PyInt_AsLong(PyList_GetItem( (PyObject*) coordinate , (Py_ssize_t) PyDIMID ));
        TWeight coordWeight      = (TWeight) PyInt_AsLong(PyList_GetItem( (PyObject*) coordinate , (Py_ssize_t) PyDIMWEIGHT));
        TPosition coordPos       = (TDispersion) PyFloat_AsDouble(PyList_GetItem( (PyObject*) coordinate, (Py_ssize_t) PyDIMPOS ));
        SubCMediansPoint->usefullDims->AddElementToUsefulElementsList(coordDim);
        SubCMediansPoint->dimWeights[coordDim] = coordWeight;
        SubCMediansPoint->positions[coordDim] = coordPos;
        //printf("%i %i %lg %i\n",coordDim,coordWeight,coordPos, j - PyLASTDESCRIPTORINPOINT - 1);
    }
	SubCMediansPoint->ComputeDistanceToBarycenter();
	SubCMediansPoint->dispersionToGroup = SubCMediansPoint->dispersionToBarycenter;
	//SubCMediansPoint->Print();
	//printf("%f\n",SubCMediansPoint->dispersionToBarycenter);
}

static PyObject* Py2CSubCMediansPointTranslator(PyObject* self, PyObject* args){
	PyListObject** object = nullptr ;
	PyObject* capsuleSubCMediansPoint = nullptr ;
	CSubCMediansPoint* SubCMediansPoint = nullptr;
	if (PyArg_ParseTuple(args, "OO",&object, &capsuleSubCMediansPoint)){
		SubCMediansPoint = (CSubCMediansPoint*)  PyCapsule_GetPointer(capsuleSubCMediansPoint,NAME_CAPSULE_SubCMediansPOINT);
        FillSubCMediansPointUsingPyList(object, SubCMediansPoint);
		return Py_BuildValue("i", 1);
	}
	return NULL;
}

static PyObject* PrintSubCMediansPoint(PyObject* self, PyObject* args){
    PyObject* capsuleSubCMediansPoint = nullptr ;
    CSubCMediansPoint* SubCMediansPoint = nullptr;
    if (PyArg_ParseTuple(args, "O", &capsuleSubCMediansPoint)){
        SubCMediansPoint = (CSubCMediansPoint*)  PyCapsule_GetPointer(capsuleSubCMediansPoint,NAME_CAPSULE_SubCMediansPOINT);
        SubCMediansPoint->Print();
        return Py_BuildValue("i", 1);
    }
    return NULL;
}

static PyObject* Py2CArraySubCMediansPointTranslator(PyObject* self, PyObject* args){
	PyListObject***            array = nullptr ;
	PyObject* capsuleArraySubCMediansPoint = nullptr ;
	CArraySubCMediansPoint* arraySubCMediansPoint = nullptr;
	if (PyArg_ParseTuple(args, "OO",&array, &capsuleArraySubCMediansPoint)){
		arraySubCMediansPoint = (CArraySubCMediansPoint*)  PyCapsule_GetPointer(capsuleArraySubCMediansPoint,NAME_CAPSULE_SubCMediansPOINTARRAY);
		arraySubCMediansPoint->usefullPoints->size = 0;
        arraySubCMediansPoint->emptyPoints->size = 0;
		//arraySubCMediansPoint->size = 0;
        TPointId size_to_modify = MIN((TPointId) PyList_Size((PyObject*) array),arraySubCMediansPoint->sizeMax);
		for (TPointId i = 0; i < size_to_modify; i++) {
			//printf("%i\n",i);
			PyListObject **object = (PyListObject **) PyList_GetItem((PyObject *) array, (Py_ssize_t) i);
			CSubCMediansPoint *SubCMediansPoint = arraySubCMediansPoint->array[i];
			FillSubCMediansPointUsingPyList(object, SubCMediansPoint);
			//arraySubCMediansPoint->size ++;
			arraySubCMediansPoint->usefullPoints->array[i] = i;
			arraySubCMediansPoint->usefullPoints->size++;

		}
		return Py_BuildValue("i", 1);
	}
	return NULL;
	
}
static PyObject* EmptyModel(PyObject* self, PyObject* args){
	CSubCMediansClust* SubCMedians = SubCMediansPythonToC(args);
	SubCMedians->Empty();
	return Py_BuildValue("i", 1);
}

static PyObject* ClonePyArrayIntoSubCMediansClust(PyObject* self, PyObject* args){
	PyListObject***            array = nullptr ;
	PyObject* capsuleSubCMediansClust = nullptr ;
	if (PyArg_ParseTuple(args, "OO",&array, &capsuleSubCMediansClust)){
		CSubCMediansClust* SubCMedians = (CSubCMediansClust*)  PyCapsule_GetPointer(capsuleSubCMediansClust,NAME_CAPSULE_SubCMediansCLUST);
		SubCMedians->Empty();
		TPointId size_to_modify = (TPointId) PyList_Size((PyObject*) array);
		for (TPointId i = 0; i < size_to_modify; i++) {
			PyListObject **object = (PyListObject **) PyList_GetItem((PyObject *) array, (Py_ssize_t) i);
			TPointId pointId = (TPointId) PyInt_AsLong(PyList_GetItem( (PyObject*) object , (Py_ssize_t) PyPOINTINDEX));
			for (TDimId j = PyLASTDESCRIPTORINPOINT; j < (TPointId) PyList_Size((PyObject*) object); j++){
				PyListObject* coordinate = (PyListObject*) PyList_GetItem( (PyObject*) object, (Py_ssize_t) j);
				TWeight weight = PyInt_AsLong(PyList_GetItem( (PyObject*) coordinate , (Py_ssize_t) PyDIMWEIGHT ));;
				TDimId dimension = PyInt_AsLong(PyList_GetItem( (PyObject*) coordinate , (Py_ssize_t) PyDIMID ));;
				TPosition position = PyFloat_AsDouble(PyList_GetItem( (PyObject*) coordinate, (Py_ssize_t) PyDIMPOS ));
				for (TElement k = 0; k < weight; k++){
					SubCMedians->AddAtomicElement(pointId, dimension,position);
				}
			}
		}
		return Py_BuildValue("i", 1);
	}
	return NULL;
}

static PyObject* PrintArraySubCMediansPoint(PyObject* self, PyObject* args){
    PyObject* capsuleArraySubCMediansPoint = nullptr ;
    CArraySubCMediansPoint* SubCMediansPointArray = nullptr;
    if (PyArg_ParseTuple(args, "O", &capsuleArraySubCMediansPoint)){
        SubCMediansPointArray = (CArraySubCMediansPoint*)  PyCapsule_GetPointer(capsuleArraySubCMediansPoint,NAME_CAPSULE_SubCMediansPOINTARRAY);
        SubCMediansPointArray->Print();
        return Py_BuildValue("i", 1);
    }
    return NULL;
}

static PyObject* TrainOnInstanceImplTranslatorArray(PyObject* self, PyObject* args){
	PyObject* capsuleSubCMediansClust = nullptr;
	PyObject* capsuleArraySubCMediansPoint = nullptr;
	if (PyArg_ParseTuple(args, "OO",&capsuleSubCMediansClust, &capsuleArraySubCMediansPoint)){
		CSubCMediansClust* SubCMedians = (CSubCMediansClust*) PyCapsule_GetPointer(capsuleSubCMediansClust,NAME_CAPSULE_SubCMediansCLUST);
		CArraySubCMediansPoint* arraySubCMediansPoint = (CArraySubCMediansPoint*)  PyCapsule_GetPointer(capsuleArraySubCMediansPoint,NAME_CAPSULE_SubCMediansPOINTARRAY);
		for(TPointId i = 0 ; i < arraySubCMediansPoint->usefullPoints->size ; i ++){
			SubCMedians->TrainOnInstanceImpl(arraySubCMediansPoint->array[i]);
		}
		//printf("END PROPERLY TRAIN INSTANCE\n");
		return Py_BuildValue("i", 1);
	}
	return NULL;
}

static PyObject* TrainOnInstanceImplTranslator(PyObject* self, PyObject* args){
	PyObject* capsuleSubCMediansClust = nullptr;
	PyObject* capsuleSubCMediansPoint = nullptr;
	if (PyArg_ParseTuple(args, "OO",&capsuleSubCMediansClust, &capsuleSubCMediansPoint)){
		CSubCMediansClust* SubCMedians = (CSubCMediansClust*) PyCapsule_GetPointer(capsuleSubCMediansClust,NAME_CAPSULE_SubCMediansCLUST);
		CSubCMediansPoint* SubCMediansPoint = (CSubCMediansPoint*)  PyCapsule_GetPointer(capsuleSubCMediansPoint,NAME_CAPSULE_SubCMediansPOINT);
		SubCMedians->TrainOnInstanceImpl(SubCMediansPoint);
		return Py_BuildValue("i", 1);
	}
	return NULL;
}

static PyObject* ClusterizeArrayInstanceTranslator(PyObject* self, PyObject* args){
	//printf("START RUN CLUSTERING ON ARRAY INSTANCE \n");
	PyObject* capsuleSubCMediansClust = nullptr;
	PyObject* capsuleArraySubCMediansPoint = nullptr;
	CSubCMediansClust* SubCMedians = nullptr;
	CArraySubCMediansPoint* arraySubCMediansPoint = nullptr;
	if (PyArg_ParseTuple(args, "OO",&capsuleSubCMediansClust, &capsuleArraySubCMediansPoint)){
		SubCMedians = (CSubCMediansClust*) PyCapsule_GetPointer(capsuleSubCMediansClust,NAME_CAPSULE_SubCMediansCLUST);
		arraySubCMediansPoint = (CArraySubCMediansPoint*)  PyCapsule_GetPointer(capsuleArraySubCMediansPoint,NAME_CAPSULE_SubCMediansPOINTARRAY);
		SubCMedians->a_G->ComputeDistanceToArray(arraySubCMediansPoint);
		return Py_BuildValue("i", 1);
	}
	return NULL;
}

static PyObject* RunClusteringOnInstanceTranslator(PyObject* self, PyObject* args){
	//printf("START RUN CLUSTERING ON ARRAY INSTANCE \n");
	PyObject* capsuleSubCMediansClust = nullptr;
	PyObject* capsuleSubCMediansPoint = nullptr;
	if (PyArg_ParseTuple(args, "OO",&capsuleSubCMediansClust, &capsuleSubCMediansPoint)){
		CSubCMediansClust* SubCMedians = (CSubCMediansClust*) PyCapsule_GetPointer(capsuleSubCMediansClust,NAME_CAPSULE_SubCMediansCLUST);
		CSubCMediansPoint* SubCMediansPoint = (CSubCMediansPoint*)  PyCapsule_GetPointer(capsuleSubCMediansPoint,NAME_CAPSULE_SubCMediansPOINT);
		SubCMedians->a_G->ComputeDistanceToPoint(SubCMediansPoint);
		return Py_BuildValue("if", SubCMediansPoint->groupId,SubCMediansPoint->dispersionToGroup);
	}
	return NULL;
}

static PyObject*  UpdatePyListPointsUsingCArraySubCMediansPoint(PyObject* self, PyObject* args){
	PyListObject***            array = nullptr ;
	PyObject* capsuleArraySubCMediansPoint = nullptr ;
	CArraySubCMediansPoint* arraySubCMediansPoint = nullptr;
	if (PyArg_ParseTuple(args, "OO",&array, &capsuleArraySubCMediansPoint)){
		arraySubCMediansPoint = (CArraySubCMediansPoint*)  PyCapsule_GetPointer(capsuleArraySubCMediansPoint,NAME_CAPSULE_SubCMediansPOINTARRAY);
		for (TPointId i = 0; i < arraySubCMediansPoint->usefullPoints->size; i++){
			//printf("%i\n",i);
			PyObject* object = PyList_GetItem( (PyObject*) array, (Py_ssize_t) i);
			PyList_SetItem(object,(Py_ssize_t) PyPOINTWEIGHT,  PyInt_FromLong((long) arraySubCMediansPoint->array[i]->weight ));
			PyList_SetItem(object,(Py_ssize_t) PyPOINTINDEX,  PyInt_FromLong((long) arraySubCMediansPoint->array[i]->id ));
			PyList_SetItem(object,(Py_ssize_t) PyPOINTGROUPID,  PyInt_FromLong((long) arraySubCMediansPoint->array[i]->groupId  ));
			PyList_SetItem(object,(Py_ssize_t) PyPOINTDISPERSION,  PyFloat_FromDouble((double) arraySubCMediansPoint->array[i]->dispersionToGroup));
			PyList_SetItem(object,(Py_ssize_t) PyNBPOINTSINCLUSTER,  PyInt_FromLong((long) arraySubCMediansPoint->array[i]->nbPointsInCluster ));
		}
		return Py_BuildValue("i", 1);
	}
	return NULL;
}

static PyObject*  UpdatePyPointsUsingCSubCMediansPoint(PyObject* self, PyObject* args){
	PyObject*          object = nullptr ;
	PyObject* capsuleSubCMediansPoint = nullptr ;
	CSubCMediansPoint* SubCMediansPoint = nullptr;
	if (PyArg_ParseTuple(args, "OO",&object, &capsuleSubCMediansPoint)){
		SubCMediansPoint = (CSubCMediansPoint*)  PyCapsule_GetPointer(capsuleSubCMediansPoint,NAME_CAPSULE_SubCMediansPOINT);
		PyList_SetItem(object,(Py_ssize_t) PyPOINTWEIGHT,  PyInt_FromLong((long) SubCMediansPoint->weight ));
		PyList_SetItem(object,(Py_ssize_t) PyPOINTINDEX,  PyInt_FromLong((long) SubCMediansPoint->id ));
		PyList_SetItem(object,(Py_ssize_t) PyPOINTGROUPID,  PyInt_FromLong((long) SubCMediansPoint->groupId  ));
		PyList_SetItem(object,(Py_ssize_t) PyPOINTDISPERSION,  PyFloat_FromDouble((double) SubCMediansPoint->dispersionToGroup));
		PyList_SetItem(object,(Py_ssize_t) PyNBPOINTSINCLUSTER,  PyInt_FromLong((long) SubCMediansPoint->nbPointsInCluster ));
		return Py_BuildValue("i", 1);
	}
	return NULL;
}

static PyObject* C2PySubCMediansModelTranslator(PyObject* self, PyObject* args){
	PyListObject*** array = nullptr ;
	PyListObject*   sizesArray = nullptr ;
	PyObject* capsuleSubCMediansClust = nullptr ;
	if (PyArg_ParseTuple(args, "OOO",&array, &sizesArray,  &capsuleSubCMediansClust)){
		CSubCMediansClust* SubCMedians = (CSubCMediansClust*) PyCapsule_GetPointer(capsuleSubCMediansClust,NAME_CAPSULE_SubCMediansCLUST);
		PyList_SetItem((PyObject*) sizesArray,(Py_ssize_t) 0,  PyInt_FromLong((long) SubCMedians->a_G->usefullPoints->size ));
		for (TPointId i = 0; i < SubCMedians->a_G->usefullPoints->size; i++){
			PyObject* object = PyList_GetItem( (PyObject*) array, (Py_ssize_t) i);
			TPointId id_point = SubCMedians->a_G->usefullPoints->array[i];
			CSubCMediansPoint* SubCMediansPoint = SubCMedians->a_G->array[id_point];
			PyList_SetItem((PyObject*) sizesArray,(Py_ssize_t) (i + 1),  PyInt_FromLong((long) SubCMediansPoint->usefullDims->size + PyLASTDESCRIPTORINPOINT ));
			C2PySubCMediansPoint(SubCMediansPoint,object);
		}
		return Py_BuildValue("i", 1);
	}
	return NULL;
}

static PyObject* C2PySubCMediansModelModificationsTranslator(PyObject* self, PyObject* args){
	PyListObject*** array = nullptr ;
	PyListObject*   sizesArray = nullptr ;
	PyObject* capsuleSubCMediansClust = nullptr ;
	CSubCMediansClust* SubCMedians = nullptr;
	if (PyArg_ParseTuple(args, "OOO",&array, &sizesArray,  &capsuleSubCMediansClust)){
		
		SubCMedians = (CSubCMediansClust*) PyCapsule_GetPointer(capsuleSubCMediansClust,NAME_CAPSULE_SubCMediansCLUST);	
		PyList_SetItem((PyObject*) sizesArray,(Py_ssize_t) 0,  PyInt_FromLong((long) SubCMedians->a_G->modifedCorePoints->size ));
		for (TPointId i = 0; i < SubCMedians->a_G->modifedCorePoints->size; i++){
			PyObject* object = PyList_GetItem( (PyObject*) array, (Py_ssize_t) i);
			TPointId id_point = SubCMedians->a_G->modifedCorePoints->array[i];
			CSubCMediansPoint* SubCMediansPoint = SubCMedians->a_G->array[id_point];
			PyList_SetItem((PyObject*) sizesArray,(Py_ssize_t) (i + 1),  PyInt_FromLong((long) SubCMediansPoint->usefullDims->size + PyLASTDESCRIPTORINPOINT ));
			C2PySubCMediansPoint(SubCMediansPoint,object);
		}
		return Py_BuildValue("i", 1);
	}
	return NULL;
}

static PyObject* GenerateHorizontalClusterTransfertToList(PyObject* self, PyObject* args){
	PyObject* capsuleSubCMediansClust = nullptr;
	PyObject* object = nullptr ;
	TOption optionHorizontalClusterTranfert;
	if (PyArg_ParseTuple(args, "hOO",&optionHorizontalClusterTranfert,&capsuleSubCMediansClust, &object)){
		CSubCMediansClust* SubCMedians = (CSubCMediansClust*) PyCapsule_GetPointer(capsuleSubCMediansClust,NAME_CAPSULE_SubCMediansCLUST);
		TElement indexAtom = SubCMedians->ChooseModelPair(optionHorizontalClusterTranfert);
		TAtomicElement atom = SubCMedians->a_innerAtomicElements->array[indexAtom];
		TPointId pointId    = atom.pointId;
		//printf("%i \n", pointId);
		CSubCMediansPoint* SubCMediansPoint = SubCMedians->a_G->array[pointId];
		C2PySubCMediansPoint(SubCMediansPoint, object);
		return Py_BuildValue("i",SubCMediansPoint->usefullDims->size + PyLASTDESCRIPTORINPOINT);
	}
	return NULL;
}


static PyObject* GetFeaturesInList(PyObject* self, PyObject* args) {
    PyListObject* array = nullptr ;
    PyObject* capsuleSubCMediansClust = nullptr ;
    CSubCMediansClust* SubCMedians = nullptr;
    if (PyArg_ParseTuple(args, "OO",&array, &capsuleSubCMediansClust)){
        SubCMedians = (CSubCMediansClust*) PyCapsule_GetPointer(capsuleSubCMediansClust,NAME_CAPSULE_SubCMediansCLUST);
        SubCMedians->ComputeFeatures();
        PyList_SetItem((PyObject*)array,(Py_ssize_t) PyDISPERSIONFEATURE,  PyFloat_FromDouble((double) SubCMedians->a_features->dispersion ));
        PyList_SetItem((PyObject*)array,(Py_ssize_t) PyKFEATURE,  PyInt_FromLong((long) SubCMedians->a_features->K));
        PyList_SetItem((PyObject*)array,(Py_ssize_t) PyNBCOREPOINTS,  PyInt_FromLong((long) SubCMedians->a_features->numberOfCorePoints ));
        PyList_SetItem((PyObject*)array,(Py_ssize_t) PyNBCLUSTERS,  PyInt_FromLong((long) SubCMedians->a_features->numberOfClusters ));
        PyList_SetItem((PyObject*)array,(Py_ssize_t) PyMEANDIMCOREPOINTS,  PyFloat_FromDouble((double) SubCMedians->a_features->meanDimensionalityCorePoints ));
        PyList_SetItem((PyObject*)array,(Py_ssize_t) PyMEANDIMCLUSTERS,  PyFloat_FromDouble((double) SubCMedians->a_features->meanDimensionalityClusters ));
        PyList_SetItem((PyObject*)array,(Py_ssize_t) PyMEANATOMCOREPOINTS,  PyFloat_FromDouble((double) SubCMedians->a_features->meanAtomicElementsCorePoints ));
        PyList_SetItem((PyObject*)array,(Py_ssize_t) PyMEANATOMCLUSTERS,  PyFloat_FromDouble((double) SubCMedians->a_features->meanAtomicElementsClusters ));
        PyList_SetItem((PyObject*)array,(Py_ssize_t) PyMEANATOMDIMCOREPOINTS,  PyFloat_FromDouble((double) SubCMedians->a_features->meanAtomicElementsCorePointDimensions ));
        PyList_SetItem((PyObject*)array,(Py_ssize_t) PyMEANATOMDIMCLUSTERS,  PyFloat_FromDouble((double) SubCMedians->a_features->meanAtomicElementsClusterDimensions ));
        PyList_SetItem((PyObject*)array,(Py_ssize_t) PyCOVERAGE,  PyFloat_FromDouble((double) SubCMedians->a_features->coverage ));
        return Py_BuildValue("i", 1);
    }
    return NULL;

}

static PyObject* GetPointClassCluster(PyObject* self, PyObject* args){
    PyObject* capsuleSubCMediansClust = nullptr ;
    PyListObject* pointClassCluster = nullptr;
    CSubCMediansClust* SubCMedians = nullptr;
    TPointId pointInD = 0;
    if (PyArg_ParseTuple(args, "hOO",&pointInD,  &capsuleSubCMediansClust, &pointClassCluster)){
        SubCMedians = (CSubCMediansClust*) PyCapsule_GetPointer(capsuleSubCMediansClust,NAME_CAPSULE_SubCMediansCLUST);
        //printf("%i %i\n", SubCMedians->a_D->array[SubCMedians->a_D->usefullPoints->array[pointInD]]->classId,SubCMedians->a_D->array[SubCMedians->a_D->usefullPoints->array[pointInD]]->groupId);
        //printf("%lu %lu\n", (long)SubCMedians->a_D->array[SubCMedians->a_D->usefullPoints->array[pointInD]]->classId,(long)SubCMedians->a_D->array[SubCMedians->a_D->usefullPoints->array[pointInD]]->groupId);
        //SubCMedians->a_D->Print();
        PyList_SetItem((PyObject*)pointClassCluster, (Py_ssize_t) PyCLASSINPOINTDUAL, PyInt_FromLong((long) SubCMedians->a_D->array[SubCMedians->a_D->usefullPoints->array[pointInD]]->classId));
        PyList_SetItem((PyObject*)pointClassCluster, (Py_ssize_t) PyCLUSTERINPOINTDUAL, PyInt_FromLong((long) SubCMedians->a_D->array[SubCMedians->a_D->usefullPoints->array[pointInD]]->groupId));
        return Py_BuildValue("i", 1);
    }
    return NULL;
}

static PyObject* GetSizeOfD(PyObject* self, PyObject* args){
    CSubCMediansClust* SubCMedians = SubCMediansPythonToC(args);
    return Py_BuildValue("i", SubCMedians->a_D->usefullPoints->size);
}

static PyObject*  TrainOnCurrentD(PyObject* self, PyObject* args){
	CSubCMediansClust* SubCMedians = SubCMediansPythonToC(args);
	SubCMedians->UpdateGUsingD();
	return Py_BuildValue("i",1);
}

static PyObject*  InsertSubCMediansPointInDWithoutTraining(PyObject* self, PyObject* args){
	PyObject* capsuleSubCMediansClust = nullptr;
	PyObject* capsuleSubCMediansPoint = nullptr;
	if (PyArg_ParseTuple(args, "OO",&capsuleSubCMediansClust, &capsuleSubCMediansPoint)){
		CSubCMediansClust* SubCMedians = (CSubCMediansClust*) PyCapsule_GetPointer(capsuleSubCMediansClust,NAME_CAPSULE_SubCMediansCLUST);
		CSubCMediansPoint* SubCMediansPoint = (CSubCMediansPoint*)  PyCapsule_GetPointer(capsuleSubCMediansPoint,NAME_CAPSULE_SubCMediansPOINT);
		SubCMedians->InsertPointToD(SubCMediansPoint);
		return Py_BuildValue("i", 1);
	}
	return NULL;
}

static PyObject*  InsertSubCMediansPointArrayInDWithoutTraining(PyObject* self, PyObject* args){
    PyObject* capsuleSubCMediansClust = nullptr;
    PyObject* capsuleArraySubCMediansPoint = nullptr;
    if (PyArg_ParseTuple(args, "OO",&capsuleSubCMediansClust, &capsuleArraySubCMediansPoint)){
        CSubCMediansClust* SubCMedians = (CSubCMediansClust*) PyCapsule_GetPointer(capsuleSubCMediansClust,NAME_CAPSULE_SubCMediansCLUST);
        CArraySubCMediansPoint* arraySubCMediansPoint = (CArraySubCMediansPoint*)  PyCapsule_GetPointer(capsuleArraySubCMediansPoint,NAME_CAPSULE_SubCMediansPOINTARRAY);
        for(TPointId i = 0 ; i < arraySubCMediansPoint->usefullPoints->size; i ++){
            SubCMedians->InsertPointToD(arraySubCMediansPoint->array[arraySubCMediansPoint->usefullPoints->array[i]]);
        }
        return Py_BuildValue("i", 1);
    }
    return NULL;
}

static PyObject*  GetSubCMediansPointClusterId(PyObject* self, PyObject* args){
    PyObject* capsuleSubCMediansPoint = nullptr;
    if (PyArg_ParseTuple(args, "O", &capsuleSubCMediansPoint)){
        CSubCMediansPoint* SubCMediansPoint = (CSubCMediansPoint*)  PyCapsule_GetPointer(capsuleSubCMediansPoint,NAME_CAPSULE_SubCMediansPOINT);
        return Py_BuildValue("i", SubCMediansPoint->groupId);
    }
    return NULL;
}

static PyObject*  GetSubCMediansPointClassId(PyObject* self, PyObject* args){
    PyObject* capsuleSubCMediansPoint = nullptr;
    if (PyArg_ParseTuple(args, "O", &capsuleSubCMediansPoint)){
        CSubCMediansPoint* SubCMediansPoint = (CSubCMediansPoint*)  PyCapsule_GetPointer(capsuleSubCMediansPoint,NAME_CAPSULE_SubCMediansPOINT);
        return Py_BuildValue("i", SubCMediansPoint->classId);
    }
    return NULL;
}


static  PyObject*  CloneSubCMediansClustAtoB(PyObject* self, PyObject* args){
    PyObject* capsuleSubCMediansClustA = nullptr;
    PyObject* capsuleSubCMediansClustB = nullptr;
    if (PyArg_ParseTuple(args, "OO",&capsuleSubCMediansClustA, &capsuleSubCMediansClustB)){
        CSubCMediansClust* SubCMediansA = (CSubCMediansClust*) PyCapsule_GetPointer(capsuleSubCMediansClustA,NAME_CAPSULE_SubCMediansCLUST);
        CSubCMediansClust* SubCMediansB = (CSubCMediansClust*) PyCapsule_GetPointer(capsuleSubCMediansClustB,NAME_CAPSULE_SubCMediansCLUST);
        SubCMediansB->CloneOtherSubCMediansClust(SubCMediansA);
        return Py_BuildValue("i",1);
    }
    return NULL;
}

static PyObject* HorizontalDimPosTransfert(PyObject* self, PyObject* args){
    PyObject* capsuleSubCMediansClust = nullptr;
    TDimId dimId;
    TPosition position;
    if (PyArg_ParseTuple(args, "hfO",&dimId, &position,&capsuleSubCMediansClust)){
        CSubCMediansClust* SubCMedians = (CSubCMediansClust*) PyCapsule_GetPointer(capsuleSubCMediansClust,NAME_CAPSULE_SubCMediansCLUST);
        //printf("%i %f \n",dimId,position);
        //SubCMedians->a_G->Print();
        //SubCMedians->a_bestChanges->Print();
        SubCMedians->UpdateGUsingTransferedPair(dimId, position);
        //SubCMediansB->CloneOtherSubCMediansClust(SubCMediansA);
        return Py_BuildValue("i",1);
    }
    return NULL;
}

static PyObject*  ComputeDistanceKymerClustAtoB(PyObject* self, PyObject* args){
    PyObject* capsuleSubCMediansClustA = nullptr;
    PyObject* capsuleSubCMediansClustB = nullptr;
    if (PyArg_ParseTuple(args, "OO",&capsuleSubCMediansClustA, &capsuleSubCMediansClustB)){
        CSubCMediansClust* SubCMediansA = (CSubCMediansClust*) PyCapsule_GetPointer(capsuleSubCMediansClustA,NAME_CAPSULE_SubCMediansCLUST);
        CSubCMediansClust* SubCMediansB = (CSubCMediansClust*) PyCapsule_GetPointer(capsuleSubCMediansClustB,NAME_CAPSULE_SubCMediansCLUST);
        TDispersion distance_B2A = SubCMediansA->a_G->ComputeDistanceToArray(SubCMediansB->a_G);
        //TDispersion distance_A2B = SubCMediansB->a_G->ComputeDistanceToArray(SubCMediansA->a_G);
        //printf("%f %f\n",distance_B2A,distance_A2B);
        return Py_BuildValue("f",distance_B2A);
    }
    return NULL;
}

static PyObject* HorizontalClusterTransfert(PyObject* self, PyObject* args){
    PyObject* capsuleSubCMediansClust = nullptr;
    PyObject* capsuleSubCMediansPoint = nullptr;
    if (PyArg_ParseTuple(args, "OO",&capsuleSubCMediansPoint,&capsuleSubCMediansClust)){
        CSubCMediansClust* SubCMedians = (CSubCMediansClust*) PyCapsule_GetPointer(capsuleSubCMediansClust,NAME_CAPSULE_SubCMediansCLUST);
        CSubCMediansPoint* cluster = (CSubCMediansPoint*) PyCapsule_GetPointer(capsuleSubCMediansPoint,NAME_CAPSULE_SubCMediansPOINT);
        //printf("%i %f \n",dimId,position);
        //SubCMedians->a_G->Print();
        //SubCMedians->a_bestChanges->Print();
        SubCMedians->UpdateGUsingTransferedCluster(cluster);
        //SubCMediansB->CloneOtherSubCMediansClust(SubCMediansA);
        return Py_BuildValue("i",1);
    }
    return NULL;
}

static PyObject* GenerateHorizontalPairTransfert(PyObject* self, PyObject* args){
    PyObject* capsuleSubCMediansClust = nullptr;
    TOption optionHorizontalPairTranfert;
    if (PyArg_ParseTuple(args, "hO",&optionHorizontalPairTranfert,&capsuleSubCMediansClust)){
        CSubCMediansClust* SubCMedians = (CSubCMediansClust*) PyCapsule_GetPointer(capsuleSubCMediansClust,NAME_CAPSULE_SubCMediansCLUST);
        TElement indexAtom = SubCMedians->ChooseModelPair(optionHorizontalPairTranfert);
        TAtomicElement atomToErase = SubCMedians->a_innerAtomicElements->array[indexAtom];
        TDimId dimChanged = atomToErase.dimId;
        TPointId pointId    = atomToErase.pointId;
        TPosition oldPosition = SubCMedians->a_G->array[pointId]->positions[dimChanged];
        return Py_BuildValue("hf",dimChanged,oldPosition);
    }
    return NULL;
}

static PyObject* GenerateHorizontalClusterTransfert(PyObject* self, PyObject* args){
    PyObject* capsuleSubCMediansClust = nullptr;
    PyObject* capsuleSubCMediansPoint = nullptr;
    TOption optionHorizontalPairTranfert;
    if (PyArg_ParseTuple(args, "hOO",&optionHorizontalPairTranfert,&capsuleSubCMediansClust,&capsuleSubCMediansPoint)){
        CSubCMediansClust* SubCMedians = (CSubCMediansClust*) PyCapsule_GetPointer(capsuleSubCMediansClust,NAME_CAPSULE_SubCMediansCLUST);
        CSubCMediansPoint* cluster = (CSubCMediansPoint*) PyCapsule_GetPointer(capsuleSubCMediansPoint,NAME_CAPSULE_SubCMediansPOINT);
        TElement indexAtom = SubCMedians->ChooseModelPair(optionHorizontalPairTranfert);
        TAtomicElement atom = SubCMedians->a_innerAtomicElements->array[indexAtom];
        TPointId pointId    = atom.pointId;
        cluster->CloneOtherPoint(SubCMedians->a_G->array[pointId]);
        return Py_BuildValue("i",pointId);
    }
    return NULL;
}


static PyObject* GetDistanceBetweenPointAndCorePoint(PyObject* self, PyObject* args){
    PyObject* capsuleSubCMediansClust = nullptr;
    PyObject* capsuleSubCMediansPoint = nullptr;
    PyListObject*          array = nullptr ;
    TPointId cluster;
    if (PyArg_ParseTuple(args, "hOOO",&cluster,&capsuleSubCMediansClust, &capsuleSubCMediansPoint, &array)){
        CSubCMediansClust* SubCMedians = (CSubCMediansClust*) PyCapsule_GetPointer(capsuleSubCMediansClust,NAME_CAPSULE_SubCMediansCLUST);
        CSubCMediansPoint* point = (CSubCMediansPoint*)  PyCapsule_GetPointer(capsuleSubCMediansPoint,NAME_CAPSULE_SubCMediansPOINT);
        CSubCMediansPoint* corepoint  = SubCMedians->a_G->array[cluster];
        TDimId icp    = 0;
        TDimId ip     = 0;
        /*
        for(int i = 0; i < point->usefullDims->size;i++){
            printf("%i | ",point->usefullDims->array[i]);
        }
        printf("\n");
        for(int i = 0; i < corepoint->usefullDims->size;i++){
            printf("%i | ",corepoint->usefullDims->array[i]);
        }
        printf("\n");
         */
        for(TDimId i = 0;i < PyList_Size((PyObject *)array);i++){
            PyList_SetItem((PyObject *)array, (Py_ssize_t) i, PyFloat_FromDouble((double)0.0));
        }
        while(1){
            if(point->usefullDims->size <= ip && corepoint->usefullDims->size <= icp){
                break;
            }
            else if(point->usefullDims->size <= ip){
                while(corepoint->usefullDims->size > icp){
                    TPosition alea = (TPosition) SubCMedians->a_p_prng->gaussian(MEANDISTRUBUTION , STDDISTRUBUTION);
                    TDispersion tmpDisp = ABS(alea - corepoint->positions[corepoint->usefullDims->array[icp]]);
                    PyList_SetItem((PyObject *)array, (Py_ssize_t) corepoint->usefullDims->array[icp], PyFloat_FromDouble((double) tmpDisp));
                    icp++;
                }
                break;
            }
            else if (corepoint->usefullDims->size <= icp) {
                while(point->usefullDims->size > ip){
                    TDispersion tmpDisp = (TDispersion)ABS(point->positions[point->usefullDims->array[ip]] - BARYCENTERPOS);
                    PyList_SetItem((PyObject *)array, (Py_ssize_t) point->usefullDims->array[ip], PyFloat_FromDouble((double) tmpDisp));
                    ip++;
                }
                break;
            }
            if(point->usefullDims->array[ip] == corepoint->usefullDims->array[icp]){
                TDispersion tmpDisp = ABS(point->positions[point->usefullDims->array[ip]] - corepoint->positions[corepoint->usefullDims->array[icp]]);
                PyList_SetItem((PyObject *)array, (Py_ssize_t) point->usefullDims->array[ip], PyFloat_FromDouble((double) tmpDisp));
                ip++;
                icp++;
            }
            else if(point->usefullDims->array[ip] < corepoint->usefullDims->array[icp]){
                TDispersion tmpDisp = (TDispersion)ABS(point->positions[point->usefullDims->array[ip]] - BARYCENTERPOS);
                PyList_SetItem((PyObject *)array, (Py_ssize_t) point->usefullDims->array[ip], PyFloat_FromDouble((double) tmpDisp));
                ip++;
            }
            else if(point->usefullDims->array[ip] > corepoint->usefullDims->array[icp]){
                //printf("\t\tP %i %f :: CP %i %f\n",point->usefullDims->array[ip],point->positions[point->usefullDims->array[ip]],corepoint->usefullDims->array[icp],corepoint->positions[corepoint->usefullDims->array[icp]]);
                TPosition alea = (TPosition) SubCMedians->a_p_prng->gaussian(MEANDISTRUBUTION , STDDISTRUBUTION);
                TDispersion tmpDisp = ABS(alea - corepoint->positions[corepoint->usefullDims->array[icp]]);
                PyList_SetItem((PyObject *)array, (Py_ssize_t) corepoint->usefullDims->array[icp], PyFloat_FromDouble((double) tmpDisp));
                icp++;
            }
        }
        return Py_BuildValue("i", 1);
    }
    return NULL;
}

static PyMethodDef modevoevo_funcs[] = {
    {"generate_SubCMediansclust",(PyCFunction)CreatSubCMediansTranslator,METH_VARARGS, "Create a SubCMediansClust instance"},
    {"get_parameters",GetParameters,METH_VARARGS,  "Get SubCMediansClust instance parameters"},
    {"set_parameters",SetParameters,METH_VARARGS, "Set SubCMediansClust instance parameters"},
    {"delete_SubCMediansclust",DeleteSubCMediansTranslator,METH_VARARGS, "Free SubCMediansClust instance"},
    {"generate_array_SubCMedians_point",CreatArraySubCMediansPoint,METH_VARARGS,"Create a ArraySubCMediansPoint instance" },
    {"generate_SubCMedians_point",CreatSubCMediansPoint,METH_VARARGS,"Create a SubCMediansPoint instance"},
    {"print_SubCMedians_point",PrintSubCMediansPoint,METH_VARARGS,"Print SubCMediansPoint instance"},
    {"print_SubCMedians_point_array",PrintArraySubCMediansPoint,METH_VARARGS,"Print ArraySubCMediansPoint instance"},
    {"print_SubCMediansClust",PrintSubCMediansClustModel,METH_VARARGS,"Print SubCMediansClust instance"},
    {"generate_prng",CreatPrng,METH_VARARGS,"Create a PRNG instance"},
    {"py2C_convert_SubCMedianspointarray",Py2CArraySubCMediansPointTranslator,METH_VARARGS,"Convert PyList*** into SubCMedians points array" },
	{"clone_SubCMedians_point_from_list",ClonePyArrayIntoSubCMediansClust,METH_VARARGS,"Clone PyList*** into SubCMedians clust" },
    {"py2C_convert_SubCMedianspoint",Py2CSubCMediansPointTranslator,METH_VARARGS,"Convert PyList** into SubCMedians point" },
    {"train_model_with_SubCMedianspointarray",TrainOnInstanceImplTranslatorArray,METH_VARARGS,"Train model on SubCMedians point array instances"},
    {"train_model_with_SubCMedianspoint",TrainOnInstanceImplTranslator,METH_VARARGS,"Train model on SubCMedians point instance"},
    {"clusterize_SubCMedianspointarray_with_model",ClusterizeArrayInstanceTranslator,METH_VARARGS,"Clusterize SubCMedians point array instances with SubCMediansClust"},
    {"clusterize_SubCMedianspoint_with_model",RunClusteringOnInstanceTranslator,METH_VARARGS,"Clusterize SubCMedians point instance with SubCMediansClust"},
    {"update_Pystream_from_CarraySubCMedianspoint",UpdatePyListPointsUsingCArraySubCMediansPoint,METH_VARARGS,"Update stream PyList according to C arraySubCMediansPoints "},
    {"get_SubCMediansclust_model",C2PySubCMediansModelTranslator,METH_VARARGS,"Get the SubCMediansClust model as a PyList*** and a PyList containing the sizes"},
    {"update_PyPoint_from_CSubCMedianspoint",UpdatePyPointsUsingCSubCMediansPoint,METH_VARARGS,"Update data stream object with according to C SubCMediansPoint"},
    {"get_features",GetFeaturesInList,METH_VARARGS,"Get the may features of the actual model"},
    {"get_D_point_class_cluster",GetPointClassCluster,METH_VARARGS,"get the class and the cluster id of a point in D"},
    {"get_data_window_size",GetSizeOfD,METH_VARARGS,"get D dataset window size"},
	{"train_on_current_D",TrainOnCurrentD,METH_VARARGS,"train model G on current dataset chunk D"},
    {"insert_SubCMedians_point_in_D",InsertSubCMediansPointInDWithoutTraining,METH_VARARGS,"insert SubCMedians point in dataset chunk D"},
    {"insert_array_SubCMedians_point_in_D",InsertSubCMediansPointArrayInDWithoutTraining,METH_VARARGS,"insert every SubCMedians point belonging to SubCMedians point array in the dataset chunk D"},
    {"get_SubCMedians_cluster_id",GetSubCMediansPointClusterId,METH_VARARGS,"returns SubCMedians point cluster ID"},
    {"get_SubCMedians_class_id",GetSubCMediansPointClassId,METH_VARARGS,"returns SubCMedians point class ID"},
    {"get_distances_to_core_point", GetDistanceBetweenPointAndCorePoint, METH_VARARGS,"Modifies python array to get the distances between the point and the given cluster"},
    {"get_SubCMediansclust_model_modifications",C2PySubCMediansModelModificationsTranslator,METH_VARARGS,"returns SubCMediansclust modified corepoints"},
    {"clone_SubCMediansclust_A_to_B",CloneSubCMediansClustAtoB,METH_VARARGS,"clone a SubCMediansClut A into a SubCMediansClust B"},
    {"horizontal_dim_position_transfert", HorizontalDimPosTransfert,METH_VARARGS,"Produces K neighbor models inserting the transfered pair <dim, pos> and keep the best"},
    {"horizontal_cluster_transfert",HorizontalClusterTransfert,METH_VARARGS,"For each component of the transfered cluster calls the horizontal_dim_position_transfert function and keep the last better individual"},
    {"compute_distance_to_SubCMediansClust", ComputeDistanceKymerClustAtoB,METH_VARARGS,"Computes the distance between 2 SubCMediansClust models"},
    {"generate_horizontal_pair_transfert",GenerateHorizontalPairTransfert,METH_VARARGS,"Extract a pair <dimension, position> from the actual model as an horizontal pair transfert"},
    {"generate_horizontal_cluster_transfert",GenerateHorizontalClusterTransfert,METH_VARARGS,"Extract a cluster from the actual model as an horizontal cluster transfert"},
	{"generate_horizontal_cluster_transfert_in_list",GenerateHorizontalClusterTransfertToList,METH_VARARGS,"Extract a cluster from the actual model as an horizontal cluster transfert and put it into a list"},
	{"empty_SubCMediansClust",EmptyModel,METH_VARARGS,"Empty SubCMediansClust model"},
	{NULL, NULL, 0, NULL}
};
void initSubCMediansWrapper_c(void){
    Py_InitModule3("SubCMediansWrapper_c", modevoevo_funcs,
                   "SubCMediansWrapper module");
}



#ifdef __cplusplus
}  // extern "C"
#endif
