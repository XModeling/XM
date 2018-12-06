//
// Created by peignier sergio on 29/01/2016.
//

#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include "TUsefullElements.h"

TUsefullElements::TUsefullElements(TModelComplexity maximalSize) {
    array = (TElement*) malloc(maximalSize * sizeof(TPointId));
    for (TPointId i = 0; i < maximalSize; i ++){
        array[i] = 0;
    }
    size = 0;
}


TUsefullElements::~TUsefullElements() {
    free(array);
}

void TUsefullElements::RemoveElementFromUsefulElementsList(TElement element){
    TDimId  i = 0;
    while( i < size && array[i] < element ) {
        i++;
    }
    TDimId sizeArrayToMoove = (TElement) (size - i - 1);
    if (size > i + 1){
        memmove( &array[i], &array[i+1], sizeArrayToMoove * sizeof(TElement));
    }
    size --;
}

void TUsefullElements::AddElementToUsefulElementsList(TElement element){
    TDimId  i = 0;
    while( i < size && array[i] < element ){
        i ++;
    }
    TDimId sizeArrayToMoove = size - i;
    if (size > i ){
        memmove( &array[i + 1], &array[i], sizeArrayToMoove * sizeof(TElement));
    }
    array[i] = element;
    size ++;
}

void TUsefullElements::CloneOtherElementsArray(TUsefullElements *other){
    for(TDimId i = 0; i < other->size; i++) {
        array[i] = other->array[i];
    }
    size = other->size;
}

void TUsefullElements::Print(){
    for(TElement i=0; i<size;i++){
        printf("%i %i |",i,array[i]);
    }
    if(size) printf("\n");
}
