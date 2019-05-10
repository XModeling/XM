//
// Created by peignier sergio on 29/01/2016.
//

#ifndef C_CLISTATOMICELEMENTS_H
#define C_CLISTATOMICELEMENTS_H


#include "SubCMedians_def.h"
#include "CSubCMediansPoint.h"
#include "CChangesTracker.h"

class CListAtomicElements {
public:
    CListAtomicElements(TModelComplexity nbElements, CPrng* prng);
    ~CListAtomicElements();
    CPrng* a_p_prng;
    TAtomicElement * array;
    TModelComplexity size;
    TModelComplexity a_Kmax;
    void InsertElement(TAtomicElement insertedElement);

    void DeleteElement(TModelComplexity idDeleteElement);

    void ApplyDeletions(CChangesTracker *changesTracker);

    void ApplyInsertions(CChangesTracker *changesTracker);

    TModelComplexity ChooseAtomIndex();

    TAtomicElement ChooseAtom();

    TElement FindPointAndDimFromAtomicElementsList(TPointId pointID, TDimId dimID);

    void Print();

    void CloneCListAtomicElements(CListAtomicElements *other);

    void Empty();
};


#endif //C_CLISTATOMICELEMENTS_H
