#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
XM - eXplainable Modeling
Copyright 2018 © Alberto Castellini, Alessandro Farinelli, Francesco Masillo

This file is part of XM.
XM is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

XM is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with XM.  If not, see <http://www.gnu.org/licenses/>.

Please, report suggestions/comments/bugs to
 alberto.castellini@univr.it, alessandro.farinelli@univr.it, francesco.masillo@studenti.univr.it
"""

import pandas as pd
import numpy as np
from pyitlib import discrete_random_variable as drv

def SU(numero, feature, solution):
    
    #print numero
    #Hfr = drv.entropy(feature, fill_value=None)
    #print "Entropy  FR:{0:.3f}".format(Hfr)
    #Hfr_sol = drv.entropy_conditional(feature, solution, fill_value=None)
    #print "Entropy  FR|I:{0:.3f}".format(Hfr_sol) 
    #HI = drv.entropy(solution, fill_value=None)
    #print "Entropy I:{0:.3f}".format(HI)
    featureDisc = pd.cut(feature, 30, labels=False)
    IG = drv.information_mutual(featureDisc, solution)
    #print "IG:{0:.3f}".format(IG)
    #IG = Hfr-Hfr_sol
    #print IG
    den = drv.entropy(featureDisc)+drv.entropy(solution)
    #print "Den:{0:.3f}".format(den)
    result = 2*(IG/den)
    #print "Result:{0:.3f}".format(result)
    return result
