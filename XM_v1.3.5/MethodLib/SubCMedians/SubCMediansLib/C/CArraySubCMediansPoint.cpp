//
// Created by peignier sergio on 29/01/2016.
//

#include <stdlib.h>
#include "CArraySubCMediansPoint.h"

CArraySubCMediansPoint::CArraySubCMediansPoint(TModelComplexity nbElements, TModelComplexity elementsSize, CPrng* prng){
    a_p_prng = prng;
    pointedPoint = 0;
    usefullPoints = new TUsefullElements(nbElements);
    emptyPoints = new TUsefullElements(nbElements);
    modifedCorePoints = new TUsefullElements(nbElements);
    emptyPoints->size = nbElements;
    for (TModelComplexity i = 0 ; i < nbElements; i ++){
        emptyPoints->array[i] = i;
    }
    array = (CSubCMediansPoint**) malloc(nbElements * sizeof(CSubCMediansPoint*));
    sizeMax = nbElements;
    probaUsefullPoints = new TProbabilitiesArray(nbElements);
    weight = 0;
    for (TModelComplexity i = 0; i < nbElements; i++) {
        array[i] = new CSubCMediansPoint(elementsSize, a_p_prng);
        array[i]->id = i;
    }
}


void CArraySubCMediansPoint::CloneOtherArraySubCMediansPoint(CArraySubCMediansPoint* other){
    pointedPoint = other->pointedPoint;
    weight = other->weight;
    usefullPoints->CloneOtherElementsArray(other->usefullPoints);
    emptyPoints->CloneOtherElementsArray(other->emptyPoints);
    modifedCorePoints->CloneOtherElementsArray(other->modifedCorePoints);
    for(TPointId i = 0; i < other->usefullPoints->size; i++){
        array[usefullPoints->array[i]]->CloneOtherPoint(other->array[other->usefullPoints->array[i]]);
    }
    probaUsefullPoints->CloneOtherProbabilitiesArray(other->probaUsefullPoints);

}

CArraySubCMediansPoint::~CArraySubCMediansPoint(){
    for (TModelComplexity i = 0; i < sizeMax; i++){
        delete array[i];
    }
    free(array);
    delete probaUsefullPoints;
    delete usefullPoints;
    delete emptyPoints;
    delete modifedCorePoints;
    //delete fullPointsList;
}

void CArraySubCMediansPoint::RevertChange(TModelChange change){
	modifedCorePoints->RemoveElementFromUsefulElementsList(change.pointId);
    weight -= change.weightDelta;
    array[change.pointId]->weight -= change.weightDelta;
    array[change.pointId]->dimWeights[change.dimChanged] -= change.weightDelta;
    array[change.pointId]->positions[change.dimChanged] = change.oldPosition;
    if(array[change.pointId]->dimWeights[change.dimChanged] == 0){
        array[change.pointId]->usefullDims->RemoveElementFromUsefulElementsList(change.dimChanged);
    }
    if(array[change.pointId]->weight == 0){
        usefullPoints->RemoveElementFromUsefulElementsList(change.pointId);
        emptyPoints->AddElementToUsefulElementsList(change.pointId);
    }
    if(array[change.pointId]->dimWeights[change.dimChanged] + change.weightDelta == 0){
        array[change.pointId]->usefullDims->AddElementToUsefulElementsList( change.dimChanged);
    }
    if(array[change.pointId]->weight + change.weightDelta == 0){
        usefullPoints->AddElementToUsefulElementsList(change.pointId);
        emptyPoints->RemoveElementFromUsefulElementsList(change.pointId);
    }
}

void CArraySubCMediansPoint::RevertChanges(CChangesTracker* changesTracker){
    for (TModelComplexity i = 0; i < changesTracker->a_nbChanges; i++){
        RevertChange(changesTracker->a_changes[i]);
    }
}

