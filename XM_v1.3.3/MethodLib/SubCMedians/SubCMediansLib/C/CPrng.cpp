#include "CPrng.h"
/*----------------------------
 * CONSTRUCTORS
 *----------------------------*/

/* default constructor */
CPrng::CPrng( void ){
  _prng = gsl_rng_alloc(gsl_rng_mt19937);
}

/* constructor with seed */
CPrng::CPrng( unsigned long int seed ){
  _prng = gsl_rng_alloc(gsl_rng_mt19937);
  gsl_rng_set(_prng, seed);
}

/* copy constructor */
CPrng::CPrng( const CPrng& prng ){
  _prng = gsl_rng_clone(prng._prng);
}

/*----------------------------
 * DESTRUCTORS
 *----------------------------*/
CPrng::~CPrng( void ){
  gsl_rng_free(_prng);
}

/*----------------------------
 * PUBLIC METHODS
 *----------------------------*/
void CPrng::setSeed(unsigned long int seed ){
    gsl_rng_set(_prng, seed);
}
/* return a [0, 1[ uniform distributed double */
double CPrng::uniform( void ){
  return gsl_ran_flat(_prng, 0.0, 1.0);
}

/* return a [min, max[ uniform distributed integer */
int CPrng::uniform( int min, int max ){
  //assert(min <= max);
  return (int) floor(gsl_ran_flat(_prng, min, max));
}

/* return a bernouilli draw (0 or 1) of probability p */
int CPrng::bernouilli( double p ){
  //assert(p >= 0.0);
  //assert(p <= 1.0);
  return gsl_ran_bernoulli(_prng, p);
}

/* return a binomial draw of size n and probability p */
int CPrng::binomial( int n, double p ){
  //assert(n >= 0);
  //assert(p >= 0.0);
  //assert(p <= 1.0);
  return gsl_ran_binomial(_prng, p, (unsigned int) n);
}

/* return in draws[] a multinomial draw of N entities, in K categories and probabilities probas[] */
void CPrng::multinomial(unsigned int* draws, double* probas, int N, int K){
  return gsl_ran_multinomial(_prng, (const size_t) K, (const unsigned int) N, probas, draws);
}

/* return a random number from a gaussian distribution N(mu, sigma) */
double CPrng::gaussian( double mu, double sigma ){
  //assert(sigma > 0.0);
  return mu+gsl_ran_gaussian_ziggurat(_prng, sigma);
}

/* return a random number from an exponential distribution exp(mu) */
int CPrng::exponential( double mu ){
  return (int) ceil(gsl_ran_exponential(_prng, mu));
}

int CPrng::wheelOfFotune(float* wheel, int wheelSize){
	double alea = uniform();
	for (int i = 0; i < wheelSize-1; i++){
		if ((alea >= wheel[i])&&(alea < wheel[i+1])) return i;
	}
	return -1;
}

void CPrng::saveState(FILE* backup_state_rng){
	gsl_rng_fwrite (backup_state_rng, _prng);
	}
	
void CPrng::loadState(FILE* backup_state_rng){
	gsl_rng_fread (backup_state_rng, _prng);
	}

void CPrng::shuffle(void * base, size_t n, size_t size){
	gsl_ran_shuffle(_prng, base, n, size);
	}
