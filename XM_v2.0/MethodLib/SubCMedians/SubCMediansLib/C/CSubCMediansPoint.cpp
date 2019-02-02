//
// Created by peignier sergio on 29/01/2016.
//

#include <stdlib.h>
#include <stdio.h>
#include "CSubCMediansPoint.h"

CSubCMediansPoint::CSubCMediansPoint(TModelComplexity elementsSize, CPrng *prng) {
    dimWeights = (TWeight *) malloc(elementsSize  * sizeof(TWeight));
    for (TDimId i = 0; i < elementsSize ; i ++){
        dimWeights[i] = 0;
    }

    positions  = (TPosition *) malloc(elementsSize * sizeof(TPosition));
    for (TDimId i = 0; i < elementsSize ; i ++){
        positions[i] = 0;
    }

    probaUsefullDim = new TProbabilitiesArray(elementsSize);
    usefullDims = new TUsefullElements(elementsSize);
    maxNbDims = elementsSize;
    weight = 0;
    id = 0;
    groupId = 0;
    classId = 0;
    dispersionToGroup = 0;
    dispersionToBarycenter = 0;
    nbPointsInCluster = 0;
    a_p_prng = prng;
}


CSubCMediansPoint::~CSubCMediansPoint(){
    free(dimWeights);
    free(positions);
    delete usefullDims;
    delete probaUsefullDim;
}


void CSubCMediansPoint::CloneOtherPoint(CSubCMediansPoint* other){
    weight = other->weight;
    id     = other->id;
    groupId = other->groupId;
    classId = other->classId;
    dispersionToGroup = other->dispersionToGroup;
    dispersionToBarycenter = other->dispersionToBarycenter;
    nbPointsInCluster = other->nbPointsInCluster;
    if (other->maxNbDims > maxNbDims){
        perror("Copy of large element into smaller element: ERROR!\n");
        printf("%hi into %hi\n",other->maxNbDims,maxNbDims);
    }
    usefullDims->CloneOtherElementsArray(other->usefullDims);
    probaUsefullDim->CloneOtherProbabilitiesArray(other->probaUsefullDim);
    for(TDimId i = 0; i < other->usefullDims->size; i++){
        dimWeights[other->usefullDims->array[i]]  = other->dimWeights[other->usefullDims->array[i]];
        positions[other->usefullDims->array[i]]   = other->positions[other->usefullDims->array[i]];
    }
}

TDimId CSubCMediansPoint::ChooseDim(TOption option) {
    probaUsefullDim->ComputeProbabilitiesFromWeights(usefullDims,dimWeights);
    TDimId dimChosen = usefullDims->array[a_p_prng->wheelOfFotune(probaUsefullDim->array, probaUsefullDim->size)];
    return dimChosen;
}

void CSubCMediansPoint::Print(){
    printf("-----------------------------------------------------\n");
    printf("printing point: %hi, groupID: %hi, classID: %hi, weight: %hi, maxNbDims: %hi\n",id,groupId, classId,weight,maxNbDims);
    printf("nbPointsInCluster : %hi, dispersionToGroup: %f\n",nbPointsInCluster,dispersionToGroup);
    for (TDimId i = 0; i < usefullDims->size ; i ++){
        printf("%hi %hi %f || ", usefullDims->array[i], dimWeights[usefullDims->array[i]], positions[usefullDims->array[i]]);
    }
    printf("\n");
    printf("-----------------------------------------------------\n");
}

void CSubCMediansPoint::Empty(){
    for (TDimId i = 0; i < usefullDims->size ; i ++){
        dimWeights[usefullDims->array[i]] = 0;
    }
    for (TDimId i = 0; i < usefullDims->size ; i ++){
        positions[usefullDims->array[i]] = 0;
    }
    while (usefullDims->size >0){
        TDimId dimToErase = usefullDims->array[0];
        usefullDims->RemoveElementFromUsefulElementsList(dimToErase);
    }
    weight = 0;
    dispersionToGroup = 0;
    dispersionToBarycenter = 0;
    nbPointsInCluster = 0;
}

void CSubCMediansPoint::ComputeDistanceToBarycenter(){
    dispersionToBarycenter=0;
    for(TDimId i = 0; i < usefullDims->size;i++){
        dispersionToBarycenter+=ABS(positions[usefullDims->array[i]]-BARYCENTERPOS);
    }
}

TDispersion CSubCMediansPoint::ComputeDistanceToPoint(CSubCMediansPoint* otherPoint){
    TDispersion dist = otherPoint->dispersionToBarycenter;
    for(TDimId i = 0; i<usefullDims->size;i++){
        TDimId d = usefullDims->array[i];
        dist -= ABS(otherPoint->positions[d]-BARYCENTERPOS);
        dist += ABS(otherPoint->positions[d] - positions[d]);
    }
    return dist;
}