void CArraySubCMediansPoint::ApplyChange(TModelChange change){
    //printf("Sto provando a fare un cambiamento\n");
	modifedCorePoints->AddElementToUsefulElementsList(change.pointId);
	//printf("Weight prima dell'add: %f\n", weight);
    weight += change.weightDelta;
    //printf("Weight dopo l'add: %f\n", weight);
    array[change.pointId]->weight += change.weightDelta;
    array[change.pointId]->dimWeights[change.dimChanged] += change.weightDelta;
    array[change.pointId]->positions[change.dimChanged] = change.newPosition;
    if(array[change.pointId]->dimWeights[change.dimChanged] == 0){
        //printf("Primo if di cambiamento - il peso della dimensione cambiata è diventato 0\n");
        array[change.pointId]->usefullDims->RemoveElementFromUsefulElementsList(change.dimChanged);
    }
    if(array[change.pointId]->weight == 0){
        //printf("Secondo if di cambiamento - il peso del punto del cambiamento è 0\n");
        usefullPoints->RemoveElementFromUsefulElementsList( change.pointId );
        emptyPoints->AddElementToUsefulElementsList( change.pointId );
    }
    if(array[change.pointId]->weight - change.weightDelta == 0){
        //printf("Terzo if di cambiamento - il peso del punto cambiato meno il deltaPeso è 0\n");
        usefullPoints->AddElementToUsefulElementsList( change.pointId );
        emptyPoints->RemoveElementFromUsefulElementsList( change.pointId );
    }
    if(array[change.pointId]->dimWeights[change.dimChanged] - change.weightDelta == 0){
        //printf("Quarto if di cambiamento - il peso della dimensione cambiata meno deltaPeso è 0\n");
        array[change.pointId]->usefullDims->AddElementToUsefulElementsList( change.dimChanged);
    }
}

void CArraySubCMediansPoint::ApplyChanges(CChangesTracker* changesTracker){
	modifedCorePoints->size = 0;
    for (TModelComplexity i = 0; i < changesTracker->a_nbChanges; i++){
        //printf("Change %d: \n", i);
        ApplyChange(changesTracker->a_changes[i]);
    }
}

TPointId CArraySubCMediansPoint::ChoosePointId(TOption option){
    if(option == CHOOSEPOINTUNIFORMLY) {
        return usefullPoints->array[a_p_prng->uniform(0, usefullPoints->size)];
    }
    if(option == CHOOSEOLDESTPOINT){
        TPointId point = usefullPoints->array[pointedPoint];
        pointedPoint++;
        pointedPoint = pointedPoint % usefullPoints->size;
        return point;
    }
    perror("Point choice option not supported yet ERROR!\n");
    return(0);
}

TPointId CArraySubCMediansPoint::ChooseEmptyPoint(TOption option){
    if(option == CHOOSEEMPTYPOINTUNIFORMLY) {
        return emptyPoints->array[a_p_prng->uniform(0, emptyPoints->size)];
    }
    if(option == CHOOSEFIRSTEMPTYPOINT){
        return emptyPoints->array[0];
    }
    perror("Point choice option not supported yet ERROR!\n");
    return(0);
}

TModelComplexity CArraySubCMediansPoint::ComputeWeight(){
    weight = 0;
    for(TPointId i = 0; i < usefullPoints->size; i++){
        CSubCMediansPoint * point = array[usefullPoints->array[i]];
        weight += point->weight;
    }
    return weight;
}


TDispersion CArraySubCMediansPoint::ComputeDistanceToPoint(CSubCMediansPoint* point){
    TDispersion locdisp = 0;
    if (usefullPoints->size == 0)locdisp = point->dispersionToBarycenter;
    else locdisp = MAXDISPERSION;
    point->dispersionToGroup = point->dispersionToBarycenter;
    point->groupId           = NULLCLUSTER;

    for(TPointId i = 0; i < usefullPoints->size; i++) {
        CSubCMediansPoint *corepoint = array[usefullPoints->array[i]];
        TDispersion tmpDisp = corepoint->ComputeDistanceToPoint(point);
        if(tmpDisp <= locdisp){
            locdisp                  = tmpDisp;
            point->dispersionToGroup = locdisp;
            point->groupId           = usefullPoints->array[i];
        }
    }

    return locdisp;
}

TDispersion CArraySubCMediansPoint::ComputeDistanceToArray(CArraySubCMediansPoint* data){
    TDispersion sum = 0;
    for(TPointId i = 0; i < data->usefullPoints->size; i++){
        sum += ComputeDistanceToPoint(data->array[data->usefullPoints->array[i]]);
    }
    return sum;
}

TPointId CArraySubCMediansPoint::ComputeNumberOfClusters(TPointId M){
    TPointId numberOfClusters = 0;
    for(TPointId i = 0; i < usefullPoints->size; i++){
        if (array[usefullPoints->array[i]]->nbPointsInCluster > M) {
            numberOfClusters ++;
        }
    }
    return numberOfClusters;
}

