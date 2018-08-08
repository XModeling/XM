//
// Created by peignier sergio on 29/01/2016.
//


#ifndef KYMERA
#define KYMERA

#include "SubCMedians_def.h"
#include "CPrng.h"
#include "CChangesTracker.h"
#include "TUsefullElements.h"
#include "CArraySubCMediansPoint.h"
#include "CListAtomicElements.h"


class CSubCMediansClust{
public :
    CSubCMediansClust();
    CSubCMediansClust(TModelComplexity Koption, TDimId maxNbDims, TPointId Hoption, TPointId Moption, TSeed seed, TOption optionGenerateDeletion, TOption optionGenerateInsertion, TOption optionFIFO, TOption optionTrainWithLatestObject,TOption optionDoNotOptimizeIfDistanceDecrease, TModelComplexity lambda, TModelComplexity mu);
    ~CSubCMediansClust();
    CArraySubCMediansPoint*   a_D;
    CArraySubCMediansPoint*   a_G;
    CArraySubCMediansPoint*   a_G_;
    CListAtomicElements* a_innerAtomicElements;
    TFeatures* a_features;
    CChangesTracker*     a_localChanges;
    CChangesTracker*     a_bestChanges;
    CPrng*               a_p_prng;
    TModelComplexity     a_K;
    TPointId             a_H;
    TPointId             a_M;
    TModelComplexity     a_Kmax;
    TDimId               a_maxNbDims;
    TDispersion          a_dispersion;
    TSeed                a_seed;
    TOption              a_optionGenerateDeletion;
    TOption              a_optionGenerateInsertion;
    TOption              a_optionFIFO;
    TOption              a_optionTrainWithLatestObject;
    TPointId             a_last_point_added;
    TOption              a_optionDoNotOptimizeIfDistanceDecrease;
    TModelComplexity     a_lambda;
    TModelComplexity     a_mu;

    TBoolean GenerateChangesTracker(CChangesTracker* changesTracker);
    void ResetNbObjectsInClusters(CArraySubCMediansPoint* model,CArraySubCMediansPoint* data);
    void UpdateGUsingD();
    void TrainOnInstanceImpl(CSubCMediansPoint* SubCMediansPointTraining);
    void ComputeFeatures();
    void InsertPointToD(CSubCMediansPoint *SubCMediansPointTraining);
    void CloneOtherSubCMediansClust(CSubCMediansClust *other);
    void CloneFeatures(TFeatures *other);
    TAtomicElement GenerateInsertionFromData(CArraySubCMediansPoint *data, CArraySubCMediansPoint *model, TOption option);
    TElement ChooseModelPair(TOption option);
    TPointId GenerateCorePointInsertionID(CArraySubCMediansPoint *model, TOption option);
    void GenerateHorizontalPairChangesTracker(CChangesTracker *changesTracker, TDimId dimTransfered,
                                              TPosition posTransfered);
    void UpdateGUsingTransferedPair(TDimId dim, TPosition pos);
    void UpdateGUsingTransferedCluster(CSubCMediansPoint *cluster);
    void Empty();
    void AddAtomicElement(TPointId pointId, TDimId dimension, TPosition position);
};
#endif