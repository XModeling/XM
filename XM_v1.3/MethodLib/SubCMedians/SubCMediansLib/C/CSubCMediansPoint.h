//
// Created by peignier sergio on 29/01/2016.
//

#ifndef C_CSubCMediansPOINT_H
#define C_CSubCMediansPOINT_H
#include "SubCMedians_def.h"
#include "TUsefullElements.h"
#include "TProbabilitiesArray.h"
#include "CPrng.h"

class CSubCMediansPoint {
public:
    CSubCMediansPoint(TModelComplexity elementsSize,CPrng* prng);
    ~CSubCMediansPoint();

    CPrng* a_p_prng;
    TWeight      * dimWeights;
    TPosition    * positions;
    TUsefullElements * usefullDims;
    TProbabilitiesArray * probaUsefullDim;
    TWeight        weight;
    TPointId    nbPointsInCluster;
    TPointId    id;
    TPointId    groupId;
    TDimId     maxNbDims;
    TDispersion dispersionToGroup;
    TDispersion dispersionToBarycenter;
    TPointId   classId;
    
    void CloneOtherPoint(CSubCMediansPoint *other);
    TDimId ChooseDim(TOption option);
    void Print();
    void Reallocate(TModelComplexity elementsSize);
    void Empty();
    void ComputeDistanceToBarycenter();
    TDispersion ComputeDistanceToPoint(CSubCMediansPoint *otherPoint);
};


#endif //C_CSubCMediansPOINT_H
