//
// Created by peignier sergio on 29/01/2016.
//

#include <stdio.h>
#include <stdlib.h>
#include "CSubCMediansClust.h"

CSubCMediansClust::CSubCMediansClust(){
    a_Kmax       = DEFAULTKMAX;
	a_maxNbDims  = DEFAULTDIMMAX;
	a_K          = 0;
	a_p_prng     = new CPrng();
	a_dispersion = MAXDISPERSION;
}

CSubCMediansClust::CSubCMediansClust(TModelComplexity Koption, TDimId maxNbDims, TPointId Hoption, TPointId Moption, TSeed seed,
                           TOption optionGenerateDeletion, TOption optionGenerateInsertion,TOption optionFIFO,
                           TOption optionTrainWithLatestObject,TOption optionDoNotOptimizeIfDistanceDecrease, 
                           TModelComplexity lambda, TModelComplexity mu){
    //printf("%i %i %i %i %i %i %i %i %i %i\n",Koption,maxNbDims,Hoption,optionGenerateDeletion, optionGenerateInsertion,optionFIFO,optionTrainWithLatestObject,optionDoNotOptimizeIfDistanceDecrease,lambda, mu);
    a_dispersion = 0;
    a_Kmax      = Koption;
	a_maxNbDims = maxNbDims;
	a_H         = Hoption;
	a_M         = Moption;
	a_K         = 0;
	a_seed      = seed;
	a_p_prng     = new CPrng(a_seed);
    a_bestChanges = new CChangesTracker();
    a_localChanges = new CChangesTracker();
    a_G = new CArraySubCMediansPoint(Koption,maxNbDims,a_p_prng);
    a_G_ = new CArraySubCMediansPoint(Koption,maxNbDims,a_p_prng);
    a_D = new CArraySubCMediansPoint(Hoption,maxNbDims,a_p_prng);
    a_innerAtomicElements = new CListAtomicElements(Koption,a_p_prng);
    a_features = (TFeatures*) malloc(sizeof(TFeatures));
    //a_outerAtomicElements = AllocateMemoryListAtomicElements(a_outerAtomicElements,a_Kmax * a_maxNbDims);
    a_optionGenerateDeletion = optionGenerateDeletion;
    a_optionGenerateInsertion = optionGenerateInsertion;
    a_optionFIFO =optionFIFO;
    a_optionTrainWithLatestObject = optionTrainWithLatestObject;
    a_optionDoNotOptimizeIfDistanceDecrease = optionDoNotOptimizeIfDistanceDecrease;
    a_last_point_added = 0;
    a_lambda = lambda;
    a_mu = mu;
}



CSubCMediansClust::~CSubCMediansClust(){
	delete a_G;
    delete a_G_;
	delete a_D;
	delete a_innerAtomicElements;
    delete a_localChanges;
    delete a_bestChanges;
    delete a_p_prng;
    free(a_features);
}

void CSubCMediansClust::TrainOnInstanceImpl(CSubCMediansPoint* SubCMediansPointTraining) {
    TDispersion dispersionBeforePointInclusion = a_dispersion;
    InsertPointToD(SubCMediansPointTraining);
    TDispersion dispersionAfterPointInclusion = a_dispersion;
    if(!a_optionDoNotOptimizeIfDistanceDecrease || (dispersionBeforePointInclusion <= dispersionAfterPointInclusion ) ){
        UpdateGUsingD();
    }
}

