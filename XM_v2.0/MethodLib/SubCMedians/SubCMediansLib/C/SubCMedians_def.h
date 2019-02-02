#ifndef SubCMediansDEF
#define SubCMediansDEF

#include <float.h>

#define MAXNBCHANGES    2
#define MAXNBINSERTIONS 1
#define MAXNBDELETIONS  1
#define MAXDISPERSION   FLT_MAX
#define DEFAULTKMAX     5000
#define DEFAULTDIMMAX   5000
#define CHOOSEDIMPROPORTIONALTOWEIGHT 0
#define ZERODIVISIONSECURITY 0.000001

#define BARYCENTERPOS   0.
#define DELTAWEIGHT     1
#define MEANDISTRUBUTION 0.0
#define STDDISTRUBUTION 1.0

#define CHOOSEPOINTUNIFORMLY 0
#define CHOOSEEMPTYPOINTUNIFORMLY 0

#define CHOOSEFIRSTEMPTYPOINT 1
#define CHOOSEOLDESTPOINT 1

#define FIFOMODE 1
#define FIROMODE 0

#define INSERTIONPROPORTIONALTOCOMPLEXITY 0
#define INSERTIONPROPORTIONALTONUMBEROFOBJECTS 1
#define INSERTIONPROPORTIONALTOINVERSENUMBEROFOBJECTS 2

#define DELETIONPROPORTIONALTOCOMPLEXITY 0
#define DELETIONPROPORTIONALTONUMBEROFOBJECTS 1
#define DELETIONPROPORTIONALTOINVERSENUMBEROFOBJECTS 2

#define NULLCLUSTER -1

#define ABS(x) ((x)<0 ? -(x) : (x))
#define MIN(a,b) ((a) < (b) ? (a) : (b))

typedef short TBoolean;
typedef short TElement;
typedef float TProbability;
typedef unsigned long int  TSeed;
typedef short  TDimId;
typedef short  TPointId;
typedef short  TModelComplexity;
typedef float TPosition;
typedef short TWeight;
typedef double TDispersion;
typedef short TOption;
typedef float TReal;

typedef struct TAtomicElement{
	TPointId  pointId;
	TDimId    dimId;
	TPosition pos;
}TAtomicElement;

typedef struct TModelChange{
	TPointId   pointId;
	TDimId     dimChanged;
	TWeight    weightDelta;
	TPosition  oldPosition;
	TPosition  newPosition;
}TModelChange;

typedef struct TFeatures{
    TDispersion dispersion;
    TModelComplexity K;
    TPointId numberOfCorePoints;
    TPointId numberOfClusters;
    TReal    meanDimensionalityCorePoints;
    TReal    meanDimensionalityClusters;
    TReal    meanAtomicElementsCorePoints;
    TReal    meanAtomicElementsClusters;
    TReal    meanAtomicElementsCorePointDimensions;
    TReal    meanAtomicElementsClusterDimensions;
    TReal    coverage;
}TFeatures;
#endif
