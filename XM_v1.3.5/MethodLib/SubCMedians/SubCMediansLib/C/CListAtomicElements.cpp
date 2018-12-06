//
// Created by peignier sergio on 29/01/2016.
//

#include <stdlib.h>
#include "CListAtomicElements.h"

CListAtomicElements::CListAtomicElements(TModelComplexity nbElements,CPrng* prng){
    a_Kmax = nbElements;
    a_p_prng = prng;
    array = (TAtomicElement*) malloc(nbElements * sizeof(TAtomicElement));
    size = 0;
    for (TModelComplexity i = 0; i < nbElements; i ++){
        array[i] = {0,0,0.0};
    }
}

void CListAtomicElements::CloneCListAtomicElements(CListAtomicElements* other){
    a_Kmax = other->a_Kmax;
    size = other->size;
    for (TModelComplexity i = 0; i < size; i ++){
        array[i].pointId = other->array[i].pointId;
        array[i].dimId = other->array[i].dimId;
        array[i].pos = other->array[i].pos;
    }
}

CListAtomicElements::~CListAtomicElements(){
    free(array);
}

void CListAtomicElements::InsertElement(TAtomicElement insertedElement){
    assert(size < a_Kmax);
    array[size].pointId = insertedElement.pointId;
    array[size].dimId = insertedElement.dimId;
    array[size].pos = insertedElement.pos;
    size ++;
}

TElement CListAtomicElements::FindPointAndDimFromAtomicElementsList(TPointId pointID,TDimId dimID){
    for (TModelComplexity i = 0 ; i < size; i ++ ){
        if (array[i].pointId == pointID && array[i].dimId == dimID){
            return i;
        }
    }
    perror("No atom found: ERROR!\n");
    return -1;
}

void CListAtomicElements::DeleteElement(TModelComplexity idDeleteElement ){
    if (idDeleteElement < size - 1){
        array[idDeleteElement].pointId = array[size - 1].pointId;
        array[idDeleteElement].dimId = array[size - 1].dimId;
        array[idDeleteElement].pos = array[size - 1].pos;
    }
    size --;
}


void CListAtomicElements::ApplyDeletions(CChangesTracker* changesTracker){
    for (TModelComplexity i = 0; i < changesTracker->a_nbDeletions; i++){
        DeleteElement(changesTracker->a_deletionsID[i]);
    }
}

void CListAtomicElements::ApplyInsertions(CChangesTracker* changesTracker){
    for (TModelComplexity i = 0; i < changesTracker->a_nbInsertions; i++){
        InsertElement(changesTracker->a_insertions[i]);
    }
}

TModelComplexity CListAtomicElements::ChooseAtomIndex() {
    return (TModelComplexity) a_p_prng->uniform(0, size);
}

TAtomicElement CListAtomicElements::ChooseAtom() {
    return array[ChooseAtomIndex()];
}

void CListAtomicElements::Print() {
    for (TModelComplexity i = 0 ; i < size; i ++ ){
        printf("%hi %hi %f\n",array[i].pointId, array[i].dimId, array[i].pos);
    }
}

void CListAtomicElements::Empty(){
    size = 0;
}
