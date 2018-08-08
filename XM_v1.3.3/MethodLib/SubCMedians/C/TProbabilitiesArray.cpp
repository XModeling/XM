//
// Created by peignier sergio on 29/01/2016.
//

#include "TProbabilitiesArray.h"
#include "CPrng.h"
#include "CArraySubCMediansPoint.h"

TProbabilitiesArray::TProbabilitiesArray(TModelComplexity elementsSize) {
    array = (TProbability *) malloc((elementsSize + 1) * sizeof(TProbability));
    if (array) {
        for (TModelComplexity i = 0; i < elementsSize + 1; i++) {
            array[i] = 0;
        }
        size = 0;
    }
    else{
        perror("Error while using malloc!!!!!!!!!");
    }
}

TProbabilitiesArray::~TProbabilitiesArray(){
    free(array);
}

void TProbabilitiesArray::CloneOtherProbabilitiesArray(TProbabilitiesArray *other){
    for(TDimId i = 0; i < other->size; i++) {
        array[i] = other->array[i];
    }
    size = other->size;
}

void TProbabilitiesArray::ComputeProbabilitiesFromWeights(TUsefullElements* usefulIndexes, TModelComplexity* weightArray){
    TProbability cumProb = 0;
    array[0] =  0;
    TWeight weight= 0;
    for(TModelComplexity i = 0; i<usefulIndexes->size;i++){
        weight += weightArray[usefulIndexes->array[i]];
    }
    for(TModelComplexity i = 0 ; i < usefulIndexes->size ; i ++){
        TProbability localProba = (TProbability) (weightArray[usefulIndexes->array[i]] * 1.0 / weight);
        array[i+1] = cumProb + localProba;
        cumProb += localProba;
    }
    array[usefulIndexes->size] = (TProbability) 1.;
    size = (TModelComplexity) (usefulIndexes->size + 1);
}

void TProbabilitiesArray::ComputeProbabilitiesFromPointsWeights(TUsefullElements* usefulIndexes, CArraySubCMediansPoint* arrayPoints){
    TProbability cumProb = 0;
    array[0] =  0;
    TWeight weight= 0;
    for(TModelComplexity i = 0 ; i< usefulIndexes->size ; i++){
        weight +=arrayPoints->array[usefulIndexes->array[i]]->weight;
    }
    for (TModelComplexity i = 0 ; i < usefulIndexes->size ; i ++){
        TProbability localProba = (TProbability) (arrayPoints->array[usefulIndexes->array[i]]->weight * 1.0 / weight);
        array[i+1] = cumProb + localProba;
        cumProb += localProba;
    }
    array[usefulIndexes->size ] = (TProbability) 1.;
    size = (TModelComplexity) (usefulIndexes->size + 1);
}


void TProbabilitiesArray::ComputeProbabilitiesFromPointsNumberOfObjects(TUsefullElements* usefulIndexes, CArraySubCMediansPoint* arrayPoints, TProbability basalEmptyClusterProbability){
    TProbability cumProb = 0;
    array[0] =  0;
    TProbability weight= 0;
    for(TModelComplexity i = 0 ; i< usefulIndexes->size ; i++){
        weight +=arrayPoints->array[usefulIndexes->array[i]]->nbPointsInCluster + basalEmptyClusterProbability;
    }
    for (TModelComplexity i = 0 ; i < usefulIndexes->size ; i ++){
        TProbability localProba = (TProbability) ((arrayPoints->array[usefulIndexes->array[i]]->nbPointsInCluster + basalEmptyClusterProbability)* 1.0 / weight);
        array[i+1] = cumProb + localProba;
        cumProb += localProba;
    }
    array[usefulIndexes->size ] = (TProbability) 1.;
    size = (TModelComplexity) (usefulIndexes->size + 1);
}

void TProbabilitiesArray::ComputeProbabilitiesFromInversePointsNumberOfObjects(TUsefullElements* usefulIndexes, CArraySubCMediansPoint* arrayPoints,  TProbability basalEmptyClusterProbability){
    TProbability cumProb = 0;
    array[0] =  0;
    TProbability weight= 0;
    for(TModelComplexity i = 0 ; i< usefulIndexes->size ; i++){
        weight += 1./(arrayPoints->array[usefulIndexes->array[i]]->nbPointsInCluster + basalEmptyClusterProbability);
    }
    for (TModelComplexity i = 0 ; i < usefulIndexes->size ; i ++){
        TProbability localProba = (TProbability) ((weight *1.0/(arrayPoints->array[usefulIndexes->array[i]]->nbPointsInCluster + basalEmptyClusterProbability)));
        array[i+1] = cumProb + localProba;
        cumProb += localProba;
    }
    array[usefulIndexes->size ] = (TProbability) 1.;
    size = (TModelComplexity) (usefulIndexes->size + 1);
}

void TProbabilitiesArray::ComputeProbabilitiesFromAllPointsNumberOfPoints(CArraySubCMediansPoint* arrayPoints, TProbability basalEmptyClusterProbability){
    TProbability cumProb = 0;
    array[0] =  0;
    TProbability weight= 0;
    for(TModelComplexity i = 0 ; i< arrayPoints->sizeMax ; i++){
        weight +=arrayPoints->array[i]->nbPointsInCluster + basalEmptyClusterProbability;
    }
    for (TModelComplexity i = 0 ; i < arrayPoints->sizeMax ; i ++){
        TProbability localProba = (TProbability) ( (arrayPoints->array[i]->nbPointsInCluster + basalEmptyClusterProbability) * 1.0 / weight);
        array[i+1] = cumProb + localProba;
        cumProb += localProba;
    }
    array[arrayPoints->sizeMax ] = (TProbability) 1.;
    size = (TModelComplexity) (arrayPoints->sizeMax + 1);
}

void TProbabilitiesArray::ComputeProbabilitiesFromAllPointsInverseNumberOfPoints(CArraySubCMediansPoint* arrayPoints, TProbability basalEmptyClusterProbability){
    TProbability cumProb = 0;
    array[0] =  0;
    TProbability weight= 0;
    for(TModelComplexity i = 0 ; i< arrayPoints->sizeMax ; i++){
        weight += 1.0 / (arrayPoints->array[i]->nbPointsInCluster + basalEmptyClusterProbability);
    }
    for (TModelComplexity i = 0 ; i < arrayPoints->sizeMax ; i ++){
        TProbability localProba = (TProbability) (weight*1.0 / (arrayPoints->array[i]->nbPointsInCluster + basalEmptyClusterProbability));
        array[i+1] = cumProb + localProba;
        cumProb += localProba;
    }
    array[arrayPoints->sizeMax ] = (TProbability) 1.;
    size = (TModelComplexity) (arrayPoints->sizeMax + 1);
}

void TProbabilitiesArray::Print(){
    for(TElement i = 0; i < size; i++){
        printf("%f, ",array[i]);
    }
    printf("\n");
}