void CSubCMediansClust::InsertPointToD(CSubCMediansPoint* SubCMediansPointTraining){
    if (a_D->usefullPoints->size >= a_H){
        TPointId indexPointToErase = 0;
        indexPointToErase = (TPointId) a_D->ChoosePointId(CHOOSEPOINTUNIFORMLY);
        a_last_point_added = indexPointToErase;
        a_dispersion -= a_D->array[indexPointToErase]->dispersionToGroup;
        a_D->array[indexPointToErase]->CloneOtherPoint(SubCMediansPointTraining);
        a_G->ComputeDistanceToPoint((a_D->array[indexPointToErase]));
        a_dispersion += a_D->array[indexPointToErase]->dispersionToGroup;
    }
    else{
        TPointId newPointId = 0;
        newPointId = a_D->ChooseEmptyPoint(CHOOSEEMPTYPOINTUNIFORMLY);
        a_last_point_added = newPointId;
        a_D->array[newPointId]->CloneOtherPoint(SubCMediansPointTraining);
        a_D->usefullPoints->AddElementToUsefulElementsList(newPointId);
        a_D->emptyPoints->RemoveElementFromUsefulElementsList(newPointId);
        a_G->ComputeDistanceToPoint(a_D->array[newPointId]);
        a_dispersion += a_D->array[newPointId]->dispersionToGroup;
    }
}

void CSubCMediansClust::UpdateGUsingTransferedCluster(CSubCMediansPoint* cluster){
    for(TDimId i = 0; i < cluster->usefullDims->size; i++){
        TDimId dimension = cluster->usefullDims->array[i];
        TPosition position = cluster->positions[dimension];
        UpdateGUsingTransferedPair(dimension,position);
    }
}

void CSubCMediansClust::UpdateGUsingTransferedPair(TDimId dimension, TPosition position) {
    for(TModelComplexity nbGenerations = 0; nbGenerations<a_mu;nbGenerations++){
        TDispersion minDispersion = a_dispersion;
        TPointId trial = 0;
        do {
            GenerateHorizontalPairChangesTracker(a_localChanges,dimension, position);
            a_G_->ApplyChanges(a_localChanges);
            TDispersion localDispersion = a_G_->ComputeDistanceToArray(a_D);
            if(localDispersion <= minDispersion){
                minDispersion = localDispersion;
                a_bestChanges->CloneOtherTracker(a_localChanges);
            }
            a_G_->RevertChanges(a_localChanges);
            trial ++;
        }while (trial < a_lambda );
        if(minDispersion <= a_dispersion){
            a_dispersion = minDispersion;
            a_G->ApplyChanges(a_bestChanges);
            a_G_->ApplyChanges(a_bestChanges);
            a_innerAtomicElements->ApplyDeletions(a_bestChanges);
            a_innerAtomicElements->ApplyInsertions(a_bestChanges);
            a_K = a_G->ComputeWeight();
            a_bestChanges->ResetTracker();
            assert(a_innerAtomicElements->size == a_K);
        }
    }
}

void CSubCMediansClust::UpdateGUsingD(){
    for(TModelComplexity nbGenerations = 0; nbGenerations<a_mu;nbGenerations++){
    	a_G->ApplyChanges(a_bestChanges);
        TDispersion minDispersion = a_dispersion;
        TPointId trial = 0;
        do{
            GenerateChangesTracker(a_localChanges);
            a_G_->ApplyChanges(a_localChanges);
            TDispersion localDispersion = a_G_->ComputeDistanceToArray(a_D);
            if(localDispersion <= minDispersion){
                minDispersion = localDispersion;
                a_bestChanges->CloneOtherTracker(a_localChanges);
            }
            a_G_->RevertChanges(a_localChanges);
            trial ++;
        }while (trial < a_lambda );
        if(minDispersion <= a_dispersion){
            a_dispersion = minDispersion;
            a_G->ApplyChanges(a_bestChanges);
            a_G_->ApplyChanges(a_bestChanges);
            a_innerAtomicElements->ApplyDeletions(a_bestChanges);
            a_innerAtomicElements->ApplyInsertions(a_bestChanges);
            a_K = a_innerAtomicElements->size;
            a_bestChanges->ResetTracker();
        }
        a_G->ComputeDistanceToArray(a_D);
    }
}

TElement CSubCMediansClust::ChooseModelPair(TOption option){
    TModelComplexity indexAtom = a_innerAtomicElements->ChooseAtomIndex();
    return indexAtom;
}



