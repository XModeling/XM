//
// Created by peignier sergio on 29/01/2016.
//

#ifndef C_CCHANGESTRACKER_H
#define C_CCHANGESTRACKER_H

#include "SubCMedians_def.h"
class CChangesTracker{
public:
    TModelChange a_changes[MAXNBCHANGES];
    TModelComplexity a_nbChanges;
    TAtomicElement a_insertions[MAXNBINSERTIONS];
    TModelComplexity a_nbInsertions;
    TModelComplexity a_deletionsID[MAXNBDELETIONS];
    TModelComplexity a_nbDeletions;

    CChangesTracker();
    ~CChangesTracker();
    void ResetTracker();
    void AddDeletionToTracker(TModelComplexity indexAtom, TPointId pointId, TDimId dimChanged, TPosition oldPosition,
                              TWeight oldWeight, TWeight delta);
    void AddInsertionToTracker(TAtomicElement insertedElement, TPosition oldPosition, TWeight delta);
    void CloneOtherTracker(CChangesTracker* other);
    void Print();
};
#endif //C_CCHANGESTRACKER_H