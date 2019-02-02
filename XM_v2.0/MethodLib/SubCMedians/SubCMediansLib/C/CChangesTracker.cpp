//
// Created by peignier sergio on 29/01/2016.
//

#include <stdio.h>
#include "CChangesTracker.h"

CChangesTracker::CChangesTracker() {
    ResetTracker();
}

CChangesTracker::~CChangesTracker() {

}

void CChangesTracker::ResetTracker(){
    a_nbChanges = 0;
    a_nbInsertions = 0;
    a_nbDeletions = 0;
}


void CChangesTracker::AddDeletionToTracker(TModelComplexity indexAtom,TPointId pointId, TDimId dimChanged,
                                           TPosition oldPosition, TWeight oldWeight, TWeight delta){
    a_deletionsID[a_nbDeletions] = indexAtom;
    a_changes[a_nbChanges].dimChanged = dimChanged;
    a_changes[a_nbChanges].pointId = pointId;
    a_changes[a_nbChanges].oldPosition = oldPosition;
    a_changes[a_nbChanges].weightDelta = - delta;
    if (oldWeight - delta == 0){
        a_changes[a_nbChanges].newPosition = (TPosition) BARYCENTERPOS;
    }
    else{
        a_changes[a_nbChanges].newPosition = oldPosition;
    }
    a_nbChanges ++;
    a_nbDeletions ++;
}

void CChangesTracker::AddInsertionToTracker(TAtomicElement insertedElement,TPosition oldPosition, TWeight delta){
    a_insertions[a_nbInsertions] = insertedElement;
    a_changes[a_nbChanges].dimChanged = insertedElement.dimId;
    a_changes[a_nbChanges].pointId    = insertedElement.pointId;
    a_changes[a_nbChanges].oldPosition  = oldPosition;
    a_changes[a_nbChanges].newPosition  = insertedElement.pos;
    a_changes[a_nbChanges].weightDelta  = delta;
    a_nbChanges ++;
    a_nbInsertions ++;
}


void CChangesTracker::CloneOtherTracker(CChangesTracker* other){
    a_nbChanges = other->a_nbChanges;
    a_nbInsertions = other->a_nbInsertions;
    a_nbDeletions = other->a_nbDeletions;
    for(TModelComplexity i = 0; i < a_nbChanges; i ++){
        a_changes[i].dimChanged = other->a_changes[i].dimChanged;
        a_changes[i].weightDelta = other->a_changes[i].weightDelta;
        a_changes[i].oldPosition = other->a_changes[i].oldPosition;
        a_changes[i].newPosition = other->a_changes[i].newPosition;
        a_changes[i].pointId = other->a_changes[i].pointId;
    }
    for(TModelComplexity i = 0; i < a_nbInsertions; i ++){
        a_insertions[i].pointId = other->a_insertions[i].pointId;
        a_insertions[i].dimId   = other->a_insertions[i].dimId;
        a_insertions[i].pos   = other->a_insertions[i].pos;
    }
    for(TModelComplexity i = 0; i < a_nbDeletions; i ++){
        a_deletionsID[i] = other->a_deletionsID[i];
    }
}

void CChangesTracker::Print() {
    printf("******************\n");
    for (TModelComplexity i = 0; i < a_nbChanges; i++) {
        printf("----------CHANGE----------\n");
        printf("dimChanged: %hi, pointID: %hi, ", a_changes[i].dimChanged, a_changes[i].pointId);
        printf("oldP: %f, newP: %f, weightDelta %hi\n", a_changes[i].oldPosition,
               a_changes[i].newPosition, a_changes[i].weightDelta);
        printf("--------------------------\n");
    }
    printf("******************\n");

}