TPointId CSubCMediansClust::GenerateCorePointInsertionID(CArraySubCMediansPoint* model, TOption option){
    TPointId groupInsertion = -1;
    if (a_p_prng->uniform() < 1. / (a_K+ZERODIVISIONSECURITY)) {
        groupInsertion = model->ChooseEmptyPoint(CHOOSEEMPTYPOINTUNIFORMLY);
    }
    else {
        groupInsertion = a_innerAtomicElements->ChooseAtom().pointId;
    }
    return groupInsertion;
}

TAtomicElement CSubCMediansClust::GenerateInsertionFromData(CArraySubCMediansPoint* data, CArraySubCMediansPoint* model, TOption option){
    TAtomicElement insertedElement;
    TPointId selectedPoint = data->ChoosePointId(CHOOSEPOINTUNIFORMLY);
    TDimId selectedDim = data->array[selectedPoint]->ChooseDim(CHOOSEDIMPROPORTIONALTOWEIGHT);//add option
    TPosition   selectedPos   = data->array[selectedPoint]->positions[selectedDim];
    insertedElement.pointId = GenerateCorePointInsertionID(model,option);
    insertedElement.dimId   = selectedDim;
    insertedElement.pos     = selectedPos;
    return insertedElement;
}

void CSubCMediansClust::GenerateHorizontalPairChangesTracker(CChangesTracker* changesTracker,TDimId dimTransfered, TPosition posTransfered){
    changesTracker->ResetTracker();
    if(a_K == a_Kmax){
        TElement indexAtom = ChooseModelPair(a_optionGenerateDeletion);
        TAtomicElement atomToErase = a_innerAtomicElements->array[indexAtom];
        TDimId dimChanged = atomToErase.dimId;
        TPointId pointId    = atomToErase.pointId;
        TPosition oldPosition = a_G->array[pointId]->positions[dimChanged];
        TWeight oldWeight = a_G->array[pointId]->dimWeights[dimChanged];
        changesTracker->AddDeletionToTracker(indexAtom, pointId, dimChanged, oldPosition,oldWeight,DELTAWEIGHT);
    }
    TAtomicElement insertedElement = {0,0,0.0};
    insertedElement.pointId = GenerateCorePointInsertionID(a_G,a_optionGenerateInsertion);
    insertedElement.dimId   = dimTransfered;
    insertedElement.pos     = posTransfered;
    TPosition oldPosition = a_G->array[insertedElement.pointId]->positions[insertedElement.dimId];
    changesTracker->AddInsertionToTracker(insertedElement, oldPosition, DELTAWEIGHT);
}

TBoolean CSubCMediansClust::GenerateChangesTracker(CChangesTracker* changesTracker){
	changesTracker->ResetTracker();
    if(a_K == a_Kmax){
        TElement indexAtom = ChooseModelPair(a_optionGenerateDeletion);
        TAtomicElement atomToErase = a_innerAtomicElements->array[indexAtom];
        TDimId dimChanged = atomToErase.dimId;
        TPointId pointId    = atomToErase.pointId;
        TPosition oldPosition = a_G->array[pointId]->positions[dimChanged];
        TWeight oldWeight = a_G->array[pointId]->dimWeights[dimChanged];
        changesTracker->AddDeletionToTracker(indexAtom, pointId, dimChanged, oldPosition,oldWeight,DELTAWEIGHT);
        }
    TAtomicElement insertedElement = GenerateInsertionFromData(a_D, a_G_, a_optionGenerateInsertion);
    TPosition oldPosition = a_G->array[insertedElement.pointId]->positions[insertedElement.dimId];
    changesTracker->AddInsertionToTracker(insertedElement, oldPosition, DELTAWEIGHT);
    return 1;
}

void CSubCMediansClust::ResetNbObjectsInClusters(CArraySubCMediansPoint* model,CArraySubCMediansPoint* data){
	for(TPointId i = 0; i < model->usefullPoints->size; i++){
		model->array[model->usefullPoints->array[i]]->nbPointsInCluster = 0;
	}
	for(TPointId i = 0; i < data->usefullPoints->size; i++){
        if (data->array[data->usefullPoints->array[i]]->groupId != NULLCLUSTER){
    		model->array[data->array[data->usefullPoints->array[i]]->groupId]->nbPointsInCluster ++;
        }
	}
}


