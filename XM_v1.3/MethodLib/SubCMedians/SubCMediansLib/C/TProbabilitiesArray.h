//
// Created by peignier sergio on 29/01/2016.
//

#ifndef C_TPROBABILITIESARRAY_H
#define C_TPROBABILITIESARRAY_H


#include "SubCMedians_def.h"
#include "TUsefullElements.h"
class CArraySubCMediansPoint;
class TProbabilitiesArray {
public:
    TProbabilitiesArray(TModelComplexity elementsSize);
    ~TProbabilitiesArray();
    TProbability * array;
    TModelComplexity size;

    void CloneOtherProbabilitiesArray(TProbabilitiesArray *other);

    void ComputeProbabilitiesFromWeights(TUsefullElements *usefulIndexes, TModelComplexity *weightArray);

    void ComputeProbabilitiesFromPointsWeights(TUsefullElements* usefulIndexes, CArraySubCMediansPoint *arrayPoints);

    void ComputeProbabilitiesFromAllPointsNumberOfPoints( CArraySubCMediansPoint *arrayPoints, TProbability basalEmptyClusterProbability);

    void ComputeProbabilitiesFromAllPointsInverseNumberOfPoints(CArraySubCMediansPoint *arrayPoints, TProbability basalEmptyClusterProbability);

    void Print();

    void ComputeProbabilitiesFromPointsNumberOfObjects(TUsefullElements *usefulIndexes, CArraySubCMediansPoint *arrayPoints, TProbability basalEmptyClusterProbability);

    void ComputeProbabilitiesFromInversePointsNumberOfObjects(TUsefullElements *usefulIndexes, CArraySubCMediansPoint *arrayPoints, TProbability basalEmptyClusterProbability);

};


#endif //C_TPROBABILITIESARRAY_H