TReal CArraySubCMediansPoint::ComputeMeanDimensionalityCorePoints(){
    TReal meanDimensionality = 0;
    for(TPointId i = 0; i < usefullPoints->size; i++){
        meanDimensionality += array[usefullPoints->array[i]]->usefullDims->size;
    }
    return (TReal) (meanDimensionality * 1.0 / (usefullPoints->size+ ZERODIVISIONSECURITY));
}

TReal CArraySubCMediansPoint::ComputeMeanDimensionalityClusters(TPointId M){
    TReal meanDimensionality = 0;
    TPointId nbClusters = 0;
    for(TPointId i = 0; i < usefullPoints->size; i++){
        if (array[usefullPoints->array[i]]->nbPointsInCluster > M) {
            meanDimensionality += array[usefullPoints->array[i]]->usefullDims->size;
            nbClusters++;
        }
    }
    return (TReal) (meanDimensionality * 1.0 / (nbClusters+ ZERODIVISIONSECURITY));
}

TReal CArraySubCMediansPoint::ComputeMeanWeightCorePoints(){
    TReal meanWeights = 0;
    for(TPointId i = 0; i < usefullPoints->size; i++){
        meanWeights += array[usefullPoints->array[i]]->weight;
    }
    return (TReal) (meanWeights * 1.0 / (usefullPoints->size+ ZERODIVISIONSECURITY));
}

TReal CArraySubCMediansPoint::ComputeMeanWeightClusters(TPointId M){
    TReal meanWeights = 0;
    TPointId nbClusters = 0;
    for(TPointId i = 0; i < usefullPoints->size; i++){
        if (array[usefullPoints->array[i]]->nbPointsInCluster > M) {
            meanWeights += array[usefullPoints->array[i]]->weight;
            nbClusters++;
        }
    }
    return (TReal) (meanWeights * 1.0 / (nbClusters+ ZERODIVISIONSECURITY));
}

TReal CArraySubCMediansPoint::ComputeMeanWeightDimClusters(TPointId M){
    TReal meanWeights = 0;
    TPointId nbClusters = 0;
    for(TPointId i = 0; i < usefullPoints->size; i++){
        if (array[usefullPoints->array[i]]->nbPointsInCluster > M) {
            meanWeights += array[usefullPoints->array[i]]->weight * 1.0 / (array[usefullPoints->array[i]]->usefullDims->size+ ZERODIVISIONSECURITY);
            nbClusters++;
        }
    }
    return (TReal) (meanWeights * 1.0 / (nbClusters + ZERODIVISIONSECURITY) );
}

TReal CArraySubCMediansPoint::ComputeMeanWeightDimCorePoints(){
    TReal meanWeights = 0;
    for(TPointId i = 0; i < usefullPoints->size; i++) {
        meanWeights += array[usefullPoints->array[i]]->weight * 1.0 / array[usefullPoints->array[i]]->usefullDims->size;
    }
    return (TReal) (meanWeights * 1.0 / (usefullPoints->size + ZERODIVISIONSECURITY) );
}

TReal CArraySubCMediansPoint::ComputeCoverage(TPointId M){
    TReal coveredNumberOfPoints = 0;
    TReal totalNumberOfPoints = 0;
    for(TPointId i = 0; i < usefullPoints->size; i++){
        if (array[usefullPoints->array[i]]->nbPointsInCluster > M) {
            coveredNumberOfPoints += array[usefullPoints->array[i]]->nbPointsInCluster;
        }
        totalNumberOfPoints += array[usefullPoints->array[i]]->nbPointsInCluster;
    }
    return (TReal) (coveredNumberOfPoints * 1.0 / (totalNumberOfPoints+ ZERODIVISIONSECURITY));
}

void CArraySubCMediansPoint::Print(){
    printf("\n");
    printf("*****************************************************\n");
    printf("––––––PRINTING CARRAYSubCMediansPOINT–––––\n");
    printf("MaxSize: %hi, weight: %hi\n",sizeMax,weight);
    printf("USEFULPOINTS:\n");
    usefullPoints->Print();
    printf("----------POINTS LIST------------%hi\n",usefullPoints->size);
    for(TPointId i = 0; i < usefullPoints->size; i ++){
        array[usefullPoints->array[i]]->Print();
    }
    printf("*****************************************************\n");
    printf("\n");
}

void CArraySubCMediansPoint::Empty(){
    while(usefullPoints->size>0) {
        TPointId pointIdToErase = usefullPoints->array[0];
        array[pointIdToErase]->Empty();
        usefullPoints->RemoveElementFromUsefulElementsList(pointIdToErase);
        emptyPoints->AddElementToUsefulElementsList(pointIdToErase);
    }
    weight = 0;
}
