//
// Created by peignier sergio on 29/01/2016.
//

#ifndef C_CARRAYSubCMediansPOINT_H
#define C_CARRAYSubCMediansPOINT_H


#include "TUsefullElements.h"
#include "TProbabilitiesArray.h"
#include "CSubCMediansPoint.h"
#include "CChangesTracker.h"
#include "CPrng.h"

class CArraySubCMediansPoint {
public:
    CArraySubCMediansPoint(TModelComplexity nbElements, TModelComplexity elementsSize, CPrng* prng);
    ~CArraySubCMediansPoint();
    CPrng* a_p_prng;
    TUsefullElements * usefullPoints;
    TUsefullElements * emptyPoints;
    TUsefullElements * modifedCorePoints;
    TProbabilitiesArray * probaUsefullPoints;
    TPointId pointedPoint;
    CSubCMediansPoint ** array;
    TPointId       sizeMax;
    TModelComplexity weight;

    void RevertChange(TModelChange change);
    void RevertChanges(CChangesTracker *changesTracker);
    void ApplyChange(TModelChange change);
    void ApplyChanges(CChangesTracker *changesTracker);
    TPointId ChoosePointId(TOption option);
    TModelComplexity ComputeWeight();
    TDispersion ComputeDistanceToPoint(CSubCMediansPoint *point);
    TDispersion ComputeDistanceToArray(CArraySubCMediansPoint *data);
    TPointId ChooseEmptyPoint(TOption option);
    void Print();
    TPointId ComputeNumberOfClusters(TPointId M);
    TReal ComputeMeanDimensionalityCorePoints();
    TReal ComputeMeanDimensionalityClusters(TPointId M);
    TReal ComputeMeanWeightCorePoints();
    TReal ComputeMeanWeightClusters(TPointId M);
    TReal ComputeMeanWeightDimClusters(TPointId M);
    TReal ComputeMeanWeightDimCorePoints();
    TReal ComputeCoverage(TPointId M);
    void CloneOtherArraySubCMediansPoint(CArraySubCMediansPoint *other);
    void Empty();

};


#endif //C_CARRAYSubCMediansPOINT_H
