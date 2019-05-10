#include <iostream>
#include <gsl/gsl_rng.h>
#include <gsl/gsl_randist.h>
#include <cmath>
#include <assert.h>

#ifndef __Prototype__Prng__
#define __Prototype__Prng__


class CPrng{
  
public:
  
  /*----------------------------
   * CONSTRUCTORS
   *----------------------------*/
  CPrng( void );
  CPrng( unsigned long int seed );
  CPrng( const CPrng& prng );
  
  /*----------------------------
   * DESTRUCTORS
   *----------------------------*/
  ~CPrng( void );
 
  
  /*----------------------------
   * PUBLIC METHODS
   *----------------------------*/
  double uniform( void );
  int    uniform( int min, int max );
  int    bernouilli( double p );
  int    binomial( int n, double p );
  void   multinomial(unsigned int* draws, double* probas, int n, int size);
  double gaussian( double mu, double sigma );
  int    exponential( double mu );
  int    wheelOfFotune(float* wheel, int wheelSize);
  void   shuffle(void * base, size_t n, size_t size); 
  void   saveState(FILE* backup_state_rng);
  void   loadState(FILE* backup_state_rng);
  /*----------------------------
   * PUBLIC ATTRIBUTES
   *----------------------------*/
  gsl_rng* _prng;

    void setSeed(unsigned long seed);
};


#endif /* defined(__Prototype__Prng__) */