void CSubCMediansClust::ComputeFeatures(){
    a_dispersion = a_G->ComputeDistanceToArray(a_D);
    ResetNbObjectsInClusters(a_G,a_D);
    a_features->dispersion = a_dispersion;
    a_features->K = a_K;
    a_features->numberOfCorePoints = a_G->usefullPoints->size;
    a_features->numberOfClusters = a_G->ComputeNumberOfClusters(a_M);
    a_features->meanDimensionalityCorePoints = a_G->ComputeMeanDimensionalityCorePoints();
    a_features->meanDimensionalityClusters = a_G->ComputeMeanDimensionalityClusters(a_M);
    a_features->meanAtomicElementsCorePoints = a_G->ComputeMeanWeightCorePoints();
    a_features->meanAtomicElementsClusters = a_G->ComputeMeanWeightClusters(a_M);
    a_features->meanAtomicElementsCorePointDimensions = a_G->ComputeMeanWeightDimCorePoints();
    a_features->meanAtomicElementsClusterDimensions = a_G->ComputeMeanWeightDimClusters(a_M);
    a_features->coverage = a_G->ComputeCoverage(a_M);
}

void CSubCMediansClust::CloneFeatures(TFeatures* other){
    a_features->dispersion = other->dispersion;
    a_features->K = other->K;
    a_features->numberOfCorePoints = other->numberOfCorePoints;
    a_features->numberOfClusters = other->numberOfClusters;
    a_features->meanDimensionalityCorePoints = other->meanDimensionalityCorePoints;
    a_features->meanDimensionalityClusters = other->meanDimensionalityClusters;
    a_features->meanAtomicElementsCorePoints = other->meanAtomicElementsCorePoints;
    a_features->meanAtomicElementsClusters = other->meanAtomicElementsClusters;
    a_features->meanAtomicElementsCorePointDimensions = other->meanAtomicElementsCorePointDimensions;
    a_features->meanAtomicElementsClusterDimensions = other->meanAtomicElementsClusterDimensions;
    a_features->coverage = other->coverage;
}


void CSubCMediansClust::CloneOtherSubCMediansClust(CSubCMediansClust* other){
    a_dispersion = other->a_dispersion;
    a_Kmax      = other->a_Kmax;
    a_maxNbDims = other->a_maxNbDims;
    a_H         = other->a_H;
    a_M         = other->a_M;
    a_K         = other->a_K;
    a_bestChanges->CloneOtherTracker(other->a_bestChanges);
    a_localChanges ->CloneOtherTracker(other->a_localChanges);
    a_G->CloneOtherArraySubCMediansPoint(other->a_G);
    a_G_->CloneOtherArraySubCMediansPoint(other->a_G);
    a_innerAtomicElements->CloneCListAtomicElements(other->a_innerAtomicElements);
    a_optionGenerateDeletion = other->a_optionGenerateDeletion;
    a_optionGenerateInsertion = other->a_optionGenerateInsertion;
    a_optionFIFO =other->a_optionFIFO;
    a_optionTrainWithLatestObject = other->a_optionTrainWithLatestObject;
    a_optionDoNotOptimizeIfDistanceDecrease = other->a_optionDoNotOptimizeIfDistanceDecrease;
    ComputeFeatures();
}

void CSubCMediansClust::Empty(){
    a_K = 0;
    a_G->Empty();
    a_G_->Empty();
    a_innerAtomicElements->Empty();
}

void CSubCMediansClust::AddAtomicElement(TPointId pointId, TDimId dimension,TPosition position){
    TModelChange change = {pointId,dimension,DELTAWEIGHT,0,position};
    TAtomicElement atomicElement = {pointId,dimension,position};
    a_G->ApplyChange(change);
    a_G_->ApplyChange(change);
    a_innerAtomicElements->InsertElement(atomicElement);
    a_K ++;
}
