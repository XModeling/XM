#!/usr/bin/env python
import os
os.environ["CC"] = "g++"
from distutils.core import setup, Extension
module = Extension('SubCMediansWrapper_c', ["SubCMediansWrapper.cpp","CSubCMediansClust.cpp", "CPrng.cpp", "CArraySubCMediansPoint.cpp", "CChangesTracker.cpp", "CSubCMediansPoint.cpp", "CListAtomicElements.cpp", "TProbabilitiesArray.cpp", "TUsefullElements.cpp"],libraries=['gsl','blas'])
module.extra_compile_args = [ '-std=gnu++0x']#,'-pg']

setup(name='SubCMediansWrapper_c',
	version='1.0',
	ext_modules=[module])