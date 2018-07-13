//
// Created by peignier sergio on 29/01/2016.
//

#ifndef C_TUSEFULLELEMENTS_H
#define C_TUSEFULLELEMENTS_H


#include "SubCMedians_def.h"
#include "CPrng.h"

class TUsefullElements {
public:
    TUsefullElements(TModelComplexity maximalSize);
    ~TUsefullElements();
    TElement * array;
    TElement size;

    void RemoveElementFromUsefulElementsList(TElement elementId);

    void AddElementToUsefulElementsList(TElement element);

    void CloneOtherElementsArray(TUsefullElements *other);

    void Print();
};


#endif //C_TUSEFULLELEMENTS_H
